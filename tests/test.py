#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collections import OrderedDict

import unittest
import yaml

from datemike import ansible, base, utils
from datemike.providers import rackspace

desired_task_yaml = """name: Create Cloud Server(s)
rax:
  exact_count: true
  flavor: performance1-1
  image: image-ubuntu-1204
  name: servername
"""

desired_play_yaml = """name: TestPlay
tasks:
- name: Create Cloud Server(s)
  rax:
    exact_count: true
    flavor: performance1-1
    image: image-ubuntu-1204
    name: servername
"""

desired_playbook_yaml = """- name: TestPlay
  tasks:
  - name: Create Cloud Server(s)
    rax:
      exact_count: true
      flavor: performance1-1
      image: image-ubuntu-1204
      name: servername
"""

desired_task_obj = OrderedDict(
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

    def tearDown(self):
        pass

    def setup_play(self):
        play = ansible.Play('TestPlay')
        play.add_task(self.task)
        return play

    def setup_playbook(self):
        play = self.setup_play()
        book = ansible.Playbook()
        return play, book

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
        self.assertEqual(desired_task_yaml, task_yaml,
                         'Task YAML and expected YAML are not equal.')

    def test_task_as_str(self):
        task_yaml = self.task.to_yaml()
        self.assertEqual(desired_task_yaml, str(task_yaml))

    def test_task_as_obj(self):
        task_obj = self.task.as_obj()
        self.assertEqual(desired_task_obj, task_obj,
                         'Task object and expected object are not the equal.')

    def test_play(self):
        play = ansible.Play('TestPlay')
        self.assertEqual(play.play.get('name'), 'TestPlay',
                         'Play name not equal to TestPlay')

    def test_play_add_task(self):
        play = self.setup_play()
        self.assertEqual(play.play.get('tasks')[0], self.task.as_obj(),
                         'Task not at expected index in play object')

    def test_play_add_tasks(self):
        play = self.setup_play()
        task = ansible.Task(self.server, local_action=True)
        play.add_task([self.task, task])
        self.assertEqual(play.play.get('tasks', [])[0], self.task.as_obj(),
                         'Play task index 0 does not match self.task')
        self.assertNotEqual(play.play.get('tasks')[1], task.as_obj(),
                            'Play task index 1 shouldn\' match local task')

    def test_play_add_host(self):
        play = ansible.Play('TestPlay')
        play.add_host('testhost')
        self.assertIn('testhost', play.as_obj().get('hosts'),
                      'testhosts not in play hosts')

    def test_play_add_role(self):
        play = ansible.Play('TestPlay')
        play.add_role('testrole')
        self.assertIn('testrole', play.as_obj().get('roles'),
                      'testrole not in play roles')

    def test_play_yaml(self):
        play = self.setup_play()
        self.assertEqual(desired_play_yaml, play.to_yaml(),
                         'Play YAML does not equal expected YAML')

    def test_playbook_add_play(self):
        play, book = self.setup_playbook()
        book.add_play(play)
        self.assertEquals(book.playbook[0], play.as_obj(),
                          'play does not equal playbook play at index 0')

    def test_playbook_add_plays(self):
        play, book = self.setup_playbook()
        play2 = self.setup_play()
        book.add_play([play, play2])
        self.assertEqual(len(book.playbook), 2,
                         'length of plays in playbook is not equal to 2')

    def test_playbook_yaml(self):
        play, book = self.setup_playbook()
        book.add_play(play)
        self.assertEqual(desired_playbook_yaml, book.to_yaml(),
                         'Playbook YAML output does not match intended YAML')


def main():
    TestAnsible.run()

if __name__ == '__main__':
    main()
