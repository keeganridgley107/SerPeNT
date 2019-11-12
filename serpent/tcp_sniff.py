#!/usr/bin/env python3

"""
Simple TCP traffic sniffer

Usage: tcp_sniff.py

Notes: currently only sniffs localhost traffic

Credits: https://www.pluralsight.com/authors/gus-khawaja :: Penetration Testing Automation Using Python and Kali Linux

"""

import socket
import struct
from ctypes import *


class IPHeader(Structure):

    # maps to ip header bytes using ctypes
    _fields_ = [
        ("ihl", c_ubyte, 4),
        ("version", c_ubyte, 4),
        ("tos", c_ubyte),
        ("len", c_ushort),
        ("id", c_ushort),
        ("offset", c_ushort),
        ("ttl", c_ubyte),
        ("protocol_num", c_ubyte),
        ("sum", c_ushort),
        ("src", c_uint32),
        ("dst", c_uint32)
    ]

    def __new__(self, data=None):
        return self.from_buffer_copy(data)

    def __init__(self, data=None):
        # map source and destination ip address
        self.source_address = socket.inet_ntoa(struct.pack("@I", self.src))
        # convert 32 bit IPV4 binary into human readable data
        self.destination_address = socket.inet_ntoa(struct.pack("@I", self.dst))
        # map protocols
        self.protocols = {1: "ICMP", 6: "TCP", 17: "UDP"}
        try:
            self.protocol = self.protocols[self.protocol_num]
        except:
            self.protocol = str(self.protocol_num)


def init_tcp_socket():
    """Create TCP socket object"""
    tcp_sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
    # bind object to localhost
    tcp_sniffer.bind(('0.0.0.0', 0))
    # include the ip header
    tcp_sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
    # return the configured socket object
    return tcp_sniffer


def start_sniffing():
    """TCP Sniffer """
    tcp_sniffer = init_tcp_socket()
    print("[+] Listening for incoming connections...")
    try:
        while True:
            # inf loop to listen on TCP
            raw_buffer_tcp = tcp_sniffer.recvfrom(65535)[0]
            ip_header_tcp = IPHeader(raw_buffer_tcp[0:20])

            if ip_header_tcp.protocol == "TCP":
                print("Protocol: %s %s -> %s" % (ip_header_tcp.protocol, ip_header_tcp.source_address, ip_header_tcp.destination_address))
    except KeyboardInterrupt:
        print("[-] Exiting Sniffer...")
        exit(0)


def main():
    start_sniffing()


if __name__ == '__main__':
    # call the main function
    main()
