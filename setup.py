#!/usr/bin/env python

from setuptools import setup

setup(name='SeekWell',
      version='0.1',
      description='SQL for Data Analysts',
      author='Mat Leonard',
      author_email='leonard.mat@gmail.com',
      url='https://github.com/mcleonard/seekwell',
      packages=['seekwell'],
      license='LICENSE.txt',
      requires=[
          'sqlalchemy',
          'terminaltables'
      ]
     )