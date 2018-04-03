import os
import socket
import redis
import redis.exceptions

import json
import logging

log = logging.getLogger(__name__)

class RedisHandler(logging.StreamHandler):
    def __init__(self,jobid,topic):
        self.red = redis.StrictRedis.from_url('PACKTIVITY_LOGGER_URL','redis://localhost')
    	self.jobid = jobid
    	self.topic = topic
        logging.StreamHandler.__init__(self)

    def emit(self, record):
    	msg = self.format(record)
    	data = {
            'jobguid': self.jobid,
            'msg_type':'simple_log',
            'msg':msg,
            'topic': self.topic,
            'host': socket.gethostname()
        }
        try:
        	self.red.publish(os.environ.get('PACKTIVITY_LOGGER_CHANNEL','logstash:in'),json.dumps(data))
        except redis.exceptions.ConnectionError:
            log.warning('publishing workflow state to redis failed')


formatter = logging.Formatter('%(message)s')
def add_handlers(log,metadata,state,topic):
    fh = RedisHandler(metadata['name'],topic)
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    log.addHandler(fh)
