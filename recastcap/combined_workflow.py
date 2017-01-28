import yaml
import yadage.workflow_loader
from yadage.helpers import WithJsonRefEncoder
from yadage.clihelpers import discover_initfiles 	
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
	template['stages'][0]['scheduler']['parameters'] = upstream_pars
	return template



def workflow_command(ctx,workdir):

	templatepath = pkg_resources.resource_filename('recastcap','resources/basicinterfacetempl.yml')

	template = yaml.load(open(templatepath))
	if ctx['combinedspec']['adapter'] == 'from-request':
		adapter = yaml.load(open('{}/inputs/evgenflow.yml'.format(workdir)))
	else:
		adapter = ctx['combinedspec']['adapter']
	
	prepped = combine_prepare(template,adapter,ctx['combinedspec']['analysis'])

	initdata = yaml.load(open('{}/inputs/input.yaml'.format(workdir)))
	initdata = discover_initfiles(initdata,os.path.realpath(workdir))

	finalized = finalize_combination(prepped,initdata)	

	combinedfilename = '{}_combined.yml'.format(ctx['jobguid'])
	yaml.safe_dump(json.loads(json.dumps(finalized, cls = WithJsonRefEncoder)), stream = open(combinedfilename,'w'))
	return 'yadage-run -u {updateinterval} -b {backend} {workdir} {workflow}'.format(
       workdir = workdir,
       updateinterval = 10,
       backend = os.environ.get('RECAST_YADAGEBACKEND','multiproc:2'),
       workflow = combinedfilename
	)