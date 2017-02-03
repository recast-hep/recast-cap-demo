import json
import os
import recastcelery.messaging
from yadage.helpers import WithJsonRefEncoder

class RECASTTracker(object):
    def __init__(self):
	   self.jobguid = os.environ['RECAST_JOBGUID']

    def initialize(self,adageobj):
        self.track(adageobj)

    def track(self,adageobj):
        serialized = json.dumps(adageobj.json(), cls=WithJsonRefEncoder, sort_keys=True)
        recastcelery.messaging.generic_message(self.jobguid,'yadage_state',json.loads(serialized))

    def finalize(self,adageobj):
        self.track(adageobj)

