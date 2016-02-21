import schedulers

handlers = {}
handlers['singlestep-from-context'] = schedulers.single_step_from_context
handlers['reduce-from-dep-output']  = schedulers.reduce_from_dep_output
handlers['map-from-dep-output']     = schedulers.map_from_dep_output