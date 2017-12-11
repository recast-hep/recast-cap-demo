import json
import jq
import os
import wflowbackend.messaging
from yadage.utils import WithJsonRefEncoder
from adage.trackers import SimpleReportTracker

class EmitTracker(object):
    def __init__(self,jobguid):
        self.jobguid = jobguid
        self.tracker = SimpleReportTracker('WFLOWSERVICELOG',120)

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
        tosend = jq.jq('{dag: {nodes: [.dag.nodes[]|{state: .state, id: .id, name: .name, proxy: .proxy, task: {metadata: .task.metadata} }], edges: .dag.edges}}').transform(
            json.loads(serialized)
        )
        wflowbackend.messaging.emit(self.jobguid,'wflow_state',{'wflow_type': 'yadage', 'state': tosend})
