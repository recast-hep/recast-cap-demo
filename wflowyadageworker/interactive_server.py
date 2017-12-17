from flask import Flask, jsonify, request
import requests
import requests.exceptions
import time
import logging
import os
from yadagehttpctrl.yadagehttpserver import init_app


log = logging.getLogger('interactive_yadage')

import pkg_resources
import json
static_path = pkg_resources.resource_filename('wflowyadageworker', 'resources/server_static')
app = Flask('interactive_yadage',static_folder=static_path, static_url_path='/static')

@app.route('/ui')
def home():
    return app.send_static_file('ui.html')

@app.route('/readyz')
def readyz():
    return jsonify({})

@app.route('/finalize', methods=['POST'])
def finalize():
    data = request.json
    log.info('finalizing with %s', finalize)
    requests.post(
        'http://localhost:5000/status',
        headers = {'Content-Type':'application/json'},
        data = json.dumps(data['status'])
    )
    return jsonify({'confirm':data})

def main():
    logging.basicConfig(level = logging.INFO)
    while True:
        try:
            log.exception('getting context')
            r = requests.get('http://localhost:5000/context')
            print(r)
            app.config['context'] = r.json()
            break
        except requests.exceptions.ConnectionError:
            log.warning('failing to connect.. trying again')
        except requests.exceptions.Timeout:
            log.warning('timeout getting context.. trying again')
        except ValueError:
            log.exception('could not decode JSON... trying again')
        nseconds = 3
        log.info('sleeping for %s seconds until we try again', nseconds)
        time.sleep(nseconds)
    log.info('acquired context %s', app.config['context'])
    log.info('starting server')

    yadagestage = os.path.join(app.config['context']['workdir'],'_yadage','yadage_state.json')
    init_app(app, 'filebacked:{}'.format(yadagestage), {}, 'celery')
    app.run(host='0.0.0.0', port = 8888)

if __name__ == '__main__':
    main()
