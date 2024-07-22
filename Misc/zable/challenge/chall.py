#!/usr/bin/env python3

from subprocess import Popen

name = input('Enter name: ')

for c in '`$(){}':
    name.replace(name, '')

Popen([
    'bazel',
    'run',
    ':run',
    f'--action_env=NAME={name}'
], shell=False).communicate()
