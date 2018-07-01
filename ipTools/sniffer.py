#!/usr/bin/env python3

"""
Simple network traffic sniffer written in Python

Usage: sniffer.py

"""

import socket

# create raw socket sniffer object
proto = input("""
\n[+] Enter a sniff type
\n
\n
[1] ICMP\n
[2] TCP\n
[3] UDP\n
\n""")
if proto != 1 or proto != 2 or proto != 3:
    print("[-] ERROR: Bad Selection! Using default: ICMP")
    # exit(0)
    proto = 1
elif proto == 1:
    proto_value = socket.IPPROTO_ICMP
elif proto == 2:
    proto_value = socket.IPPROTO_TCP
elif proto == 3:
    proto_value = socket.IPPROTO_UDP
# use IPV4 / raw sockets / user input protocol to create sniffer object
sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, proto_value)

# bind socket to localhost machine (0.0.0.0)
# use reserved unix port (0) to dynamically find open port
sniffer.bind(('0.0.0.0', 0))

# use set socket option method to ensure IP header is included
sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

# print status message
print("[+} Sniffer is listening for incoming connections... \n")

# get single packet
print(sniffer.recvfrom(65535))