Role Name
=========

Role to manage creation of basic jails on freebsd.

Requirements
------------

I try to keep this as simple as possible. Therefore I try to not use any feature or tool which is not part of the base system.

Role Variables
--------------

Most of the variables are used from the guest's variables. The only variable it uses from the host is the `jail_root`. It must be a dict and must have at least two keys provided:
- dataset: The dataset name which will contain all of your jails. Eg. zroot/jails
- mountpoint: Where your dataset should be mounted. Eg. /jails
eg. write this into the `host_variables`:
```
jail_root:
  dataset: zroot/jails
  mountpoint: /jails
```

Though the role goes through every singe host in your inventory, and checks every one of them.
If that has a `jail_parent` variable, and the name of the `jail_parent` is the same what is the current host's inventory-name, than that jail will be taken care of.
Possible variables for the jails:
`jail_parent`: Which `ansible_host` is the host of this jail
`jail_vnet`: A string or list of interface names which will have a bridge with the jails epair interface
`jail_inet`: network configuration line (or lines) of the interfaces of the epair interfaces. This goes right away to the jail's rc.conf into the respective line or lines.
`jail_defaultrouter`: defaultrouter of the jail
`jail_ns_search`: This string will be appeneded after the `search` keyword in the guest's resolv.conf
`jail_ns_server`: ip, or list of ips of nameservers for the jail.

example jail's host vars:
```
jail_parent: parenthost
jail_vnet:
  - re0.101
  - re0.102
jail_inet:
  - inet 10.0.0.1 netmask 255.255.255.0
  - inet 10.0.1.1 netmask 255.255.255.0
jail_defaultrouter: 10.0.0.254
jail_ns_search: srv.intra dmz.intra
jail_ns_server:
  - 10.0.0.254
  - 10.0.1.254
```


Dependencies
------------

This role doesn't depend on any other role, installed function or anything. It only uses tools coming with the base system.

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

    - hosts: servers
      roles:
         - pasztor.jail

License
-------

BSD

Author Information
------------------

source url: https://github.com/pasztor/jail
Most of the idea and hints are coming from this tutorial: 
- https://eoli3n.eu.org/2021/06/08/jails-part-1.html
- https://eoli3n.eu.org/2021/06/09/jails-part-2.html
- https://eoli3n.eu.org/2021/06/14/jails-part-3.html
