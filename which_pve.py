#!/usr/bin/env python

import pve_credentials
import proxmoxer
import argparse

pve_con = proxmoxer.ProxmoxAPI(pve_credentials.pve_host, user=pve_credentials.pve_user, password=pve_credentials.pve_password, verify_ssl=False)

# lists all vms in cluster
for pve_node in pve_con.nodes.get():
    for vm in pve_con.nodes(pve_node['node']).qemu.get():
        print(pve_node['node'])
        print("{}. {} => {}".format(vm['firewall'], vm['name'], vm['status']))

parser = argparse.ArgumentParser(description="Get hypervisor running given VM as argument")

parser.add_argument('vm_name', help="virtual machine name")
