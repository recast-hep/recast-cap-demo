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
    'pyyaml',
    'jsonref',
    'adage',
    'yadage',
    'jsonschema'
  ],
  entry_points = {
  },
  dependency_links = [
      'https://github.com/lukasheinrich/yadage/tarball/master#egg=yadage-0.0.1',
      'https://github.com/lukasheinrich/adage/tarball/master#egg=adage-0.0.1'
  ]
)
