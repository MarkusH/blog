===================================
[Update] My own IPv6 tunnel broker.
===================================


:tags: Bash, Encryption, Linux, Network, Security, Server
:author: Markus Holtermann


Some days ago I needed to test a web application on its IPv6 support. But since
my Internet service provider only gives me an IPv4 address, I was not able to
test the application. So, I thought about registering at `SixXS
<http://www.sixxs.net/>`_ to get an IPv6 address. But then I thought about
setting up my own broker. After some time I found a `nearly perfect tutorial
<https://www.zagbot.com/openvpn_ipv6_tunnel.html>`_ that uses `OpenVPN
<http://openvpn.net/index.php/open-source.html>`_.

I took the scripts from that tutorial and stored them on my server and client,
set everything up as explained and ... didn't got it working :(. I must say,
that I had limited time to completely understand what was going wrong, so I
stop trying.

Last weekend I had some hours to work on the IPv6 tunnel broker again and
finally got it working. So, here are my scripts and a short explanation.

**Update:** I did some improvements and enhancements on the scripts and pushed
them to `a Github repository <https://github.com/MarkusH/ipv6-broker>`_. Feel
free to fork and report issues.


Server
======

* You need a dedicated OpenVPN account if your OpenVPN does not run as root.
  You must give this user full password-less ``sudo`` access to ``/sbin/ip``:
  ``openvpn ALL=(ALL)  NOPASSWD: /sbin/ip``
* You must enable package forwarding for IPv6. Append
  ``net.ipv6.conf.all.forwarding = 1`` to ``/etc/sysctl.conf``.
  
  .. warning::

     If you automatically receive your IPv6 routes, you *must* set your v6
     routes manually:

     .. code-block:: code
     
        $ ip -6 route add ::/0 via <IPv6-Gateway> dev <eth0>

* You may need to activate *Neighbor Discovery Proxy*: Add
  ``net.ipv6.conf.all.proxy_ndp = 1`` to your ``/etc/sysctl.conf``
* Copy the files ``client-connect-ipv6-broker.sh``,
  ``client-disconnect-ipv6-broker.sh`` and ``ipv6-broker.sh`` to your server
  into the directory ``/etc/openvpn/`` and make sure they are executable.
* Append the lines from the ``server-ipv6.conf`` file to your OpenVPN server
  configuration.


Client
======

* You need a dedicated OpenVPN account if your OpenVPN does not run as root.
  You must give this user full password-less ``sudo`` access to ``/sbin/ip``:
  ``openvpn ALL=(ALL)  NOPASSWD: /sbin/ip``
* Copy the files ``up-ipv6-broker.sh``, ``down-ipv6-broker.sh`` and
  ``ipv6-broker.sh`` to your client into the directory ``/etc/openvpn/`` and
  make sure they are executable.
* Append the lines from the ``client-ipv6.conf`` file to your OpenVPN client
  configuration.


The scripts
===========

.. code-block:: bash

    OpenVPN IPv6 Tunnel Broker

    Copyright (c) 2012 Markus Holtermann

    Copyright (c) 2011 Lyndsay Roger - https://www.zagbot.com/

    This program is free software: you can redistribute it and/or modify it under
    the terms of the GNU General Public License as published by the Free Software
    Foundation, either version 3 of the License, or (at your option) any later
    version.

    This program is distributed in the hope that it will be useful, but WITHOUT ANY
    WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
    PARTICULAR PURPOSE. See the GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along with
    this program. If not, see http://www.gnu.org/licenses/.


ipv6-broker.sh
--------------

.. code-block:: bash

    #!/bin/bash

    # Your /64 Network prefix
    export BASERANGE="1234:5678:90ab:cdef"
    # The IPv4 address of your vpn server
    export VPN_HOST="10.8.0.1"

    export LOG_TAG="ipv6-broker"
    export DEBUG=1

    if [ -e "/etc/openvpn/client.conf" ] ; then
        export CLIENT=1
    else
        export CLIENT=0
    fi

    if [ $CLIENT -eq 1 ] ; then
        export SITID="sit1"
        export V6NET="${BASERANGE}::$(echo ${ifconfig_local} | awk -F. '{printf "%02x%02x:%02x", $2, $3, $4}')"
    else
        export SITID="sit$(echo ${ifconfig_pool_remote_ip} | awk -F. '{print $2"-"$3"-"$4}')"
        export V6NET="${BASERANGE}::$(echo ${ifconfig_pool_remote_ip} | awk -F. '{printf "%02x%02x:%02x", $2, $3, $4}')"
    fi


client-connect-ipv6-broker.sh
-----------------------------

.. code-block:: bash

    #!/bin/bash

    source /etc/openvpn/ipv6-broker.sh

    # This is a script that is run each time a remote client connects
    # to this openvpn server.
    # it will setup the ipv6 tunnel depending on the ip address that was
    # given to the client

    # setup the sit between the local and remote openvpn addresses
    test $DEBUG -eq 1 && echo "/sbin/ip tunnel add ${SITID} mode sit ttl 255 remote ${ifconfig_pool_remote_ip} local ${ifconfig_local}" | /usr/bin/logger -t $LOG_TAG
    sudo /sbin/ip tunnel add ${SITID} mode sit ttl 255 remote ${ifconfig_pool_remote_ip} local ${ifconfig_local}

    # activate the tunnel device
    test $DEBUG -eq 1 && echo "/sbin/ip link set dev ${SITID} up" | /usr/bin/logger -t $LOG_TAG
    sudo /sbin/ip link set dev ${SITID} up

    # config routing for the new network
    test $DEBUG -eq 1 && echo "/sbin/ip -6 addr add ${V6NET}01/124 dev ${SITID}" | /usr/bin/logger -t $LOG_TAG
    sudo /sbin/ip -6 addr add ${V6NET}01/124 dev ${SITID}

    # add the route for the network
    test $DEBUG -eq 1 && echo "/sbin/ip -6 route add ${V6NET}00/124 via ${V6NET}02 dev ${SITID} metric 1" | /usr/bin/logger -t $LOG_TAG
    sudo /sbin/ip -6 route add ${V6NET}00/124 via ${V6NET}02 dev ${SITID} metric 1

    # add neighbor discovering proxy for this interface
    test $DEBUG -eq 1 && echo "/sbin/ip -6 neigh add proxy ${V6NET}02 dev eth0" | /usr/bin/logger -t $LOG_TAG
    sudo /sbin/ip -6 neigh add proxy ${V6NET}02 dev eth0

    # log to syslog
    test $DEBUG -eq 1 && echo "${script_type} client_ip:${trusted_ip} common_name:${common_name} local_ip:${ifconfig_local} remote_ip:${ifconfig_pool_remote_ip} sit:${SITID} ipv6net:${V6NET}" | /usr/bin/logger -t $LOG_TAG
    test $DEBUG -eq 1 && sudo /sbin/ip addr show | /usr/bin/logger -t $LOG_TAG
    test $DEBUG -eq 1 && sudo /sbin/ip -6 route show | /usr/bin/logger -t $LOG_TAG

    # needed for connection
    exit 0


client-disconnect-ipv6-broker.sh
--------------------------------

.. code-block:: bash

    #!/bin/bash

    source /etc/openvpn/ipv6-broker.sh

    # remove neighbor discovering proxy again
    test $DEBUG -eq 1 && echo "/sbin/ip -6 neigh del proxy ${V6NET}02 dev eth0" | /usr/bin/logger -t $LOG_TAG
    sudo /sbin/ip -6 neigh del proxy ${V6NET}02 dev eth0

    # remove the route
    test $DEBUG -eq 1 && echo "/sbin/ip -6 route del ${V6NET}00/124 via ${V6NET}02 dev ${SITID} metric 1" | /usr/bin/logger -t $LOG_TAG
    sudo /sbin/ip -6 route del ${V6NET}00/124 via ${V6NET}02 dev ${SITID} metric 1

    # unset the ipv6 address
    test $DEBUG -eq 1 && echo "/sbin/ip -6 addr del ${V6NET}01/124 dev ${SITID}" | /usr/bin/logger -t $LOG_TAG
    sudo /sbin/ip -6 addr del ${V6NET}01/124 dev ${SITID}

    # deactivate the tunnel
    test $DEBUG -eq 1 && echo "/sbin/ip link set dev ${SITID} down" | /usr/bin/logger -t $LOG_TAG
    sudo /sbin/ip link set dev ${SITID} down

    # remove the tunnel interface
    test $DEBUG -eq 1 && echo "/sbin/ip tunnel del ${SITID} mode sit ttl 255 remote ${ifconfig_pool_remote_ip} local ${ifconfig_local}" | /usr/bin/logger -t $LOG_TAG
    sudo /sbin/ip tunnel del ${SITID} mode sit ttl 255 remote ${ifconfig_pool_remote_ip} local ${ifconfig_local}

    test $DEBUG -eq 1 && sudo /sbin/ip addr show | /usr/bin/logger -t $LOG_TAG
    test $DEBUG -eq 1 && sudo /sbin/ip -6 route show | /usr/bin/logger -t $LOG_TAG

    exit 0


up-ipv6-broker.sh
-----------------

.. code-block:: bash

    #!/bin/bash

    source /etc/openvpn/ipv6-broker.sh

    # script that is run on the client when it creates a tunnel to the remote OpenVPN server

    test $DEBUG -eq 1 && echo "/sbin/ip tunnel add ${SITID} mode sit ttl 255 remote ${VPN_HOST} local ${ifconfig_local}" | /usr/bin/logger -t $LOG_TAG
    sudo /sbin/ip tunnel add ${SITID} mode sit ttl 255 remote ${VPN_HOST} local ${ifconfig_local}

    test $DEBUG -eq 1 && echo "/sbin/ip link set dev ${SITID} up" | /usr/bin/logger -t $LOG_TAG
    sudo /sbin/ip link set dev ${SITID} up

    test $DEBUG -eq 1 && echo "/sbin/ip -6 addr add ${V6NET}02/124 dev ${SITID}" | /usr/bin/logger -t $LOG_TAG
    sudo /sbin/ip -6 addr add ${V6NET}02/124 dev ${SITID}

    test $DEBUG -eq 1 && echo "/sbin/ip route add ::/0 via ${V6NET}01" | /usr/bin/logger -t $LOG_TAG
    sudo /sbin/ip route add ::/0 via ${V6NET}01

    test $DEBUG -eq 1 && sudo /sbin/ip addr show | /usr/bin/logger -t $LOG_TAG
    test $DEBUG -eq 1 && sudo /sbin/ip -6 route show | /usr/bin/logger -t $LOG_TAG

    exit 0


down-ipv6-broker.sh
-------------------

.. code-block:: bash

    #!/bin/bash

    source /etc/openvpn/ipv6-broker.sh

    test $DEBUG -eq 1 && echo "/sbin/ip route del ::/0 via ${V6NET}01" | /usr/bin/logger -t $LOG_TAG
    sudo /sbin/ip route del ::/0 via ${V6NET}01

    test $DEBUG -eq 1 && echo "/sbin/ip -6 addr del ${V6NET}02/124 dev ${SITID}" | /usr/bin/logger -t $LOG_TAG
    sudo /sbin/ip -6 addr del ${V6NET}02/124 dev ${SITID}

    test $DEBUG -eq 1 && echo "/sbin/ip link set dev ${SITID} down" | /usr/bin/logger -t $LOG_TAG
    sudo /sbin/ip link set dev ${SITID} down

    test $DEBUG -eq 1 && echo "/sbin/ip tunnel del ${SITID} mode sit ttl 255 remote ${VPN_HOST} local ${ifconfig_local}" | /usr/bin/logger -t $LOG_TAG
    sudo /sbin/ip tunnel del ${SITID} mode sit ttl 255 remote ${VPN_HOST} local ${ifconfig_local}

    test $DEBUG -eq 1 && sudo /sbin/ip addr show | /usr/bin/logger -t $LOG_TAG
    test $DEBUG -eq 1 && sudo /sbin/ip -6 route show | /usr/bin/logger -t $LOG_TAG

    exit 0


Configuration

You finally need to add a few lines to your ``/etc/openvpn/server.conf``

.. code-block:: bash

    ###########################################
    # IPv6 tunnel broker
    ###########################################
    script-security 2
    client-connect /etc/openvpn/client-connect-ipv6-broker.sh
    client-disconnect /etc/openvpn/client-disconnect-ipv6-broker.sh


And a few lines to your ``/etc/openvpn/client.conf``:

.. code-block:: bash

    #############################################
    # IPv6 tunnel broker
    #############################################
    # need this so when the client disconnects it
    # tells the server so the server can remove
    # the ipv6 tunnel the client was using
    explicit-exit-notify
    script-security 2

    # create the ipv6 tunnel
    up /etc/openvpn/up-ipv6-broker.sh
    down /etc/openvpn/down-ipv6-broker.sh
