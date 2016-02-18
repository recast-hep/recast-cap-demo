
import os
import cap
import importlib
import subprocess
import adage.backends
import time
import psutil
import sys

class RECAST_Task(object):
  def __init__(self,func):
    self.func = func
    self.node = None
    self.context = None

  def __repr__(self):
    return '<RECAST name: {}>'.format(self.node['name'])

  def __call__(self):
    return self.func(self.node,self.context)
  
  def set(self,node,context):
    self.node = node
    self.context = context

def RCST(func):
  def sig(*args,**kwargs):
    instance = RECAST_Task(func)
    instance.set(*args,**kwargs)
    return instance
  func.s = sig
  return func

class RECAST_Rule(object):
  def __init__(self,stepinfo,workflow,allrules,global_context):
    self.stepinfo = stepinfo
    self.global_context = global_context
    self.workflow = workflow
    self.allrules = allrules

  def applicable(self,dag):
    depstats = []
    for x in self.stepinfo['dependencies']:
      deprule = self.allrules[x]
      if not 'scheduled_nodes' in deprule.stepinfo:
        depstats += [False]
      else:
        depstats += [all([x.successful() for x in deprule.stepinfo['scheduled_nodes']])]
    
    return all(depstats)

  def apply(self,dag):
    self.schedule(dag)

  def schedule(self,dag):
    from scheduler_handlers import handlers as sched_handlers
    sched_spec = self.stepinfo['scheduler']
    scheduler = sched_handlers[sched_spec['scheduler-type']]
    scheduler(self.workflow,self.stepinfo,dag,self.global_context,sched_spec)
    
import traceback
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
                'outputs':self.publish(self.task.node)
            },
            'taskresult':taskresult
        }
        self.result = result
        return self.result

    def publish(self,node):
        pubtype =  node['node_spec']['publisher']['publisher-type']
        from publisher_handlers import handlers as pub_handlers
        publisher = pub_handlers[pubtype]
        return publisher(node)
  

class RECAST_Backend(adage.backends.MultiProcBackend):
  def submit(self,task):
    return RECAST_Result(super(RECAST_Backend,self).submit(task),task)

  def ready(self,result):
    ready =  super(RECAST_Backend,self).ready(result)
    return ready
    
  def result_of(self,result):
    return result.get()

def build_command(node):
  proc_type =  node['node_spec']['process']['process-type']
  from process_handlers import handlers as proc_handlers
  handler = proc_handlers[proc_type]
  command = handler(node['node_spec']['process'],node['attributes'])
  return command

import logging

@RCST
def runNode(node,global_context):
    nodelog = '{}/{}.node.log'.format(os.path.abspath(global_context['workdir']),node['name'])
    log = logging.getLogger('node_logger_{}'.format(node['name']))
    fh  = logging.FileHandler(nodelog)
    fh.setLevel(logging.DEBUG)
    log.addHandler(fh)
    
    log.info('starting log for node: {}'.format(node['name']))
    
    print node
    command = build_command(node)
    
    environment = node['node_spec']['environment']
    from environment_handlers import handlers as env_handlers
    handlercls = env_handlers[environment['environment-type']]
    handler = handlercls(node['name'],global_context,command,environment, log = log)
    handler.handle()
