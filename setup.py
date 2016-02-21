from setuptools import setup, find_packages

setup(
  name = 'recast-cap-demo',
  version = '0.0.1',
  description = 'recast-cap-demo',
  url = '',
  author = 'Lukas Heinrich',
  author_email = 'lukas.heinrich@cern.ch',
  packages = find_packages(),
  include_package_data = True,
  install_requires = [
    'adage',
    'click',
    'psutil',
    'requests',
    'pyyaml'
    'jsonref',
    'jsonschema'
  ],
  entry_points = {
      'console_scripts': ['recastworkflow-capsteer=recastcap.steering:main'],
  },
  dependency_links = [
  ]
)
