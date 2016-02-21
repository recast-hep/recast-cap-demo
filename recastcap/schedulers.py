import json
import cap
import adage
import yaml
import foradage
from foradage import runStep
  
def single_step_from_context(workflow,stage,dag,context,sched_spec):
  stepname = '{}_single'.format(stage['name'])
  step = {
    'name':stepname,
    'attributes': {k:v.format(**context) for k,v in stage['parameters'].iteritems()},
    'step_spec':sched_spec['steps']['single']
  }
  
  step = adage.mknode(dag,task = runStep.s(step,context), nodename = stepname)
  stage['scheduled_steps'] = [step]

def map_step_from_context(workflow,stage,dag,context,sched_spec):
    mappar = sched_spec['map_parameter']
    to_input = sched_spec['to_input']
    stepname_template   = sched_spec['stepname']
    stagepars = stage['parameters']

    #for the one parameter pointed to by mappar, we interpret the string as a serialized yaml list
    mapparlist = yaml.load(stagepars[mappar].format(**context))
    
    #the remaining parameter set will be used for each scheduled step
    parswithoutmap = stage['parameters']
    parswithoutmap.pop(mappar)
    stage['scheduled_steps'] = []
    for index,p in enumerate(mapparlist):
        withindex = context.copy()
        withindex.update(index = index)
        
        attributes = {k:str(v).format(**withindex) for k,v in parswithoutmap.iteritems()}
        attributes[to_input] = p
        step = {
          'name': stepname_template.format(index = index),
          'attributes': attributes,
          'step_spec':sched_spec['steps']['map'],
        }
        stepobj = adage.mknode(dag,task = runStep.s(step,context), nodename = step['name'])
        stage['scheduled_steps'] += [stepobj]

def map_from_dep_output(workflow,stage,dag,context,sched_spec):
    dependencies = [s for s in workflow['stages'] if s['name'] in sched_spec['from_stages']]
    
    outputkey           = sched_spec['take_outputs']
    to_input            = sched_spec['to_input']
    stepname_template   = sched_spec['stepname']
    stage['scheduled_steps'] = []
    index = 0
    for x in [step for d in dependencies for step in d['scheduled_steps']]:
      rcmeta = x.result_of()['RECAST_metadata']
      for this_index,y in enumerate(rcmeta['outputs'][outputkey]):
        withindex = context.copy()
        withindex.update(index = index)

        
        attributes = {k:str(v).format(**withindex) for k,v in stage['parameters'].iteritems()}
        attributes[to_input] = y
        
        used_inputs = {x.task.step['name'] :[(outputkey,this_index)]}

        step = {
          'name': stepname_template.format(index = index),
          'attributes': attributes,
          'step_spec':sched_spec['steps']['map'],
          'used_inputs':used_inputs
        }
        stepobj = adage.mknode(dag,task = runStep.s(step,context), nodename = step['name'])
        dag.addEdge(x,stepobj)
        stage['scheduled_steps'] += [stepobj]
        index += 1

def reduce_from_dep_output(workflow,stage,dag,context,sched_spec):
    dependencies = [s for s in workflow['stages'] if s['name'] in sched_spec['from_stages']]

    new_inputs = []
    used_inputs = {}
    for x in [step for d in dependencies for step in d['scheduled_steps']]:
        used_inputs[x.task.step['name']] = []
        outputkey =  sched_spec['take_outputs']
        for i,y in enumerate(x.result_of()['RECAST_metadata']['outputs'][outputkey]):
            new_inputs += [y]
            used_inputs[x.task.step['name']] += [(outputkey,i)]

    to_input = sched_spec['to_input']
    attributes = {k:str(v).format(**context) for k,v in stage['parameters'].iteritems()}
    attributes[to_input] = new_inputs
    
    stepname = '{}_reduce'.format(stage['name'])
    step = {
        'name':stepname,
        'attributes':attributes,
        'step_spec':sched_spec['steps']['reduce'],
        'used_inputs':used_inputs
    }

    step = adage.mknode(dag,runStep.s(step,context), nodename = stepname)
    stage['scheduled_steps'] = [step]
    for x in [s for d in dependencies for s in d['scheduled_steps']]:
        dag.addEdge(x,step)
