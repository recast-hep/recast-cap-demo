import json
import pkg_resources
def load_spec(spec):
  path = pkg_resources.resource_filename('recastcap','capdata/{}.json'.format(spec))
  with open(path) as f:
    return json.load(f)