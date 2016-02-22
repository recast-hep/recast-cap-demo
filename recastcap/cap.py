import json
import pkg_resources
import requests
import jsoncap
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