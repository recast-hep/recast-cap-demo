import logging
import yaml
import os

log = logging.getLogger('WFLOWSERVICELOG')

def workflow_options(ctx,workdir):

    log.info('running workflow on context %s',ctx)

    initdata = ctx.get('fixed_pars',{})

    initdir = os.path.join(workdir,'inputs')
    if not os.path.exists(initdir):
        os.makedirs(initdir)

    yadage_pars = os.path.join(initdir,'input.yaml')
    if os.path.exists(yadage_pars):
        initdata.update(**yaml.load(open(yadage_pars)))
    else:
        log.info('no workflow parameters in init dir')


    if not os.path.exists(workdir):
        log.error('workdirectory: %s does not exist',workdir)

    return dict(
        workflow = ctx['workflow'],
        toplevel = ctx.get('toplevel','from-github/pseudocap'),
        initdata = initdata,
        dataopts = {'initdir': os.path.abspath(os.path.join(workdir,initdir))}
    )
