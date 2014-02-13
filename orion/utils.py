#!/usr/bin/env python
# -*- coding: utf-8 -*-

import yaml


def pretty_yaml(value):
    return yaml.safe_dump(value, indent=2, allow_unicode=True, default_flow_style=False)
