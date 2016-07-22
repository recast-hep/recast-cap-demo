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

    log.info('running recast workflow on context {}'.format(ctx))

    if not os.path.exists(workdir):
        log.error('workdirectory: %s does not exist',workdir)

    if not os.path.exists(yadagectx):
        log.error('context file: %s does not exist',yadagectx)

    yadage_env = env = os.environ.copy()

    if 'RECAST_IN_DOCKER_WORKDIRS_VOL' in os.environ:
        #publish absolute path of this workdir for use by plugins
        workdirpath = '/'.join([os.environ['RECAST_IN_DOCKER_WORKDIRS_VOL'],workdir])
        yadage_env['PACKTIVITY_WORKDIR_LOCATION'] = '{}:{}'.format(os.path.abspath(workdir),workdirpath)
        log.info('plugin is running in Docker. set packtivity workdir as %s',yadage_env['PACKTIVITY_WORKDIR_LOCATION'])

    cmd = 'yadage-run -b {backend} -t {toplevel} {workdir} {workflow} {context}'.format(
        workdir = workdir,
        backend = os.environ.get('RECAST_YADAGEBACKEND','multiproc:2'),
        workflow = ctx['workflow'],
        context  = yadagectx,
        toplevel = ctx.get('toplevel','from-github/pseudocap')
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

    while True:

        s = proc.stdout.readline().strip()
        if s:
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
        else:
            if proc.poll() is not None:
                break
        time.sleep(0.01)

    log.info('workflow process terminated task')
    if proc.returncode:
        log.error('workflow failed, raising error')
        raise RuntimeError('failed workflow process return code {}'.format(proc.returncode))
