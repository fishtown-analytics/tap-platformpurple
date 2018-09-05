#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='tap-platformpurple',
      version='0.0.2',
      description='Singer.io tap for extracting data from the LogMeIn Rescue API',
      author='Fishtown Analytics',
      url='http://fishtownanalytics.com',
      classifiers=['Programming Language :: Python :: 3 :: Only'],
      py_modules=['tap_platformpurple'],
      install_requires=[
          'tap-framework==0.0.4',
      ],
      entry_points='''
          [console_scripts]
          tap-platformpurple=tap_platformpurple:main
      ''',
      packages=find_packages(),
      package_data={
          'tap_platformpurple': [
              'schemas/*.json'
          ]
      })