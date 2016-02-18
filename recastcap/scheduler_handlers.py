import schedulers

handlers = {}
handlers['singlenode-from-context'] = schedulers.single_node_from_context
handlers['reduce-from-dep-output']  = schedulers.reduce_from_dep_output