import json
import cap
import adage
import foradage
from foradage import runNode
  
def single_node_from_context(workflow,step,dag,context,sched_spec):
  nodename = '{}_single'.format(step['name'])
  node = {
    'name':nodename,
    'attributes': {k:v.format(**context) for k,v in step['parameters'].iteritems()},
    'node_spec':sched_spec['nodes']['single']
  }
  
  node = adage.mknode(dag,task = runNode.s(node,context), nodename = nodename)
  step['scheduled_nodes'] = [node]
  
def map_from_dep_output(workflow,step,dag,context,nodename_template,dependency,outputkey,to_input,to_output,output_template):
  stepspec = cap.step(*(step['step_spec'].split('/',1)))

  dep = [x for x in workflow if x['name'] == dependency][0]

  step['scheduled_nodes'] = []
  index = 0
  for x in dep['scheduled_nodes']:
    rcmeta = x.result_of()['RECAST_metadata']
    for this_index,y in enumerate(rcmeta['outputs'][outputkey]):
      copy = context.copy()
      copy.update(index = index)
      
      attr = {}
      attr[to_input] = y
      attr[to_output] = output_template.format(**copy)
      
      used_inputs = {x.task.node['name'] :[(outputkey,this_index)]}
      
      node = {
        'name': nodename_template.format(**copy),
        'attributes': attr,
        'spec':stepspec['definition']['node_spec'],
        'used_inputs':used_inputs
      }
      
      nodeobj = adage.mknode(dag,task = runNode.s(node,context), nodename = node['name'])
      dag.addEdge(x,nodeobj)
      step['scheduled_nodes'] += [nodeobj]
      index += 1

def reduce_from_dep_output(workflow,step,dag,context,sched_spec):
# def reduce_from_dep_output(workflow,step,dag,context,nodename,dependency,outputkey,to_input):
    print step.keys()
    print sched_spec.keys()
    dependency = [stage for stage in workflow['stages'] if stage['name'] == sched_spec['from_stage']][0]
    print dependency

    new_inputs = []
    used_inputs = {}
    for x in dependency['scheduled_nodes']:
        used_inputs[x.task.node['name']] = []
        outputkey =  sched_spec['take_outputs']
        for i,y in enumerate(x.result_of()['RECAST_metadata']['outputs'][outputkey]):
            new_inputs += [y]
            used_inputs[x.task.node['name']] += [(outputkey,i)]

    to_input = sched_spec['to_input']
    print 'to_input : {} new input: {}'.format(to_input,new_inputs)
    attributes = {k:str(v).format(**context) for k,v in step['parameters'].iteritems()}
    attributes[to_input] = new_inputs
    
    nodename = '{}_reduce'.format(step['name'])
    node = {
        'name':nodename,
        'attributes':attributes,
        'node_spec':sched_spec['nodes']['reduce'],
        'used_inputs':used_inputs
    }

    node = adage.mknode(dag,runNode.s(node,context), nodename = nodename)
    step['scheduled_nodes'] = [node]
    for x in dependency['scheduled_nodes']:
        dag.addEdge(x,node)
