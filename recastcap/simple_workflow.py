import logging
import yaml
import os

log = logging.getLogger('RECAST')


def workflow_command(ctx,workdir):
    fixed_pars = ctx.get('fixed_pars',{})
    presetfilename = '{}/inputs/preset.yaml'.format(workdir)
    with open(presetfilename,'w') as presetfile:
        yaml.dump(fixed_pars,presetfile, default_flow_style = False)

    log.info('preset parameters are %s',fixed_pars)
    yadagectx = '{}/inputs/input.yaml'.format(workdir)

    log.info('running recast workflow on context {}'.format(ctx))

    if not os.path.exists(workdir):
        log.error('workdirectory: %s does not exist',workdir)

    if not os.path.exists(yadagectx):
        log.error('context file: %s does not exist',yadagectx)

    cmd = 'yadage-run -u {updateinterval} -d inputs -b {backend} -t {toplevel} {workdir} {workflow} {initpar} {presetpar}'.format(
        workdir = workdir,
        backend = os.environ.get('RECAST_YADAGEBACKEND','multiproc:2'),
        workflow = ctx['workflow'],
        initpar  = yadagectx,
        presetpar = presetfilename,
        updateinterval = 30,
        toplevel = ctx.get('toplevel','from-github/pseudocap')
    )
    return cmd
