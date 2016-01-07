#!/usr/bin/env python

from setuptools import setup

setup(name='sagescrape',
      version='0.1',
      description='sacrape Sage GmbH webapplications, especially DPW',
      url='http://github.com/ebirn/sagescrape',
      author='Erich Birngruber',
      author_email='ebirn@outdated.at',
      license='MIT',
      packages=['sagescrape'],
      install_requires=[
          'ConfigParser',
          'datetime',
          'selenium',
      ],
      zip_safe=False)


