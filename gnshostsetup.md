############################################
Create TAP interface:
--

ip tuntap add name tap0 mode tap
ifconfig tap0 10.0.0.1/24 up
sudo ip route add 10.0.0.0/16 via 10.0.0.2


############################################
modify openvpn to push a route, modify the file /etc/openvpn/udp1194.conf to be:
basically add in the push linebelow

server 172.16.253.0 255.255.255.0
verb 3
duplicate-cn
comp-lzo
key key.pem
ca cert.pem
cert cert.pem
dh dh.pem
keepalive 10 60
persist-key
persist-tun
proto udp
port 1194
dev tun1194
push "route 10.0.0.0 255.255.0.0"
status openvpn-status-1194.log
log-append /var/log/openvpn-udp1194.log

############################################

Ensuring TAP is persistent upon reboot
--

vi /etc/rc.local (this creates file if non existent)

PASTE CONTENTS BETWEEN LINES CONTENTS:



-----------------COPY BELOW-----------------

#!/bin/sh -e
#
# rc.local
#
# This script is executed at the end of each multiuser runlevel.
# Make sure that the script will "exit 0" on success or any other
# value on error.
#
# In order to enable or disable this script just change the execution
# bits.
#
# By default this script does nothing.

sudo ip tuntap add name tap0 mode tap
sudo ifconfig tap0 10.0.0.1/24 up
sudo ip route add 10.0.0.0/16 via 10.0.0.2

exit 0

-----------------STOP ABOVE THIS LINE-----------------

Make rc.local executable:

chmod +x /etc/rc.local

############################################

Initial Router Configuration for Connection:
(Ensure you are in configuration terminal mode prior to pasting configs)
--

hostname R1
ip domain name cisco.com
crypto key generate rsa general-keys modulus 2048
ip ssh version 2
username kevin priv 15 secret kevin
line vty 0 4
 transport input ssh
 transport outputssh
 login local
int E0/0
 ip address 10.0.0.2 255.255.255.0
 no shut
ip route 0.0.0.0 0.0.0.0 10.0.0.1