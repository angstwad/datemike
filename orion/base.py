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


class ModuleBase(object):
    def __init__(self):
        """ Base class for module implementations
        Subclasses must implement the module_name and display_name attributes
        Module arguments must be prefaced with 'mod_' or will be ignored
        when building out the dict in _make_dict().
        This object can be wrapped in a Task class.
        This class' reason for existing is to assign arguments to an Ansible
        module, provide a Python representation of the module/args, and to dump
        the YAML representation of the object.

        """
        self.module = dict()
        self.module_args = dict()
        self.module_name = None
        self.display_name = None

    def __str__(self):
        """ String of ModuleBase
        :return: A pretty-formatted YAML representation of the module
        """
        return pretty_yaml(self.module)

    def _make_dict(self):
        """ Constructs the module dictionary from attributes defined on the
        object, but only adds arguments for the module if attributes are
        prefaced with 'mod_'.
        """
        for prop, val in vars(self).items():
            try:
                split_ = prop.split('_')
                head = split_[0]
                key = "_".join(split_[1:])
            except IndexError:
                    continue
            else:
                if head == 'mod' and val is not None:
                    self.module_args[key] = val
        self.module[self.module_name] = self.module_args

    def as_dict(self):
        """ Representation of the constructed module as a dict
        :return: dict
        """
        if not self.module:
            self._make_dict()
        return self.module

    def to_yaml(self):
        """ Representation of the constructed module as YAML string
        :return: str
        """
        if not self.module:
            self._make_dict()
        return pretty_yaml(self.module)
