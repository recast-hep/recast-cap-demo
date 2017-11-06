from setuptools import setup, find_packages

setup(
  name = 'wflow-yadage-worker',
  version = '0.0.3',
  description = 'wflow-yadage-worker',
  url = '',
  author = 'Lukas Heinrich',
  author_email = 'lukas.heinrich@cern.ch',
  packages = find_packages(),
  include_package_data = True,
  install_requires = [
    'click',
    'psutil',
    'requests[security]>2.9',
    'pyyaml',
    'jsonref',
    'yadage',
    'jsonschema',
    'pyyaml',
    'jq',
  ],
  entry_points = {
  },
  dependency_links = [
  ]
)
