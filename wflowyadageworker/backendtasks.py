import logging
import os
import yaml
import wflowyadageworker.tracker

import simple_workflow
import simple_workflow_fromjson
import combined_workflow

from yadage.steering_object import YadageSteering
import yadage.utils

logging.basicConfig(level=logging.INFO)
log = logging.getLogger('WFLOWSERVICELOG')

def init_workflow(ctx):
    log.info('initializing interactive yadage workflow: %s', ctx)
    jobguid = ctx['jobguid']
    workdir = ctx['workdir']

    log.info('workflow id: %s', jobguid)

    if os.path.exists(os.path.join(workdir,'_yadage')):
        log.info('already initialized')
        assert os.path.exists(wflow_state_file)

    wflow_state_file = os.path.join(ctx['workdir'],'_yadage','yadage_state.json')

    yadage_kwargs = dict(
        dataarg = workdir,
        modelsetup = 'filebacked:{}'.format(wflow_state_file)
    )
    log.info('yadabe base settings %s', yadage_kwargs)
    if 'combinedspec' in ctx:
        additional_kwargs = combined_workflow.workflow_options(ctx,workdir)
        log.info('combined workflow')
    elif type(ctx['workflow'])==dict:
        additional_kwargs = simple_workflow_fromjson.workflow_options(ctx,workdir)
        log.info('workflow from context')
    else:
        additional_kwargs = simple_workflow.workflow_options(ctx,workdir)
        log.info('load workflow from source')

    yadage_kwargs.update(**additional_kwargs)
    log.info('additional keyword arguments were %s', additional_kwargs)
    log.info('executing yadage initalization: %s',yadage_kwargs)

    ys = YadageSteering.create(**yadage_kwargs)

def run_workflow(ctx):
    log.info('running yadage workflow for context: %s', ctx)

    jobguid = ctx['jobguid']
    workdir = ctx['workdir']

    backend = 'py:sharedstatekube:backend'
    backendopts = {
        'optsyaml':'/yadageconfig/backendopts'
    }

    log.info('connecting backend: %s', backend)

    yadage_kwargs = dict(
        dataarg = workdir,
        backend = yadage.utils.setupbackend_fromstring(backend,backendopts),
        updateinterval = float(os.environ.get('WFLOW_YADAGEUPDATE',30)),
    )

    log.info('yadabe base settings %s', yadage_kwargs)

    if 'combinedspec' in ctx:
        additional_kwargs = combined_workflow.workflow_options(ctx,workdir)
        log.info('combined workflow')
    elif type(ctx['workflow'])==dict:
        additional_kwargs = simple_workflow_fromjson.workflow_options(ctx,workdir)
        log.info('workflow from context')
    else:
        additional_kwargs = simple_workflow.workflow_options(ctx,workdir)
        log.info('load workflow from source')

    yadage_kwargs.update(**additional_kwargs)

    log.info('additional keyword arguments were %s', additional_kwargs)
    try:
        log.info('executing yadage workflows with: %s',yadage_kwargs)
        with yadage.steering_api.steering_ctx(**yadage_kwargs) as ys:
            if yaml.load(os.environ.get('WFLOW_PLUGIN_TRACK','true')):
                ys.adage_argument(additional_trackers = [
                    wflowyadageworker.tracker.EmitTracker(jobguid)
                ])
    except:
        log.exception('workflow failed')
        raise RuntimeError('workflow failed')

    log.info('workflow succeeded, workflow plugin end.')
