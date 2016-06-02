#! /usr/bin/python

import os
from multiprocessing import Pool
from neutronclient.v2_0 import client as neutron_client

def get_neutron_credentials():
    d = {}
    d['username'] = os.environ['OS_USERNAME']
    d['password'] = os.environ['OS_PASSWORD']
    d['auth_url'] = os.environ['OS_AUTH_URL']
    d['tenant_name'] = os.environ['OS_TENANT_NAME']
    return d

def t_create_network(i):
    neutron_credentials = get_neutron_credentials()
    neutron = neutron_client.Client(**neutron_credentials)
    json = {'network': {'name': 'network-' + str(i),
                        'admin_state_up': True}}
    while True:
        try:
            neutron.create_network(body=json)
            print '\nnetwork-' + str(i) + ' created'
            break
        except Exception as e:
            print e
            continue

pool = Pool(processes=10)

for i in range(1,101):
    pool.apply_async(t_create_network, (i, ))

pool.close()
pool.join()
print "****** DONE!! ******"
