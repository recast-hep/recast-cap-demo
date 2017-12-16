import yaml
import yadage.workflow_loader
from yadage.utils import WithJsonRefEncoder
import json
import pkg_resources
import os

def combine_prepare(template,adapter,analysis):
    upstream_workflow = yadage.workflow_loader.workflow(adapter['workflow'], adapter['toplevel'])
    template['stages'][0]['scheduler']['workflow'] = upstream_workflow
    downstream_workflow = yadage.workflow_loader.workflow(analysis['workflow'], analysis['toplevel'])
    analysis_pars = analysis.get('preset_pars',{})
    analysis_pars.update(**adapter['interface_parameters'])
    template['stages'][1]['scheduler']['parameters'] = analysis_pars
    template['stages'][1]['scheduler']['workflow'] = downstream_workflow
    return template

def finalize_combination(template,upstream_pars):
    template['stages'][0]['scheduler']['bindings'] = upstream_pars
    return template

def workflow_options(ctx,workdir):

    templatepath = pkg_resources.resource_filename('wflowyadageworker','resources/basicinterfacetempl.yml')

    template = yaml.load(open(templatepath))
    if ctx['combinedspec']['adapter'] == 'from-request':
        adapter = yaml.load(open('{}/inputs/evgenflow.yml'.format(workdir)))
    else:
        adapter = ctx['combinedspec']['adapter']

    prepped = combine_prepare(template,adapter,ctx['combinedspec']['analysis'])

    input_path = '{}/inputs/input.yaml'.format(workdir)

    raise RuntimeError('yadage version change not carried over to combined workflows yet')
