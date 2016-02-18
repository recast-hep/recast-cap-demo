handlers = {}

def process_attr_pub_handler(node):
    outputs = {}
    for k,v in node['node_spec']['publisher']['outputmap'].iteritems():
      outputs[k] = [node['attributes'][v]]
    return outputs
    
handlers['process-attr-pub'] = process_attr_pub_handler