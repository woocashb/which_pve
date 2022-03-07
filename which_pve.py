#!/usr/bin/env python

import pve_credentials
import proxmoxer
import argparse
import sys

proxmox_api = proxmoxer.ProxmoxAPI(pve_credentials.pve_host, user=pve_credentials.pve_user, backend="ssh_paramiko")

# lists all vms in cluster

pve_hosts = [ "192.168.2.125", "192.168.2.126", "192.168.7.21", "192.168.7.22", "192.168.253.184", "192.168.7.17", "10.22.127.11", "10.22.127.12", "10.22.127.13", "192.168.7.24"]

parser = argparse.ArgumentParser(description="Get hypervisor running given VM as argument")

parser.add_argument('vm_name', help="virtual machine name")

args = parser.parse_args()
vm_found = False

for pve_host in pve_hosts:
    proxmox_api = proxmoxer.ProxmoxAPI(pve_host, user="root", backend="ssh_paramiko")
    for pve_node in proxmox_api.nodes.get():
        for vm in proxmox_api.nodes(pve_node['node']).qemu.get():
            if vm['name'] == args.vm_name:
                print("{} -> https://{}:8006".format(pve_node['node'], pve_host))
                vm_found = True
                sys.exit(0)


if not vm_found:
    print('No such VM found in pve list')
