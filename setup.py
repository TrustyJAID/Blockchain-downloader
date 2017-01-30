#!/usr/bin/env python
'''WikiLeaks Freedom Force presents the python blockchain downloader tool and library: wlffbd

This can be used to scan for and download data from the bitcoin blockchain.
Particularly, Wikileaks' known data formats are supported, but potentially more.'''
import re
import ast
from setuptools import setup, find_packages

_version_re = re.compile('__VERSION__\s+=\s+(.*)')

with open('wlffbd/__init__.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(f.read().decode('utf-8')).group(1)))

setup(name='wlffbd',
      description='WikiLeaks Freedom Force Blockchain Downlloader',
      long_description=__doc__,
      license='',
      keywords='wikileaks wiki leaks blockchain cryptography bitcoin',
      author='WikiLeaks Freedom Force',
      url='https://github.com/WikiLeaksFreedomForce',
      version=version,
      packages=find_packages(),
      zip_safe=True,
      platforms='Any',
      install_requires=['jsonrpclib-pelix'],
      entry_points='''
      [console_scripts]
      wlffbd=wlffbd.cli:wlffbd''')

      
