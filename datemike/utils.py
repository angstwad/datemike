#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of datemike: https://github.com/angstwad/datemike
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

import yaml
from collections import OrderedDict


def order_rep(dumper, data):
    """ YAML Dumper to represent OrderedDict """
    return dumper.represent_mapping(u'tag:yaml.org,2002:map', data.items(),
                                    flow_style=False)

# Adds a representation for OrderedDicts
yaml.add_representer(OrderedDict, order_rep)


def pretty_yaml(value, file_=None):
    """ Print an object to a YAML string

    :param value: object to dump
    :param file_: Open, writable file object
    :return: str (YAML)
    """
    return yaml.dump(value, stream=file_, indent=2, allow_unicode=True,
                     default_flow_style=False)
