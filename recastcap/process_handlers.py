handlers = {}

def stringinterp_handler(process_spec,attributes):
    return process_spec['cmd'].format(**attributes)

handlers['string-interpolated-cmd'] = stringinterp_handler