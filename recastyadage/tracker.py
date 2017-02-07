import json
import os
import recastcelery.messaging
import logging
from yadage.helpers import WithJsonRefEncoder
from adage.trackers import SimpleReportTracker
class RECASTTracker(object):
    def __init__(self):
        self.jobguid = os.environ['RECAST_JOBGUID']
        self.log, self.handler = recastcelery.messaging.setupLogging(self.jobguid)
        self.tracker = SimpleReportTracker(self.log,30)

    def initialize(self,adageobj):
    	self.tracker.initialize(adageobj)
        # self.track(adageobj)

    def track(self,adageobj):
    	self.tracker.track(adageobj)
        # serialized = json.dumps(adageobj.json(), cls=WithJsonRefEncoder, sort_keys=True)
        # recastcelery.messaging.socketlog(self.jobguid,'noop tracking for now.. but still alive')
        # recastcelery.messaging.generic_message(self.jobguid,'yadage_state',json.loads(serialized))

    def finalize(self,adageobj):
    	self.tracker.finalize(adageobj)
        # self.track(adageobj)

