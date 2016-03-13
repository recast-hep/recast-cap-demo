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
  
    cmd = 'yadage-run -t from-github {workdir} {analysis} {context}'.format(
        workdir = workdir,
        analysis = ctx['analysis'],
        context  = yadagectx
    )
     
    log.info('running cmd: {}'.format(cmd))
    
    proc = subprocess.Popen(shlex.split(cmd), stderr = subprocess.STDOUT, stdout = subprocess.PIPE)
    
    while proc.poll() is None:
        s = proc.stdout.readline()
        print s.strip()
        try:
            splitup = s.strip().split(':',1)
            if len(splitup)==2:
                for line in splitup[1].splitlines():
                    if 'adage' in line:
                        log.log(getattr(logging,splitup[0]),line)
            # log.log(getattr(logging,splitup[0]),line)
        except AttributeError:
            pass
        time.sleep(0.01)
      
    log.info('workflow process terminated task')
    if proc.returncode:
        log.error('workflow failed, raising error')
        raise RuntimeError('failed workflow process return code {}'.format(proc.returncode))