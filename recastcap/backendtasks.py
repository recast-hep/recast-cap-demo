import logging
import subprocess
import time
import os
import shlex

logging.basicConfig(level=logging.INFO)
log = logging.getLogger('RECAST')

def recast(ctx):
    log.info('running CAP analysis')
    workdir = 'workdirs/{}'.format(ctx['jobguid'])
    yadagectx = '{}/inputs/input.yaml'.format(workdir)
    
    if not os.path.exists(workdir):
        log.error('workdirectory: %s does not exist',workdir)
    
    if not os.path.exists(yadagectx):
        log.error('context file: %s does not exist',yadagectx)
    
    yadage_env = env = os.environ.copy()
    
    if 'RECAST_IN_DOCKER_WORKDIRS_VOL' in os.environ:
        #publish absolute path of this workdir for use by plugins
        yadage_env['PACKTIVITY_WORKDIR_LOCATION']='/'.join([os.environ['RECAST_IN_DOCKER_WORKDIRS_VOL'],workdir])
        log.info('plugin is running in Docker. set packtivity workdir as %s',yadage_env['PACKTIVITY_WORKDIR_LOCATION'])
          
    cmd = 'yadage-run -t from-github {workdir} {workflow} {context}'.format(
        workdir = workdir,
        workflow = ctx['workflow'],
        context  = yadagectx
    )
     
    log.info('running cmd: %s',cmd)
    
    subprocess.call(shlex.split('find {}'.format(workdir)))
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
    
    while proc.poll() is None:
        s = proc.stdout.readline().strip()
        filelogger.debug(s)
        try:
            splitup = s.split(':',1)
            if len(splitup)==2:
                level,rest = splitup
                thelevel = getattr(logging,level)
                for line in rest.splitlines():
                    if 'adage' in line or thelevel>logging.INFO:
                        log.log(thelevel,rest)
        except AttributeError:
            pass
        time.sleep(0.01)
    
    log.info('workflow process terminated task')
    if proc.returncode:
        log.error('workflow failed, raising error')
        raise RuntimeError('failed workflow process return code {}'.format(proc.returncode))
    