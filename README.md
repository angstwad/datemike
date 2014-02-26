# Date Mike

[![Build Status](https://drone.io/github.com/angstwad/datemike/status.png)](https://drone.io/github.com/angstwad/datemike/latest)

![Imgur](http://i.imgur.com/p2GywkM.png)

A library to create Ansible tasks, plays, and playbooks in Python.

## Examples
Please note that the following is an overly-simplified example for a quick demo only.  Please see the `examples` dir for a full example.  This builds a single play that builds a single Rackspace server.

```
from datemike import Task, Play, Playbook
from datemike.providers.rackspace import CloudServer


servers = CloudServer('webserver', 'performance1-1', 
                      'ubuntu-1204-lts-precise-pangolin')

task_servers = Task(servers, local_action=True, register='rax')

play = Play('Launch a single server in Rackspace')
play.add_task(task_servers)
play.add_host('localhost')

print play.to_yaml()
```
This results in the following:
```
name: Launch a single server in Rackspace
tasks:
- name: Create Cloud Server(s)
  register: rax
  local_action:
    module: rax
    image: ubuntu-1204-lts-precise-pangolin
    name: webserver
    flavor: performance1-1
    exact_count: true
hosts:
- localhost
```

The `Play` and `Playbook` have a `to_yaml` method that will dump the object as an Ansible-compatible YAML data structure.


## Extending

If adding your own modules to `providers`, subclass the included base class `datemike.base.ModuleBase`.  `ModuleBase` makes some assumptions, primarily that any object attribute name must begin with mod_ in order for it to be passed along as a module argument once wrapped in a task.  `ModuleBase` provides some methods for you, such as returning the resulting module object as a native Python data structure (`as_obj`) and dumping the module to YAML (`to_yaml`).

## Use

datemike follows the Ansible object hierarchy.  Modules are used to create tasks (and therefore `Task` objects can wrap modules).  `Tasks` are added to `Plays`, and `Plays` are added to `Playbooks`.  Most importatantly, it's not the purpose of datemike to attempt to create a python representation of each and every Ansible module in existence.  Instead, anywhere modules are needed to programmatically be created by a 3rd party application is where a module object should be added to datemike.

In the `datemike/providers` directory, I have `rackspace.py` representing all the available rax* modules in Ansible.  Again, I don't want a representation of *all* the Ansible modules, only Rackspace.  That's because I fully intend to programmatically instantiate them, wrap them in a task, and create full plays and playbooks orchestrating the construction Rackspace cloud enviroment.  However, all subsequent configuration management will not be done programmatically, but rather via the roles mechanism.  Therefore, there's no need to programmatically interact (or write) classes for Modules -- we'll attach our roles to plays via the `Play.add_role()` method.

## Why?

##### The YAML syntax is already so simple.  Why did I need you complicate things?
That's right, the sytax was simple and this isn't a trivial library.  There was no existing way to programatically create Ansible-valid YAML.  In order to create a web-based Ansible configurator, a library like this needed to exist.

### I should admit…

I should admit that this module is of really limited use, and takes a lot of work to properly implement a modules interface in order to output proper YAML.  In it's current form, it requires that you create a class for every module.  In the future, perhaps it's possible to parse every module in the Ansible library (using the docstrings) for arguments, and then use some of the `module_utils` to get our data into a normalized data structure.  Let's see how it goes… 

## License

Apache v2.0 License


