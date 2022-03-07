#!/usr/bin/env python

import fabric
import sys
import argparse

pve_hosts = [ "192.168.2.125", "192.168.2.126", "192.168.7.21", "192.168.7.22", "192.168.253.184", "192.168.7.17", "10.22.127.11", "10.22.127.12", "10.22.127.13", "192.168.7.24"]
#pve_hosts = ['10.12.20.11', '10.12.20.13']
parser = argparse.ArgumentParser(description='Get hypervisor where given virtual machine resides')
parser.add_argument('vm_name', help='virtual machine name')
args = parser.parse_args()

VM_SEARCH_CMD = "qm list | awk '{print $2}' | grep -- " + args.vm_name

for pve_host in pve_hosts:
    with fabric.Connection(pve_host, user="root") as pve_host_connection:
        try:
            pve_host_vm_search_result = pve_host_connection.run(VM_SEARCH_CMD, hide=True)
            pve_host_hostname = pve_host_connection.run('hostname', hide=True)
            if pve_host_vm_search_result.return_code == 0 and pve_host_hostname.return_code == 0:
                print(f"{pve_host_hostname.stdout.rstrip()} -> https://{pve_host}:8006")
                sys.exit(0)
        except Exception:
            continue
else:
    print("No such vm name found in known PVE hosts!")
    sys.exit(1)
