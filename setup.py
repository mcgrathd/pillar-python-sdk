# -*- coding: utf-8 -*-
from distutils.core import setup

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'attractsdk'))
from config import __version__, __pypi_packagename__, __github_username__, __github_reponame__

long_description="""
    The Attract REST SDK provides Python APIs to communicate to the Attract webservices.
  """

# license='Free BSD'
# if os.path.exists('LICENSE.md'):
#   license = open('LICENSE.md').read()

url='https://github.com/' + __github_username__ + '/' + __github_reponame__

setup(
  name=__pypi_packagename__,
  version= __version__,
  author='Francesco Siddi, PayPal',
  author_email='francesco@blender.org',
  packages=['attractsdk'],
  scripts=[],
  url=url,
  license='BSD License',
  description='The Attract REST SDK provides Python APIs to communicate to the Attract webservices.',
  long_description=long_description,
  install_requires=['requests>=1.0.0', 'six>=1.0.0', 'pyopenssl>=0.14'],
  classifiers=[
    'Intended Audience :: Developers',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Topic :: Software Development :: Libraries :: Python Modules'
  ],
  keywords=['attract', 'rest', 'sdk', 'tracking', 'film', 'production']
)
