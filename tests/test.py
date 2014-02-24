#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collections import OrderedDict

import unittest
import yaml

from datemike import ansible, base, utils
from datemike.providers import rackspace

desired_yaml = """name: Create Cloud Server(s)
rax:
  exact_count: true
  flavor: performance1-1
  image: image-ubuntu-1204
  name: servername
"""

desired_obj = OrderedDict(
    [
        ('name', 'Create Cloud Server(s)'),
        (
            'rax', {
                'image': 'image-ubuntu-1204',
                'name': 'servername',
                'flavor': 'performance1-1',
                'exact_count': True
            }
        )
    ]
)


class TestAnsible(unittest.TestCase):
    def setUp(self):
        self.server = rackspace.CloudServer(
            'servername', 'performance1-1', 'image-ubuntu-1204'
        )
        self.task = ansible.Task(self.server)
        self.play = ansible.Play('')

    def tearDown(self):
        pass

    def test_task_localaction(self):
        task = ansible.Task(self.server, local_action=True)
        yamlobj = yaml.load(task.to_yaml())
        self.assertIn('local_action', yamlobj.keys(),
                      'local_action not in the parsed YAML object!')

    def test_task_localaction_module(self):
        task = ansible.Task(self.server, local_action=True)
        yamlobj = yaml.load(task.to_yaml())
        module = yamlobj.get('local_action')
        self.assertEqual(module.get('module'), 'rax',
                         'value of module not rax')
        self.assertEqual(module.get('image'), 'image-ubuntu-1204',
                         'value of image not image-ubuntu-1204')
        self.assertEqual(module.get('flavor'), 'performance1-1',
                         'value of flavor not performance1-1')

    def test_task(self):
        yamlobj = yaml.load(self.task.to_yaml())
        self.assertNotIn('local_action', yamlobj.keys())

    def test_task_module(self):
        module = yaml.load(self.task.to_yaml())
        self.assertIn('rax', module.keys())
        rax = module.get('rax')
        self.assertEqual(rax.get('image'), 'image-ubuntu-1204',
                         'value of image not image-ubuntu-1204')
        self.assertEqual(rax.get('flavor'), 'performance1-1',
                         'value of flavor not performance1-1')

    def test_task_to_yaml(self):
        task_yaml = self.task.to_yaml()
        self.assertEqual(desired_yaml, task_yaml,
                         'Task YAML and expected YAML are not equal.')

    def test_task_as_str(self):
        task_yaml =  self.task.to_yaml()
        self.assertEqual(desired_yaml, str(self.task))

    def test_task_as_obj(self):
        task_obj = self.task.as_obj()
        self.assertEqual(desired_obj, task_obj,
                         'Task object and expected object are not the equal.')




def main():
    TestAnsible.run()

if __name__ == '__main__':
    main()
