Role Name
=========

Role to manage creation of basic jails on freebsd.

Requirements
------------

I try to keep this as simple as possible. Therefore I try to not use any feature or tool which is not part of the base system.

Role Variables
--------------

Most of the variables are used from the guest's variables. 
Only a few comes from the host. Which comes from the host, must be a dict within the variable name `jail`.

The mandatory variables within the jail is:
- `root`: the definition of the *root*
- `child_group`: the child's groupname
- `user`: user name to be created within the jails
- `ssh_key`: ssh public-key installed into the user's *authorized_keys*.

Within the `root` the following two keys must be defined:
- `dataset`: The dataset name which will contain all of your jails. Eg. `zroot/jails`
- `mountpoint`: Where your dataset should be mounted. Eg. `/jails`

`child_group` must contain that ansible inventory group name which have the all the jails on this host

eg. write this into the `host_variables` (`host_vars/beastie.yaml`) :
```
jail:
  root:
    dataset: zroot/jails
    mountpoint: /jails
  child_group: beastie_jails
  user: ansible
  ssh_key: ssh-rsa AAA...=
```

Configuration of the jails themselves are imported from the hostvars of the given jail.
Specifically, you must create a variable called `jail` and every jail related setting is below this dict.

Though the jail role goes through every singe host in the above defined group within your inventory, there is a way to add a dobule-check step:

If the jail configuration has a `parent` key defined, and the value of the given key is different from the parent hosts's hostname, than that jail will be skipped in processing.
Possible variables for the jails:
`parent`: Which `ansible_host` is the host of this jail. default: the host we are running steps on.
`vnet`: A string or list of interface names which will have a bridge with the jails epair interface
`inet`: network configuration line (or lines) of the interfaces of the epair interfaces. This goes right away to the jail's rc.conf into the respective line or lines. N.B. If an array of interfaces are defined, than vnet[0]'s inet config within the jail is inet[0], and so on...
`defaultrouter`: defaultrouter of the jail
`ns_search`: This string will be appeneded after the `search` keyword in the guest's resolv.conf
`ns_server`: ip, or list of ips of nameservers for the jail.
`mounts`: list of mount points. A list element is either a simple directory name. In this case the directory must be the same on the host and within the jail. Or a list of two elements: the directory name on the host, and the directory name, how you can see it within the jail. Prefix of the jail's root must be omited.
`custom`: custom jail configurations can be added here, eg. enabling sysv ipc.

There is one important configuration item in the jails' hostconfig: the `ansible_user`. With this you can override the username from the host's configuration on a per-jail basis.
example jail's host vars (e.g.: `host_vars/beelzebub.yaml`) :
```
jail:
  parent: beastie
  vnet:
    - re0.101
    - re0.102
  inet:
    - inet 10.0.0.1 netmask 255.255.255.0
    - inet 10.0.1.1 netmask 255.255.255.0
  defaultrouter: 10.0.0.254
  ns_search: srv.intra dmz.intra
  ns_server:
    - 10.0.0.254
    - 10.0.1.254
  mounts:
    - [/srv/beelzebub, /srv]
  custom:
    enforce_statfs: 1
    sysvshm: new
    sysvmsg: new
    sysvsem: new
ansible_user: pasztor
```

example inventory file:
```
[jailhosts]
beastie

[beastie_jails]
beelzebub
```

Tags
----

Rest of the tasks don't have any tags. Though at certain points for debug reasons a few variables can be displayed if you allow the debug tags to run too.
If you only provide the ``--tags debug`` to ansible-playbook, than no task will run. In order to run the usual steps and the debug tags, you should use the ``--tags all,debug`` parameters to allow these debug steps to run.


Dependencies
------------

This role doesn't depend on any other role, installed function or anything. It only uses tools coming with the base system.

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

```
    - hosts: jailhosts
      roles:
         - pasztor.jail
```

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
