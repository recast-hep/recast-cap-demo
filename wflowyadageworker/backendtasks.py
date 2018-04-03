import logging
import os
import simple_workflow
import simple_workflow_fromjson
import combined_workflow

from wflowyadageworker.tracker import EmitTracker
from yadage.steering_api import steering_ctx
from yadage.steering_object import YadageSteering
import yadage.utils

log = logging.getLogger(__name__)

def init_workflow(ctx):
    log.info('initializing interactive yadage workflow: %s', ctx)
    jobguid = ctx['jobguid']
    workdir = ctx['workdir']

    log.info('workflow id: %s', jobguid)

    wflow_state_file = os.path.join(ctx['workdir'],'_yadage','yadage_state.json')
    if os.path.exists(os.path.join(workdir,'_yadage')):
        log.info('already initialized')
        assert os.path.exists(wflow_state_file)


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
    assert ys

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
        with steering_ctx(**yadage_kwargs) as ys:
            ys.adage_argument(additional_trackers = [EmitTracker(jobguid)])
    except:
        log.exception('workflow failed')
        raise RuntimeError('workflow failed')

    log.info('workflow succeeded, workflow plugin end.')
