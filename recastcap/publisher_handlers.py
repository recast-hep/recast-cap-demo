import yaml

handlers = {}

def process_attr_pub_handler(step,context):
    outputs = {}
    for k,v in step['step_spec']['publisher']['outputmap'].iteritems():
      outputs[k] = [step['attributes'][v]]
    return outputs
    
handlers['process-attr-pub'] = process_attr_pub_handler

def fromyaml_pub_handler(step,context):
    yamlfile =  step['step_spec']['publisher']['yamlfile']
    yamlfile =  yamlfile.replace('/workdir',context['workdir'])
    pubdata = yaml.load(open(yamlfile))
    return pubdata
    
handlers['fromyaml-pub'] = fromyaml_pub_handler

def dummy_pub_handler(step,context):
    return  step['step_spec']['publisher']['publish']
    
handlers['dummy-pub'] = dummy_pub_handler