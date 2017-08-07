import logging
import yaml
import os

log = logging.getLogger('WFLOWSERVICELOG')

def workflow_command(ctx,workdir):
    fixed_pars = ctx.get('fixed_pars',{})
    initdir = os.path.join(workdir,'inputs')
    if not os.path.exists(initdir):
        os.makedirs(initdir)
    presetfilename = os.path.join(initdir,'preset.yaml')
    with open(presetfilename,'w') as presetfile:
        yaml.dump(fixed_pars,presetfile, default_flow_style = False)

    log.info('preset parameters are %s',fixed_pars)
    yadage_pars = os.path.join(initdir,'input.yaml')

    log.info('running workflow on context %s',ctx)

    if not os.path.exists(workdir):
        log.error('workdirectory: %s does not exist',workdir)

    if not os.path.exists(yadage_pars):
        log.warning('workflow parameter file: %s does not exist',yadage_pars)

    cmd = 'yadage-run -u {updateinterval} -d inputs -b {backend} -t {toplevel} {workdir} {workflow} {initpar} {presetpar}'.format(
        workdir = workdir,
        backend = os.environ.get('WFLOW_YADAGEBACKEND','multiproc:2'),
        workflow = ctx['workflow'],
        initpar  = yadage_pars if os.path.exists(yadage_pars) else '',
        presetpar = presetfilename,
        updateinterval = os.environ.get('WFLOW_YADAGEUPDATE',30),
        toplevel = ctx.get('toplevel','from-github/pseudocap')
    )
    return cmd
