import os
import logging
import redis
import json

class RedisHandler(logging.StreamHandler):
    def __init__(self,jobid,topic):
    	self.red = redis.StrictRedis(
    		host = os.environ.get('PACKTIVITY_LOGGER_HOST','localhost'),
    		port = os.environ.get('PACKTIVITY_LOGGER_PORT',6379),
    		db = os.environ.get('PACKTIVITY_LOGGER_DB',0)
    	)
    	self.jobid = jobid
    	self.topic = topic
        logging.StreamHandler.__init__(self)

    def emit(self, record):
    	msg = self.format(record)
    	data = {'jobguid': self.jobid, 'msg_type':'simple_log', 'msg':msg, 'topic': self.topic}
    	self.red.publish(os.environ.get('PACKTIVITY_LOGGER_CHANNEL','logstash:in'),json.dumps(data))

formatter = logging.Formatter('%(message)s')
def add_handlers(log,metadata,state,topic):
    fh = RedisHandler(metadata['name'],topic)
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    log.addHandler(fh)