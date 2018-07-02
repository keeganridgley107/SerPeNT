#!/usr/bin/env python3

"""
Simple network binary traffic sniffer written in Python

Usage: bin_sniff.py

"""

import socket

# create raw socket sniffer object
proto = int(input("""
\n[+] Enter a sniff type

[1] ICMP
[2] TCP
[3] UDP
\nTYPE: """))
if proto != 1 and proto != 2 and proto != 3:
    print("[-] ERROR: Bad Selection! Using default: ICMP")
    proto_value = socket.IPPROTO_ICMP
    # exit(0)
elif proto == 1:
    proto_value = socket.IPPROTO_ICMP
elif proto == 2:
    proto_value = socket.IPPROTO_TCP
elif proto == 3:
    proto_value = socket.IPPROTO_UDP
try:
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
    exit(0)
except:
    # handle general errors, break out more in refactor
    print("[-] Error: Encountered a fatal error.")
    # TODO: if windows && not admin == set runas=admin & try again
    print("[-] Exiting...")
    exit(0)
