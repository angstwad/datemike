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

servers = CloudServer(
    'webserver',
    'performance1-1',
    'ubuntu-1204-lts-precise-pangolin',
    credentials=CREDS,
    region='IAD',
    count=3,
    group='web'
)
add_host = CloudServersAddHosts('rax_servers')
loadbal = CloudLoadBal('loadbal1', credentials=CREDS, algorithm='ROUND_ROBIN')

task_servers = Task(servers, local_action=True, register='rax')
task_add_hosts = Task(add_host, local_action=True, with_items='rax.success')
task_loadbal = Task(loadbal, local_action=True)

play_cloud = Play('Create servers and load balancer')
# We can add a single task, or optionally, a list of tasks
play_cloud.add_task([task_servers, task_add_hosts, task_loadbal])
play_cloud.add_host('localhost')

# Provide a list of roles, or optionally, a single string.
roles = ['common', 'nginx', 'sites']

play_bootstrap = Play('Bootstrap servers')
play_bootstrap.add_role(roles)
play_bootstrap.add_host('webservers')

book = Playbook()
book.add_play(play_cloud)
book.add_play(play_bootstrap)

print book.to_yaml()

# Write to file locally
book.to_yaml_file('./launchservers.yml')
