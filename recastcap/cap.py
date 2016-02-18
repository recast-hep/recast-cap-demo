import json
import pkg_resources
import os
import requests

import jsoncap
# HOST = os.environ['CAP_HOST']
# def api_getcall(endpoint):
#     r = requests.get('{}/api/{}'.format(HOST,endpoint), auth = (os.environ['CAP_USER'],os.environ['CAP_ACCESSKEY']))
#     if not r.ok:
#         print r
#         raise RuntimeError('call failed')
#
#     return json.loads(r.content)['data']


def localcap_workflow(workflowpath):
    toplevel = pkg_resources.resource_filename('recastcap','capdata/yamlworkflow')
    schemas  = pkg_resources.resource_filename('recastcap','capdata/justschemas')
    return jsoncap.validate_workflow(workflowpath,toplevel,schemas)
    
def workflow(name):
    ok, workflow =  localcap_workflow(name)
    if ok:
        return workflow
    else:
        raise RuntimeError('Schema is not validating')
    # return api_getcall('workflow/{}'.format(name))

def step(name,stepname):
    return api_getcall('step/{}/{}'.format(name,stepname))

def node(node,nodename):
    return api_getcall('node/{}/{}'.format(node,nodename))
