
import os
import cap
import importlib
import subprocess
import adage.backends
import time
import psutil
import sys
import logging
import traceback

class RECAST_Task(object):
    def __init__(self,func):
        self.func = func
        self.step = None
        self.context = None

    def __repr__(self):
        return '<RECAST name: {}>'.format(self.step['name'])

    def __call__(self):
        return self.func(self.step,self.context)
  
    def set(self,step,context):
        self.step = step
        self.context = context

class RECAST_Rule(object):
    def __init__(self,stageinfo,workflow,allrules,global_context):
        self.stageinfo = stageinfo
        self.global_context = global_context
        self.workflow = workflow
        self.allrules = allrules
  
    def applicable(self,dag):
        depstats = []
        for x in self.stageinfo['dependencies']:
            deprule = self.allrules[x]
            if not 'scheduled_steps' in deprule.stageinfo:
                depstats += [False]
            else:
                depstats += [all([x.successful() for x in deprule.stageinfo['scheduled_steps']])]
                
        return all(depstats)

    def apply(self,dag):
        self.schedule(dag)
    
    def schedule(self,dag):
        from scheduler_handlers import handlers as sched_handlers
        sched_spec = self.stageinfo['scheduler']
        scheduler = sched_handlers[sched_spec['scheduler-type']]
        scheduler(self.workflow,self.stageinfo,dag,self.global_context,sched_spec)
    
class RECAST_Result(object):
    def __init__(self,resultobj,task):
        self.resultobj = resultobj
        self.task = task
        self.result = None
    
    def ready(self):
        return self.resultobj.ready()
    def successful(self):
        return self.resultobj.successful()
    def get(self):
        if self.result:
            return self.result
      
        try:
            taskresult = self.resultobj.get()
        except:
            t,e,tb = sys.exc_info()
            print "taskresult retrieval failed error: {} {}".format(t,e)
            print traceback
            traceback.print_tb(tb)
            raise
        
        result = {
            'RECAST_metadata':{
                'outputs':self.publish(self.task.step,self.task.context)
            },
            'taskresult':taskresult
        }
        self.result = result
        return self.result

    def publish(self,step,context):
        pubtype =  step['step_spec']['publisher']['publisher-type']
        from publisher_handlers import handlers as pub_handlers
        publisher = pub_handlers[pubtype]
        return publisher(step,context)
  

class RECAST_Backend(adage.backends.MultiProcBackend):
    def submit(self,task):
        return RECAST_Result(super(RECAST_Backend,self).submit(task),task)

    def ready(self,result):
        ready =  super(RECAST_Backend,self).ready(result)
        return ready
    
    def result_of(self,result):
        return result.get()

def build_command(step):
    proc_type =  step['step_spec']['process']['process-type']
    from process_handlers import handlers as proc_handlers
    handler = proc_handlers[proc_type]
    command = handler(step['step_spec']['process'],step['attributes'])
    return command


def RCST(func):
    def sig(*args,**kwargs):
        instance = RECAST_Task(func)
        instance.set(*args,**kwargs)
        return instance
    func.s = sig
    return func

@RCST
def runStep(step,global_context):
    steplog = '{}/{}.step.log'.format(os.path.abspath(global_context['workdir']),step['name'])
    log = logging.getLogger('step_logger_{}'.format(step['name']))
    fh  = logging.FileHandler(steplog)
    fh.setLevel(logging.DEBUG)
    log.addHandler(fh)
    
    log.info('starting log for step: {}'.format(step['name']))
    
    command = build_command(step)
    
    environment = step['step_spec']['environment']
    from environment_handlers import handlers as env_handlers
    handlercls = env_handlers[environment['environment-type']]
    handler = handlercls(step['name'],global_context,command,environment, log = log)
    handler.handle()
