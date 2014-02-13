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

from orion.utils import pretty_yaml


class Task(object):
    def __init__(self, module, local_action=True, **kwargs):
        self.module = module
        self.task_args = kwargs
        self.local_action = local_action
        self.task = {
            'name': module.display_name,
        }
        self.task.update(kwargs)
        if local_action:
            self.task['local_action'] = module.as_dict()
        else:
            self.task.update(module.as_dict())

    def __str__(self):
        return self.to_yaml()

    def init_task(self):
        if self.local_action:
            self.task['local_action'] = self.module.as_dict()
        if self.task_args:
            self.task.update(self.task_args)

    def as_dict(self):
        return self.task

    def to_yaml(self):
        return pretty_yaml(self.task)


class Play(object):
    def __init__(self, name, **kwargs):
        self.play_args = kwargs
        self.play = {
            'name': name
        }
        self.play.update(kwargs)

    def __str__(self):
        return self.to_yaml()

    def add_task(self, task):
        if not self.play.get('tasks'):
            self.play['tasks'] = []
        self.play['tasks'].append(task.as_dict())

    def add_host(self, host):
        if not self.play.get('hosts'):
            self.play['hosts'] = []
        if isinstance(host, str):
            self.play['hosts'].append(host)
        elif isinstance(host, list):
            self.play['hosts'].extend(host)

    def add_role(self, role):
        if not self.play.get('roles'):
            self.play['roles'] = []
        if isinstance(role, str):
            self.play['roles'].append(role)
        elif isinstance(role, list):
            self.play['roles'].extend(role)

    def as_dict(self):
        return self.play

    def to_yaml(self):
        return pretty_yaml(self.play)


class Playbook(object):
    def __init__(self, name, **kwargs):
        self.playbook = {
            'name': name
        }
        self.playbook.update(kwargs)

    def __str__(self):
        return self.to_yaml()

    def add_play(self, play):
        if not self.playbook.get('plays'):
            self.play['plays'] = []
        self.play['tasks'].append(play.as_dict())

    def as_dict(self):
        return self.playbook

    def to_yaml(self):
        return pretty_yaml(self.playbook)
