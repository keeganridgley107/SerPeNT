""""
TCP traffic sniffer

Usage: tcp_sniff.py

"""

import socket
import struct
from ctypes import *


class IPHeader(Structure):
    pass


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




def main():
    start_sniffing()


if __name__ == '__main__':
    # call the main function
    main()
