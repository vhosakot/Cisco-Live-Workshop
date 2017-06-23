OpenStack with OpenDaylight - workshop steps
============================================

1. Select the VM ``devstack-odl`` in VirtualBox and press the "**Start**" button
   (green right arrow at the top). Wait a minute for the VM to boot.

2. After the VM boots and the login prompt is seen, open a terminal on the laptop,
   and SSH into the VM. Password is ``ciscolive``.

::

      ssh stack@192.168.10.3
      stack@192.168.10.3's password: ciscolive


3. Deploy OpenStack Ocata with OpenDaylight Boron. It takes about 13 minutes.

::

      cd devstack_odl
      ./stack.sh


4. After ``stack.sh`` ends, the OpenStack Horizon GUI can be accessed in a
   browser at http://192.168.10.3 (username is ``admin``, password is ``password``).

5. In the OpenStack GUI, select the ``demo`` project at the top left (next to the
   OpenStack logo). On the left pane, click on ``Project --> Network --> Network Topology`` and click on the ``Graph`` tab.

6. Close the OpenStack GUI.

7. The OpenDaylight DLUX GUI can be accessed at http://192.168.10.3:8181/index.html (username is ``admin``, password is ``admin``).

8. In the OpenDaylight GUI, click on each of the following on the left pane:

-  Yang Visualizer (select different ``Model`` at the top)
-  Topology
-  Network Virtualization --> 2D View
-  Nodes --> Node connectors --> 2
-  Yang UI

9. Close the OpenDaylight GUI.

10. In the terminal,
