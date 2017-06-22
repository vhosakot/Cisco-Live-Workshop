#! /usr/bin/python

################################################
#                                              #
# api_setup.py - Sets up Python OpenStack APIs #
#                                              #
# Author: Vikram Hosakote (vhosakot@cisco.com) #
#                                              #
################################################

# Import required libraries
import os
import random
import subprocess
import sys
import time
from keystoneauth1 import identity
from keystoneauth1 import session
from neutronclient.v2_0 import client as neutron_client
from novaclient import client as nova_client

# Use OpenStack credentials and create neutron and nova client objects
try:
    username = os.environ['OS_USERNAME']
    password = os.environ['OS_PASSWORD']
    project_name = os.environ['OS_PROJECT_NAME']
    project_domain_id = os.environ['OS_PROJECT_DOMAIN_ID']
    user_domain_id = os.environ['OS_USER_DOMAIN_ID']
    auth_url = os.environ['OS_AUTH_URL']

    auth = identity.Password(auth_url=auth_url,
                             username=username,
                             password=password,
                             project_name=project_name,
                             project_domain_id=project_domain_id,
                             user_domain_id=user_domain_id)
    sess = session.Session(auth=auth)
    neutron = neutron_client.Client(session=sess)
    nova = nova_client.Client("2.0", session=sess)
except Exception as e:
    print "\nAn Exception was raised: ", type(e), e, "\n"
    sys.exit()

# GLobal variables
network_id = ''
subnet_id  = ''
router_id  = ''
many_router_list = []

# Function to run a Linux command
def run_command(cmd):
    try:
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        if err is not None:
            raise Exception(cmd + " failed with error: " + err)
    except Exception as e:
        print "\nAn Exception was raised: ", type(e), e, "\n"
        sys.exit()

# Function to start tcpdump packet capture
def start_capture(capture_name, port="9696"):
    try:
        run_command("echo 'ciscolive' | sudo -S sudo pkill tcpdump > /dev/null")
        run_command("rm -rf *.pcap")
        run_command("echo 'ciscolive' | sudo -S sudo tcpdump -vvvv -i any -w " \
                    + capture_name + " port " + port + " > /dev/null 2>&1 &")
    except Exception as e:
        print "\nAn Exception was raised: ", type(e), e, "\n"
        sys.exit()

# Function to stop tcpdump packet capture and push it to GitHub
def stop_capture(capture_name):
    try:
        run_command("echo 'ciscolive' | sudo -S sudo pkill tcpdump > /dev/null")
        time.sleep(1)
        run_command("mv -f " + capture_name + " Cisco-Live-Workshop/best-rest/packet-captures/")
        os.chdir("Cisco-Live-Workshop")
        run_command("git pull > /dev/null 2>&1")
        run_command("git pull > /dev/null 2>&1")
        run_command("git add *")
        run_command("git commit -m \"Cisco Live commit\" > /dev/null 2>&1")
        run_command("git push origin master > /dev/null 2>&1")
        os.chdir("..")
        run_command("rm -rf *.pcap")
        run_command("echo 'ciscolive' | sudo -S sudo pkill tcpdump > /dev/null")
    except Exception as e:
        print "\nAn Exception was raised: ", type(e), e, "\n"
        sys.exit()

# Function to push Cisco-Live-Workshop to GitHub
def push_capture():
    try:
        os.chdir("Cisco-Live-Workshop")
        run_command("git pull > /dev/null 2>&1")
        run_command("git pull > /dev/null 2>&1")
        run_command("git add *")
        run_command("git commit -m \"Cisco Live commit\" > /dev/null 2>&1")
        run_command("git push origin master > /dev/null 2>&1")
        os.chdir("..")
    except Exception as e:
        print "\nAn Exception was raised: ", type(e), e, "\n"
        sys.exit()

# Function to create a neutron network
def create_network(prefix):
    try:
        global network_id
        network_name = prefix + "-network"
        data  ={'network' : {'name': network_name, 'admin_state_up': True}}
        print "\nCreating network " + network_name +  ", please wait..."
        capture_name = prefix + "_create_network.pcap"
        start_capture(capture_name)
        time.sleep(1)
        result = neutron.create_network(data)
        network_id = result['network']['id']
        time.sleep(random.randint(1,6))
        stop_capture(capture_name)
        print "\nCreated network " + network_name + \
            "! Check the OpenStack GUI.\n"
    except Exception as e:
        print "\nAn Exception was raised: ", type(e), e, "\n"
        sys.exit()

# Function to create a neutron subnet
def create_subnet(prefix):
    try:
        global subnet_id
        subnet_name = prefix + "-subnet"
        data = {'subnets': [{'cidr': "30.30.0.0/24",
                     'ip_version': 4,
                     'network_id': network_id,
                     'gateway_ip': "30.30.0.1",
                     'name': subnet_name}]}
        print "\nCreating subnet " + subnet_name +  ", please wait..."
        capture_name = prefix + "_create_subnet.pcap"
        start_capture(capture_name)
        time.sleep(1)
        result = neutron.create_subnet(data)
        subnet_id = result['subnets'][0]['id']
        time.sleep(random.randint(1,6))
        stop_capture(capture_name)
        print "\nCreated subnet " + subnet_name + \
            "! Check the OpenStack GUI.\n"
    except Exception as e:
        print "\nAn Exception was raised: ", type(e), e, "\n"
        sys.exit()

# Function to create a neutron router
def create_router(prefix):
    try:
        global router_id
        router_name = prefix + "-router"
        data = {"router": {"name": router_name, "admin_state_up": True}}
        print "\nCreating router " + router_name +  ", please wait..."
        capture_name = prefix + "_create_router.pcap"
        start_capture(capture_name)
        time.sleep(1)
        result = neutron.create_router(data)
        router_id = result['router']['id']
        time.sleep(random.randint(1,6))
        stop_capture(capture_name)
        print "\nCreated router " + router_name + \
            "! Check the OpenStack GUI.\n"
    except Exception as e:
        print "\nAn Exception was raised: ", type(e), e, "\n"
        sys.exit()

# Function to add router gateway and router interface
def setup_router(prefix):
    try:
        router_name = prefix + "-router"
        print "\nSetting up router " + router_name + ", please wait..."
        public_network_id = neutron.list_networks(name="public")['networks'][0]['id']
        data = {"network_id": public_network_id}
        neutron.add_gateway_router(router_id, data)
        data = {"subnet_id": subnet_id}
        neutron.add_interface_router(router_id, data)
        print "\nRouter " + router_name + " setup successfully" + \
            "! Check the OpenStack GUI.\n"
    except Exception as e:
        print "\nAn Exception was raised: ", type(e), e, "\n"
        sys.exit()

# Function to boot a nova VM
def boot_vm(prefix):
    try:
        vm_name = prefix + "-vm"
        image = nova.images.find(name="cirros-0.3.4-x86_64-uec")
        flavor = nova.flavors.find(name="m1.tiny")
        nics = [{'net-id': network_id}]
        print "\nBooting VM " + vm_name +  ", please wait..."
        capture_name = prefix + "_boot_vm.pcap"
        start_capture(capture_name, port="8774")
        time.sleep(1)
        nova.servers.create(name=vm_name, image=image, flavor=flavor, nics=nics)
        time.sleep(3)
        time.sleep(random.randint(1,6))
        stop_capture(capture_name)
        run_command("openstack security group rule create --protocol tcp --dst-port 22 default > /dev/null 2>&1")
        run_command("openstack security group rule create --protocol icmp --dst-port -1 default > /dev/null 2>&1")
        run_command("echo 'ciscolive' | sudo -S sudo rm -rf /root/.ssh/known_hosts")
        vm = nova.servers.list()[0]
        vm_private_ip = vm.addresses[prefix + '-network'][0]['addr']
        print "\nBooted VM " + vm_name + "! Check the OpenStack GUI."
        print "\nYou can SSH into the VM " + vm_name + " using the following command after few minutes:"
        print "\n  sudo ip netns exec qdhcp-" + network_id + " ssh cirros@" + vm_private_ip
        print "\n  SSH password is cubswin:)\n"
    except Exception as e:
        print "\nAn Exception was raised: ", type(e), e, "\n"
        sys.exit()

# Function to delete nova VM
def delete_vm(prefix):
    try:
        vm_name = prefix + "-vm"
        print "\nDeleting VM " + vm_name + ", please wait..."
        capture_name = prefix + "_delete_vm.pcap"
        start_capture(capture_name, port="8774")
        time.sleep(1)
        vm = nova.servers.list()
        for v in vm:
            nova.servers.delete(v)
        time.sleep(random.randint(1,6))
        stop_capture(capture_name)
        print "\nDeleted VM " + vm_name + "! Check the OpenStack GUI.\n"
    except Exception as e:
        print "\nAn Exception was raised: ", type(e), e, "\n"
        sys.exit()

# Function to delete router gateway, router interface and neutron router
def delete_router(prefix):
    try:
        router_name = prefix + "-router"
        print "\nDeleting router " + router_name +  ", please wait..."
        routers = neutron.list_routers()['routers']
        for r in routers:
            if r['name'] == 'router1':
                continue
            else:
                # Delete router gateway
                neutron.remove_gateway_router(r['id'])
                # Delete router interface
                subnets = neutron.list_subnets()['subnets']
                for s in subnets:
                    if s['name'] == 'private-subnet' or \
                       s['name'] == 'ipv6-private-subnet':
                        continue
                    else:
                        data = {"subnet_id": s['id']}
                        neutron.remove_interface_router(r['id'], data)
                # Delete router
                capture_name = prefix + "_delete_router.pcap"
                start_capture(capture_name)
                time.sleep(1)
                neutron.delete_router(r['id'])
                time.sleep(random.randint(1,6))
                stop_capture(capture_name)
        print "\nDeleted router " + router_name + "! Check the OpenStack GUI.\n"
    except Exception as e:
        print "\nAn Exception was raised: ", type(e), e, "\n"
        sys.exit()

# Function to delete neutron subnet
def delete_subnet(prefix):
    try:
        subnet_name = prefix + "-subnet"
        print "\nDeleting subnet " + subnet_name +  ", please wait..."
        subnets = neutron.list_subnets()['subnets']
        for s in subnets:
            if s['name'] == 'private-subnet' or \
               s['name'] == 'ipv6-private-subnet':
                continue
            else:
                capture_name = prefix + "_delete_subnet.pcap"
                start_capture(capture_name)
                time.sleep(1)
                neutron.delete_subnet(s['id'])
                time.sleep(random.randint(1,6))
                stop_capture(capture_name)
        print "\nDeleted subnet " + subnet_name + \
            "! Check the OpenStack GUI.\n"
    except Exception as e:
        print "\nAn Exception was raised: ", type(e), e, "\n"
        sys.exit()

# Function to delete neutron network
def delete_network(prefix):
    try:
        network_name = prefix + "-network"
        print "\nDeleting network " + network_name +  ", please wait..."
        networks = neutron.list_networks()['networks']
        for n in networks:
            if n['name'] == 'public' or n['name'] == 'private':
                continue
            else:
                capture_name = prefix + "_delete_network.pcap"
                start_capture(capture_name)
                time.sleep(1)
                neutron.delete_network(n['id'])
                time.sleep(random.randint(1,6))
                stop_capture(capture_name)
        print "\nDeleted network " + network_name + \
            "! Check the OpenStack GUI."
        print "\n  Great job!! :)\n"
    except Exception as e:
        print "\nAn Exception was raised: ", type(e), e, "\n"
        sys.exit()

# Function to cleanup everything (router, subnet, network)
def cleanup():
    try:
        # Delete nova VM
        vm = nova.servers.list()
        for v in vm:
            nova.servers.delete(v)
            print "\nDeleted VM " + v.name + "."

        # Delete router gateway, router interface and router
        routers = neutron.list_routers()['routers']
        for r in routers:
            if r['name'] == 'router1':
                continue
            else:
                # Delete router gateway
                neutron.remove_gateway_router(r['id'])

                # Delete router interface
                try:
                    subnets = neutron.list_subnets()['subnets']
                    for s in subnets:
                        if s['name'] == 'private-subnet' or \
                           s['name'] == 'ipv6-private-subnet':
                            continue
                        else:
                            data = {"subnet_id": s['id']}
                            neutron.remove_interface_router(r['id'], data)
                except:
                    pass

                # Delete router
                neutron.delete_router(r['id'])
                print "\nDeleted router " + r['name'] + "."

        # Delete subnet
        subnets = neutron.list_subnets()['subnets']
        for s in subnets:
            if s['name'] == 'private-subnet' or \
               s['name'] == 'ipv6-private-subnet':
                continue
            else:
                neutron.delete_subnet(s['id'])
                print "\nDeleted subnet " + s['name'] + "."

        # Delete network
        networks = neutron.list_networks()['networks']
        for n in networks:
            if n['name'] == 'public' or n['name'] == 'private':
                continue
            else:
                neutron.delete_network(n['id'])
                print "\nDeleted network " + n['name'] + ".\n"
    except Exception as e:
        print "\nAn Exception was raised: ", type(e), e, "\n"
        sys.exit()

# Function to create 8 networks, 8 subnets and 8 routers
def create_many(prefix):
    try:
        for i in range (1, 9):
            # Create network
            network_name = prefix + "-network-" + str(i)
            data  ={'network' : {'name': network_name, 'admin_state_up': True}}
            result = neutron.create_network(data)
            print "\nCreated network " + network_name + "."
            time.sleep(1)
            n_id = result['network']['id']

            # Create subnet
            subnet_name = prefix + "-subnet-" + str(i)
            data = {'subnets': [{'cidr': "40.40." + str(i) + ".0/24",
                    'ip_version': 4,
                    'network_id': n_id,
                    'gateway_ip': "40.40." + str(i) + ".1",
                    'name': subnet_name}]}
            result = neutron.create_subnet(data)
            print "\nCreated subnet " + subnet_name + "."
            time.sleep(1)
            s_id = result['subnets'][0]['id']

            # Create router
            router_name = prefix + "-router-" + str(i)
            data = {"router": {"name": router_name, "admin_state_up": True}}
            result = neutron.create_router(data)
            print "\nCreated router " + router_name + "."
            time.sleep(1)
            r_id = result['router']['id']
            public_network_id = neutron.list_networks(name="public")['networks'][0]['id']
            data = {"network_id": public_network_id}
            neutron.add_gateway_router(r_id, data)
            data = {"subnet_id": s_id}
            neutron.add_interface_router(r_id, data)
            item = {'router_id' : r_id, 'subnet_id' : s_id}
            many_router_list.append(item)
        print "\n Done!\n"
    except Exception as e:
        print "\nAn Exception was raised: ", type(e), e, "\n"
        sys.exit()

# Function to delete 8 networks, 8 subnets and 8 routers
def delete_many(prefix):
    try:
        # Delete router interface, router gateway and neutron router
        for item in many_router_list:
            data = {"subnet_id": item['subnet_id']}
            # Delete router interface
            neutron.remove_interface_router(item['router_id'], data)

        routers = neutron.list_routers()['routers']
        for r in routers:
            if r['name'] == 'router1':
                continue
            else:
                # Delete router gateway
                neutron.remove_gateway_router(r['id'])
                # Delete router
                neutron.delete_router(r['id'])
                print "\nDeleted router " + r['name'] + "."
                time.sleep(1)

        # Delete subnets
        subnets = neutron.list_subnets()['subnets']
        for s in subnets:
            if s['name'] == 'private-subnet' or \
               s['name'] == 'ipv6-private-subnet':
                continue
            else:
                neutron.delete_subnet(s['id'])
                print "\nDeleted subnet " + s['name'] + "."
                time.sleep(1)

        # Delete networks
        networks = neutron.list_networks()['networks']
        for n in networks:
            if n['name'] == 'public' or n['name'] == 'private':
                continue
            else:
                neutron.delete_network(n['id'])
                print "\nDeleted network " + n['name'] + "."
                time.sleep(1)
        print "\n Done!!\n"
    except Exception as e:
        print "\nAn Exception was raised: ", type(e), e, "\n"
        sys.exit()
