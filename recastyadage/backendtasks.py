import logging
import subprocess
import os
import yaml
import shlex
import simple_workflow
import combined_workflow

logging.basicConfig(level=logging.INFO)
log = logging.getLogger('RECAST')

def recast(ctx):
    log.info('running yadage workflow for context: %s', ctx)
    jogbuid = ctx['jobguid']

    workdir = os.path.join('workdirs',jogbuid)

    if 'combinedspec' in ctx:
        cmd = combined_workflow.workflow_command(ctx,workdir)
    else:
        cmd = simple_workflow.workflow_command(ctx,workdir)

    log.info('running cmd: %s',cmd)

    subprocess.call(shlex.split('find {}'.format(workdir)))

    yadage_env = os.environ.copy()
    yadage_env['RECAST_JOBGUID'] = jogbuid
    if yaml.load(os.environ.get('RECAST_PLUGIN_TRACK','true')):
        yadage_env['YADAGE_CUSTOM_TRACKER'] = 'recastyadage.tracker:RECASTTracker'

    if 'RECAST_IN_DOCKER_WORKDIRS_VOL' in os.environ:
        #publish absolute path of this workdir for use by plugins
        workdirpath = '/'.join([os.environ['RECAST_IN_DOCKER_WORKDIRS_VOL'],workdir])
        yadage_env['PACKTIVITY_WORKDIR_LOCATION'] = '{}:{}'.format(os.path.abspath(workdir),workdirpath)
        log.info('plugin is running in Docker. set packtivity workdir as %s',yadage_env['PACKTIVITY_WORKDIR_LOCATION'])

    proc = subprocess.Popen(shlex.split(cmd),
                            env = yadage_env,
                            stderr = subprocess.STDOUT,
                            stdout = open('{}/fullyadage.log'.format(workdir),'w'))

    proc.communicate()
    log.info('workflow process terminated')
    if proc.returncode:
        log.error('workflow failed, raising error')
        raise RuntimeError('failed workflow process return code {}'.format(proc.returncode))
    log.info('workflow succeeded, recast plugin end.')