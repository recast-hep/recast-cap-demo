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
  
  
    if 'RECAST_IN_DOCKER_WORKDIR' in os.environ:
        os.environ['PACKTIVITY_WORKDIR_LOCATION']=os.environ['RECAST_IN_DOCKER_WORKDIR']
        
    cmd = 'yadage-run -t from-github {workdir} {workflow} {context}'.format(
        workdir = workdir,
        workflow = ctx['workflow'],
        context  = yadagectx
    )
     
    log.info('running cmd: %s',cmd)
    
    subprocess.call(shlex.split('find {}'.format(workdir)))
    proc = subprocess.Popen(shlex.split(cmd), stderr = subprocess.STDOUT, stdout = subprocess.PIPE)
    
    while proc.poll() is None:
        s = proc.stdout.readline()
        try:
            splitup = s.strip().split(':',1)
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
