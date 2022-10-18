import json
import sys

'''
Generates a dict which is simply usable in interface configuration templates
input:
    inets:
          - inet 10.1.2.3 netmask 255.255.255.0
          - - 'inet 10.1.3.2 netmask 255.255.255.0'
            - 'inet vhid 11 pass secret advskew 1 alias 10.1.3.1/24'
          - ifname: epair1b
            ifconf: '10.1.4.2 netmask 255.255.255.0'
          - ifname: epair1b_alias0
            ifconf: 'inet vhid 10 pass secret advskew 1 alias 10.1.4.1/24'
    hostname: 'foo'

output: 
    - ifname: e0b_foo
      ifconf: inet 10.1.2.3 netmask 255.255.255.0
    - ifname: e1b_foo
      ifconf: inet 10.1.3.2 netmask 255.255.255.0
    - ifname: e1b_foo_alias0
      ifconf: inet vhid 11 pass secret advskew 1 alias 10.1.3.1/24
    - ifname: epair1b
      ifconf: '10.1.4.2 netmask 255.255.255.0'
    - ifname: epair1b_alias0
      ifconf: 'inet vhid 10 pass secret advskew 1 alias 10.1.4.1/24'

'''

def jail_net_conf (inets, hostname):
    ret = []
    ifindex = 0
    for inet in inets:
        if isinstance(inet, str):
            ret.append(dict( ifname = f'e{ ifindex }b_{ hostname }', ifconf = inet))
        elif isinstance(inet, list):
            ret.append(dict( ifname = f'e{ ifindex }b_{ hostname }', ifconf = inet[0]))
            aliasindex = 0
            for alias in inet[1:]:
                ret.append(dict( ifname = f'e{ ifindex }b_{ hostname }_alias{ aliasindex }', ifconf = alias))
                aliasindex += 1
        elif isinstance(inet, dict):
            ret.append(inet)
            continue
        ifindex += 1
    return ret

class FilterModule(object):
    '''
    Ansible filter to format jail network config to be usable in conf
    '''
    def filters(self):
        return {
                'jail_net_conf': jail_net_conf
                }


