#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of Orion: https://github.com/angstwad/orion
#
# Copyright 2014 Paul Durivage
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from orion import Task, Play, Playbook
from orion.providers.rackspace import *

CREDS = '~/.rackspace_cloud_credentials'

# Instantiate a Cloud Server module object
servers = CloudServer(
    'webserver',
    'performance1-1',
    'ubuntu-1204-lts-precise-pangolin',
    credentials=CREDS,
    region='IAD',
    count=3,
    group='web'
)
# Instantiate the helper module to add rax servers into a hosts group
add_host = CloudServersAddHosts('rax_servers')
# And create a cloud load balancer
loadbal = CloudLoadBal('loadbal1', credentials=CREDS, algorithm='ROUND_ROBIN')

# Create a task for each server, passing task-level keyword args
# directly into the Task constructor
task_servers = Task(servers, local_action=True, register='rax')
task_add_hosts = Task(add_host, local_action=True, with_items='rax.success')
task_loadbal = Task(loadbal, local_action=True)

# Instantiate a Play
play_cloud = Play('Create servers and load balancer')
# We can add a single task, or optionally, a list of tasks
play_cloud.add_task([task_servers, task_add_hosts, task_loadbal])
# And add hosts to the play
play_cloud.add_host('localhost')

# Provide a list of roles, or optionally, a single string.
roles = ['common', 'nginx', 'sites']

# Instantiate a new play
play_bootstrap = Play('Bootstrap servers')
# Add a group of roles to this play
play_bootstrap.add_role(roles)
# ...and add hosts
play_bootstrap.add_host('webservers')

# Instantiate a playbook
book = Playbook()
# And add our plays to the playbook
book.add_play(play_cloud)
book.add_play(play_bootstrap)

print book.to_yaml()

# Write to file locally
book.to_yaml_file('./launchservers.yml')
