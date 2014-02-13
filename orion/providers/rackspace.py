#!/usr/bin/env python
# -*- coding: utf-8 -*-

from orion.base import ModuleBase

__all__ = [
    'CloudServer', 'CloudLoadBal', 'CloudLoadBalNodes', 'CloudDnsRecord',
    'CloudDns', 'CloudFilesContainer', 'CloudFilesObjects', 'CloudKeypair',
    'CloudFacts', 'CloudNetwork', 'CloudQueue'
]

class CloudBase(ModuleBase):
    def __init__(self,
                 api_key=None,
                 credentials=None,
                 region=None,
                 username=None
        ):
        super(CloudBase, self).__init__()
        self.r_api_key = api_key
        self.r_credentials = credentials
        self.r_region = region
        self.r_username = username

    def _make_dict(self):
        for prop, val in vars(self).items():
            try:
                split_ = prop.split('_')
                head = split_[0]
                key = "_".join(split_[1:])
            except IndexError:
                    continue
            else:
                if head == 'r' and val is not None:
                    self.module_args[key] = val
        self.module[self.module_name] = self.module_args


class CloudServer(CloudBase):
    def __init__(self, name, flavor, image,
                 display_name="Create Cloud Server(s)",
                 auto_increment=None,
                 count=None,
                 count_offset=None,
                 disk_config=None,
                 exact_count=True,
                 files=None,
                 group=None,
                 identity_type='rackspace',
                 instance_ids=None,
                 key_name=None,
                 meta=None,
                 networks=None,
                 region=None,
                 state=None,
                 wait=None,
                 wait_timeout=None,
                 **kwargs
        ):
        super(CloudServer, self).__init__(**kwargs) 
        self.display_name = display_name
        self.module_name = "rax"

        self.r_name = name or 'server'
        self.r_flavor = flavor
        self.r_image = image
        self.r_auto_increment = auto_increment
        self.r_count = count
        self.r_count_offset = count_offset
        self.r_disk_config = disk_config
        self.r_exact_count = exact_count
        self.r_files = files
        self.r_group = group
        self.r_identity_type = identity_type
        self.r_instance_ids = instance_ids
        self.r_key_name = key_name
        self.r_meta = meta
        self.r_networks = networks
        self.r_region = region
        self.r_state = state
        self.r_wait = wait
        self.r_wait_timeout = wait_timeout


class CloudLoadBal(CloudBase):
    def __init__(self, name,
                 display_name='Create Cloud Load Balancer',
                 algorithm=None,
                 meta=None,
                 port=None,
                 protocol=None,
                 state=None,
                 timeout=None,
                 type=None,
                 vip_id=None,
                 wait=None,
                 wait_timeout=None,
                 **kwargs
        ):
        super(CloudLoadBal, self).__init__(**kwargs) 
        self.display_name = display_name
        self.module_name = 'rax_clb'

        self.r_name = name or 'load-bal'
        self.r_algoritm = algorithm
        self.r_meta = meta
        self.r_port = port
        self.r_protocol = protocol
        self.r_state = state
        self.r_timeout = timeout
        self.r_type = type
        self.r_vip_id = vip_id
        self.r_wait = wait
        self.r_wait_timeout = wait_timeout


class CloudLoadBalNodes(CloudBase):
    def __init__(self, name, load_balancer_id,
                 display_name='Create Cloud Load Balancer Node(s)',
                 address=None,
                 condition=None,
                 node_id=None,
                 port=None,
                 state=None,
                 type=None,
                 virtualenv=None,
                 wait=None,
                 wait_timeout=None,
                 weight=None,
                 **kwargs
        ):
        super(CloudLoadBalNodes, self).__init__(**kwargs) 
        self.display_name = display_name
        self.module_name = 'rax_clb_nodes'

        self.r_name = name or 'node'
        self.r_load_balancer_id = load_balancer_id
        self.r_address = address
        self.r_condition = condition
        self.r_node_id = node_id
        self.r_port = port
        self.r_state = state
        self.r_type = type
        self.r_virtualenv = virtualenv
        self.r_wait = wait
        self.r_wait_timeout = wait_timeout
        self.r_weight = weight


class CloudDns(CloudBase):
    def __init__(self, domain_name,
                 display_name='Create Cloud DNS Domain',
                 comment=None,
                 email=None,
                 state=None,
                 ttl=None,
                 **kwargs
        ):
        super(CloudDns, self).__init__(**kwargs) 
        self.display_name = display_name
        self.module_name = 'rax_dns'

        self.r_name = domain_name
        self.r_comment = comment
        self.r_email = email
        self.r_state = state
        self.r_ttl = ttl


class CloudDnsRecord(CloudBase):
    def __init__(self, domain_name, fqdn, data,
                 display_name='Create Cloud DNS Record',
                 comment=None,
                 priority=None,
                 state=None,
                 ttl=None,
                 type_=None,
                 **kwargs
        ):
        super(CloudDnsRecord, self).__init__(**kwargs) 
        self.display_name = display_name
        self.module_name = 'rax_dns_record'

        self.r_domain = domain_name
        self.r_name = fqdn
        self.r_data = data
        self.r_comment = comment
        self.r_priority = priority
        self.r_state = state
        self.r_ttl = ttl
        self.r_type = type_


class CloudFilesContainer(CloudBase):
    def __init__(self, container,
                 display_name='Cloud Files container',
                 clear_meta=None,
                 meta=None,
                 private=None,
                 public=None,
                 ttl=None,
                 type_=None,
                 web_error=None,
                 web_index=None,
                 **kwargs
        ):
        super(CloudFilesContainer, self).__init__(**kwargs) 
        self.display_name = display_name
        self.module_name = 'rax_files'

        self.r_container = container
        self.r_clear_meta = clear_meta
        self.r_meta = meta
        self.r_private = private
        self.r_public = public
        self.r_ttl = ttl
        self.r_type = type_
        self.r_web_error = web_error
        self.r_web_index = web_index


class CloudFilesObjects(CloudBase):
    def __init__(self, container,
                 display_name='Cloud Files container objects',
                 clear_meta=None,
                 dest=None,
                 expires=None,
                 meta=None,
                 method=None,
                 src=None,
                 structure=None,
                 type_=None,
                 **kwargs
        ):
        super(CloudFilesObjects, self).__init__(**kwargs) 
        self.display_name = display_name
        self.module_name = 'rax_files_objects'

        self.r_container = container
        self.r_clear_meta = clear_meta
        self.r_dest = dest
        self.r_expires = expires
        self.r_meta = meta
        self.r_method = method
        self.r_src = src
        self.r_structure = structure
        self.r_type = type_


class CloudKeypair(CloudBase):
    def __init__(self, name,
                 display_name='Add Cloud Keypair',
                 public_key=None,
                 state=None,
                 **kwargs
        ):
        super(CloudQueue, self).__init__(**kwargs)
        self.display_name = display_name
        self.module_name = 'rax_keypair'

        self.r_name = name
        self.r_public_key = public_key
        self.r_state = state


class CloudNetwork(CloudBase):
    def __init__(self, label,
                 display_name='Add Cloud Network',
                 cidr=None,
                 state=None,
                 **kwargs
        ):
        super(CloudQueue, self).__init__(**kwargs)
        self.display_name = display_name
        self.module_name = 'rax_network'

        self.r_label = label
        self.r_cidr = cidr
        self.r_state = state


class CloudQueue(CloudBase):
    def __init__(self, name,
                 display_name='Create Cloud Queue',
                 state=None,
                 **kwargs
        ):
        super(CloudQueue, self).__init__(**kwargs)
        self.display_name = display_name
        self.module_name = 'rax_queue'

        self.r_name = name
        self.r_state = state


class CloudFacts(CloudBase):
    def __init__(self, display_name='Get Rackspace facts',
                 address=None,
                 id_=None,
                 name=None,
                 **kwargs
        ):
        super(CloudQueue, self).__init__(**kwargs)
        self.display_name = display_name
        self.r_address = address
        self.r_id = id_
        self.name = name
