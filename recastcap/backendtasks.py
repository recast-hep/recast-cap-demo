import logging
import subprocess
import time
import os
import shlex
import simple_workflow
import combined_workflow
import re

logging.basicConfig(level=logging.INFO)
log = logging.getLogger('RECAST')

def recast(ctx):
    log.info('running CAP analysis')

    workdir = 'workdirs/{}'.format(ctx['jobguid'])

    if 'combinedspec' in ctx:
        cmd = combined_workflow.workflow_command(ctx,workdir)
    else:
        cmd = simple_workflow.workflow_command(ctx,workdir)

    log.info('running cmd: %s',cmd)

    subprocess.call(shlex.split('find {}'.format(workdir)))

    yadage_env = env = os.environ.copy()
    if 'RECAST_IN_DOCKER_WORKDIRS_VOL' in os.environ:
        #publish absolute path of this workdir for use by plugins
        workdirpath = '/'.join([os.environ['RECAST_IN_DOCKER_WORKDIRS_VOL'],workdir])
        yadage_env['PACKTIVITY_WORKDIR_LOCATION'] = '{}:{}'.format(os.path.abspath(workdir),workdirpath)
        log.info('plugin is running in Docker. set packtivity workdir as %s',yadage_env['PACKTIVITY_WORKDIR_LOCATION'])

    proc = subprocess.Popen(shlex.split(cmd),
                            env = yadage_env,
                            stderr = subprocess.STDOUT,
                            stdout = subprocess.PIPE)

    filelogger = logging.getLogger('yadage_output')
    filelogger.setLevel(logging.DEBUG)
    fh = logging.FileHandler('{}/fullyadage.log'.format(workdir))
    fh.setLevel(logging.DEBUG)
    filelogger.addHandler(fh)
    filelogger.propagate = False

    while True:
        s = proc.stdout.readline().strip()
        if s:
            filelogger.debug(s)
            try:
                match = re.match('.* - adage - ([A-Za-z]*) - (.*)', s)
                if match and len(match.groups())==2:
                    level,rest = match.groups()
                    thelevel = getattr(logging,level)
                    for line in rest.splitlines():
                        log.log(thelevel,rest)
            except AttributeError:
                pass
        else:
            if proc.poll() is not None:
                break
        time.sleep(0.01)

    log.info('workflow process terminated task')
    if proc.returncode:
        log.error('workflow failed, raising error')
        raise RuntimeError('failed workflow process return code {}'.format(proc.returncode))
