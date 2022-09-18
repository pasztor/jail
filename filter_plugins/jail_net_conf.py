import json
import sys

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


