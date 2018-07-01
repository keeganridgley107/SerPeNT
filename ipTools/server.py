#!/usr/bin/env python3
"""
Simple Python web server tool

Usage: server.py

"""


################################################################################
# IMPORT MODULES
################################################################################


import socket
import threading
import argparse


################################################################################
# Functions
################################################################################


def start_server(port_number):
    """start the server up on the user specified port number"""
    # TODO: option starts a udp server using datagram protocol 
    # server_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', port_number))
    server.listen(10)
    print('[+] Listening on port %d ...' % port_number)

    while True:
        client,address = server.accept()
        print('[+] Connected with the client: %s:%d' % (address[0], address[1]))

        # multi-threading
        serve_client_thread = threading.Thread(target=serve_client,args=(client,address[0],address[1]))
        serve_client_thread.start()


def parse():
    """"parse the cmd line args passed in"""
    parser = argparse.ArgumentParser('server.py')
    parser.add_argument("-p", "--port", type=int, help="The port to serve on", default=5555)
    args = parser.parse_args()
    
    # store value of port
    port_number = args.port
    
    # start the server
    start_server(port_number)


def serve_client(client_to_serve_socket, client_ip, port_number):
    client_request = client_to_serve_socket.recv(4096)
    print('[+] Received data from the client (%s:%d):%s' % (client_ip, port_number, client_request))
    client_to_serve_socket.send("IpTools.server Version 1.0.2")
    client_to_serve_socket.close()


def main():
    print('[+] Starting web server... ')
    parse()


if __name__ == '__main__':
    # call the main function
    main()
