#!/usr/bin/env python
"""
ADSPipelineMsg
-------------
Interpipeline communication messages
"""
import os
from subprocess import Popen, PIPE

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

with open('requirements.txt') as f:
    required = f.read().splitlines()

with open('dev-requirements.txt') as f:
    dev_required = f.read().splitlines()

def get_git_version(default="v0.0.1"):
    try:
        p = Popen(['git', 'describe', '--tags'], stdout=PIPE, stderr=PIPE)
        p.stderr.close()
        line = p.stdout.readlines()[0]
        line = line.strip()
        return line.decode()
    except:
        return default

setup(
    name='adsmsg',
    version=get_git_version(default="v0.0.1"),
    url='http://github.com/adsabs/flask-discoverer/',
    license='MIT',
    author='NASA/SAO ADS',
    description='Interpipeline communication messages',
    long_description=__doc__,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=required,
    test_suite='adsmsg/tests',
    tests_require = dev_required,
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
