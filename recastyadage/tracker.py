import json
import jq
import os
import recastcelery.messaging
import logging
from yadage.helpers import WithJsonRefEncoder
from adage.trackers import SimpleReportTracker
class RECASTTracker(object):
    def __init__(self):
        self.jobguid = os.environ['RECAST_JOBGUID']
        self.log, self.handler = recastcelery.messaging.setupLogging(self.jobguid)
        self.tracker = SimpleReportTracker(self.log,120)
        
    def initialize(self,adageobj):
    	self.tracker.initialize(adageobj)
        self.send_state(adageobj)
        # self.track(adageobj)

    def track(self,adageobj):
    	self.tracker.track(adageobj)
        self.send_state(adageobj)

    def finalize(self,adageobj):
    	self.tracker.finalize(adageobj)
        self.send_state(adageobj)

    def send_state(self,adageobj):
        serialized = json.dumps(adageobj.json(), cls=WithJsonRefEncoder, sort_keys=True)
        tosend = jq.jq('{dag: {nodes: [.dag.nodes[]|{state: .state, id: .id, name: .name}], edges: .dag.edges}}').transform(
            json.loads(serialized)
        )
        recastcelery.messaging.generic_message(self.jobguid,'yadage_state',tosend)
    	
