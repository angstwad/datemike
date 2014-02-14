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

import os
from collections import OrderedDict

from orion.utils import pretty_yaml


class Task(object):
    def __init__(self, module, local_action=False, **kwargs):
        """ A task wraps a module object following the Ansible
        Task < Play < Playbook hierarchy

        :param module: ModuleBase derivative
        :param local_action: Sets task local_action if True
        :param kwargs: Task-level arguments as defined by Ansible, i.e. sudo,
        su, sudo_pass, etc.
        """
        self.module = module
        self.task_args = kwargs
        self.local_action = local_action
        self.task = OrderedDict(name=module.display_name)
        self.task.update(kwargs)
        if local_action:
            module_name = module.as_obj().keys()[0]
            new_module = OrderedDict(module=module_name)
            new_module.update(module.as_obj()[module_name])
            self.task['local_action'] = new_module
        else:
            self.task.update(module.as_obj())

    def __str__(self):
        return self.to_yaml()

    def init_task(self):
        if self.local_action:
            self.task['local_action'] = self.module.as_obj()
        if self.task_args:
            self.task.update(self.task_args)

    def as_obj(self):
        return self.task

    def to_yaml(self):
        return pretty_yaml(self.task)


class Play(object):
    def __init__(self, name, **kwargs):
        """ A play consists of a task or several tasks, following the Ansible
        Task < Play < Playbook hierarchy

        :param name:
        :param kwargs:
        """
        self.play_args = kwargs
        self.play = OrderedDict(name=name)
        self.play.update(kwargs)

    def __str__(self):
        return self.to_yaml()

    def add_task(self, task):
        """ Add a task to this play

        :param task: Task as an object
        """
        if not self.play.get('tasks'):
            self.play['tasks'] = []
        if isinstance(task, Task):
            self.play['tasks'].append(task.as_obj())
        elif isinstance(task, list):
            lst = [t.as_obj() for t in task]
            self.play['tasks'].extend(lst)

    def add_host(self, host):
        """ Add host(s) to this play

        :param host: A host as a string or hosts as a list of strings
        """
        if not self.play.get('hosts'):
            self.play['hosts'] = []
        if isinstance(host, str):
            self.play['hosts'].append(host)
        elif isinstance(host, list):
            self.play['hosts'].extend(host)

    def add_role(self, role):
        """ Add role(s) to this play

        :param role: A role as a string or roles as a list of strings
        """
        if not self.play.get('roles'):
            self.play['roles'] = []
        if isinstance(role, str):
            self.play['roles'].append(role)
        elif isinstance(role, list):
            self.play['roles'].extend(role)

    def as_obj(self):
        """ Get the object representation of a play

        :return: dict
        """
        return self.play

    def to_yaml(self):
        """ Get the YAML representation of a play

        :return: str
        """
        return pretty_yaml(self.play)


class Playbook(object):
    def __init__(self):
        """ A playbook is a list of Ansible Plays, following the Ansible
        Task < Play < Playbook hierarchy.
        """
        self.playbook = []

    def __str__(self):
        return self.to_yaml()

    def add_play(self, play):
        """ Add a play to this playbook

        :param play: Play object or list of play objects
        """
        if isinstance(play, Play):
            self.playbook.append(play.as_obj())
        elif isinstance(play, list):
            lst = [p.as_obj() for p in play]
            self.playbook.extend(lst)

    def as_obj(self):
        """ Get the object representation of this playbook

        :return: list
        """
        return self.playbook

    def to_yaml(self):
        """ Get the YAML representation of this playbook

        :return: str
        """
        return pretty_yaml(self.playbook)

    def to_yaml_file(self, filepath):
        """ Write this playbook to disk

        :param filepath: Filepath as a string
        """
        filepath = os.path.abspath(os.path.expanduser(filepath))
        with open(filepath, 'w') as f:
            pretty_yaml(self.playbook, f)
