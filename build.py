#!/usr/bin/env python
'''Xnt build script for project'''

import xnt

@xnt.target
def build():
    xnt.setup(['build'])

@xnt.target
def clean():
    xnt.rm('pylibchorus.egg-info',
           'build',
           'dist',
           '.eggs',
           '**/__pycache__',
           '**/tests/__pycache__',
           '**/*.pyc',
           '**/tests/*.pyc')

@xnt.target
def test():
    return xnt.setup(['test'])

@xnt.target
def lint():
    return xnt.call(['pylint', '--rcfile=pylint.conf', 'pylibchorus'])

@xnt.target
def package():
    return xnt.setup(['bdist'])

@xnt.target
def install():
    return xnt.setup(['install', '--user'])
