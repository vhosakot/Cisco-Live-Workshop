Best REST in OpenStack - workshop steps
=======================================

1. Select the VM ``devstack-api`` in VirtualBox and press the "**Start**" button
   (green right arrow at the top). Wait a minute for the VM to boot.

2. After the VM boots and the login prompt is seen, open a terminal on the laptop,
   and SSH into the VM. Password is ``ciscolive``.

::

      ssh stack@192.168.20.3
      stack@192.168.20.3's password: ciscolive


3. Deploy OpenStack Ocata.  It takes about 13 minutes.

::

      cd devstack
      ./stack.sh


4. After ``stack.sh`` ends, the OpenStack Horizon GUI can be accessed in a
   browser at http://192.168.20.3. Username is ``admin`` and password is ``password``.

5. In the OpenStack GUI, select the ``demo`` project at the top left (next to the
   OpenStack logo). On the left pane, click on ``Project --> Network --> Network Topology`` and click on the ``Graph`` tab.

6. Source the environment variables needed for OpenStack. Ignore the warning.

::

      source openrc


7. Enter the ``python`` interpreter.

::

      python


8. Import the setup library.

::

      import api_setup as api


9. Set a ``prefix`` which is unique and not same as others. It is a good idea to use your first name or last name. We will use this ``prefix`` to create virtual objects in OpenStack and also to differentiate your HTTP packets from others.

::

      prefix = "<first name or last name>"


10. Create an OpenStack neutron network, check the OpenStack GUI, analyze HTTP packet.

::

      api.create_network(prefix)


11. Create an OpenStack neutron subnet, check the OpenStack GUI, analyze HTTP packet.

::

      api.create_subnet(prefix)


12. Create an OpenStack neutron router, check the OpenStack GUI, analyze HTTP packet.

::

      api.create_router(prefix)


13. Setup router (add router gateway and router interface), check the OpenStack GUI.

::

      api.setup_router(prefix)


14. Boot an OpenStack nova virtual machine, check the OpenStack GUI, analyze HTTP packet.

::

      api.boot_vm(prefix)


15. Open another terminal on the laptop and SSH into the ``devstack-api`` VM (password is ``ciscolive``). Copy the command in the output of step **14** above, paste it in this terminal to SSH into the OpenStack nova virtual machine. Check internet connectivity inside the nova virtual machine.

::

      ssh stack@192.168.20.3
      stack@192.168.20.3's password: ciscolive

      sudo ip netns exec qdhcp-c5fc33de-1ab9-4003-a860-c0a24ab03122 ssh cirros@30.30.0.3

      Type yes

      password is cubswin:)

      ip a

      ping -c 5 www.google.com

      ping -c 5 www.cisco.com

      exit

      exit


16. Back in the first terminal, delete the nova virtual machine, check the OpenStack GUI, analyze HTTP packet.

::

      api.delete_vm(prefix)


17. Delete the neutron router, check the OpenStack GUI, analyze HTTP packet.

::

      api.delete_router(prefix)


18. Delete the neutron subnet, check the OpenStack GUI, analyze HTTP packet. 

::

      api.delete_subnet(prefix)


19. Delete neutron network, check the OpenStack GUI, analyze HTTP packet.

::

      api.delete_network(prefix)


20. Create 8 networks, 8 subnets, 8 routers. This takes about 2 minutes to finish. Check the OpenStack GUI.

::

      api.create_many(prefix)


21. Delete 8 networks, 8 subnets, 8 routers. This takes about 2 minutes to finish. Check the OpenStack GUI.

::

      api.delete_many(prefix)


22. The script ``api_setup.py`` is at https://github.com/vhosakot/Cisco-Live-Workshop/blob/master/best-rest/scripts/api_setup.py.

23. The presentation slides of this workshop are at .
