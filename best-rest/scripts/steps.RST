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


10. Create an OpenStack neutron network.
