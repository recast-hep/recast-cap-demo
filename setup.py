from setuptools import setup, find_packages

setup(
  name = 'recast-yadage-plugin',
  version = '0.0.1',
  description = 'recast-yadage-plugin',
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
    'pyyaml'
  ],
  entry_points = {
  },
  dependency_links = [
  ]
)
