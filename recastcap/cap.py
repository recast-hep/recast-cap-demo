import pkg_resources
import jsoncap

def workflow(name):
    toplevel = pkg_resources.resource_filename('recastcap','capdata/yamlworkflow')
    schemas  = pkg_resources.resource_filename('recastcap','capdata/justschemas')
    ok, workflow =  jsoncap.validate_workflow(name,toplevel,schemas)
    if ok:
        return workflow
    else:
        raise RuntimeError('Schema is not validating')