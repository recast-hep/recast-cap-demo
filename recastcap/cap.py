import json
import pkg_resources
import os
import requests

HOST = 'http://pseudo-cap.herokuapp.com'

def api_getcall(endpoint):
    r = requests.get('{}/api/{}'.format(HOST,endpoint), auth = (os.environ['CAP_USER'],os.environ['CAP_ACCESSKEY']))
    if not r.ok:
        print r
        raise RuntimeError('call failed')

    return json.loads(r.content)['data']

def workflow(name):
    return api_getcall('workflow/{}'.format(name))

def step(name,stepname):
    return api_getcall('step/{}/{}'.format(name,stepname))

def node(node,nodename):
    return api_getcall('node/{}/{}'.format(node,nodename))
