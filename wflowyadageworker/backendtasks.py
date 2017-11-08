import logging
import subprocess
import os
import yaml
import json
import shlex
import wflowyadageworker.tracker
import logging

import simple_workflow
import simple_workflow_fromjson
import combined_workflow

import yadage.steering_api
import yadage.utils

logging.basicConfig(level=logging.INFO)
log = logging.getLogger('WFLOWSERVICELOG')

def run_workflow(ctx):
    log.info('running yadage workflow for context: %s', ctx)
    jobguid = ctx['jobguid']

    workdir = os.path.join('workdirs',jobguid)

    backend = os.environ.get('WFLOW_YADAGEBACKEND','multiproc:auto')
    backendopts = {}

    log.info('connecting backend: %s', backend)

    yadage_kwargs = dict(
        dataarg = workdir,
        backend = yadage.utils.setupbackend_fromstring(backend,backendopts),
        updateinterval = os.environ.get('WFLOW_YADAGEUPDATE',30),
    )

    if 'combinedspec' in ctx:
        additional_kwargs = combined_workflow.workflow_options(ctx,workdir)
    elif 'workflow_json' in ctx:
        additional_kwargs = simple_workflow_fromjson.workflow_options(ctx,workdir)
    else:
        additional_kwargs = simple_workflow.workflow_options(ctx,workdir)

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
