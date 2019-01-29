#!/usr/bin/env python3

"""
Simple network utility written in Python

Usage: scanner.py [-help] ADDRESS [-network] [-connect] [-ports] <PORT,PORT,+>

"""

# IMPORT MODULES
import argparse
from socket import *
import ipaddress
import ftplib
import random
from platform import system as system_name  # Returns the system/OS name
import subprocess  # Execute a shell command

###########################
# Main TODO: refactor / + multi-threading / + arg[report_closed]
###########################

##########################################################################################
# CURRENT MODULES : network scan / port scan / ftp password brute-force
##########################################################################################


def ping_host(host):
    """
    Returns True if host (str) responds to a ping request.
    Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
    """

    # Ping command count option as function of OS
    param = '-n' if system_name().lower() == 'windows' else '-c'

    # Building the command. "ping -c 1 google.com" for Unix || "ping -n 1 google.com" for windows
    command = ['ping', param, '1', host]

    # TODO: change to use check_output to not print pinging; only result
    # hostInfo = subprocess.check_output(['ping', param, '1', host], shell=True).decode("utf-8")
    # replyInfo = hostInfo.split("\n")
    # replyInfo = replyInfo[2]

    return subprocess.call(command) == 0


def ftp_recon(host, user, password):
    """ recon ftp server once password is found """
    try:
        ftp = ftplib.FTP(host)
        ftp.login(user, password)
        welcome = ftp.getwelcome()
        ftp_dir = ftp.dir()
        ftp.quit()
        print(" \n-------------------SCAN-REPORT-------------------")
        print("[+] FTP service: " + welcome + "\n")
        print("[+] Dir: " + ftp_dir)
        print(" \n")
    except:
        # error
        print("[-] ERROR: ERRRORRRRRRR0RRR!!!!")


def connect(host, user, password):
    """ connect to FTP server using dict file login """
    try:
        ftp = ftplib.FTP(host)
        ftp.login(user, password)
        ftp.quit()
        return True
    except:
        return False


def ftp_module(target_host):
    """Main module for ftp service tools"""

    print('\n')
    # get input for user name / list.txt
    user_name = input('Enter FTP UserName: ')

    passwords_file_path = "../Lists/" + input('Enter name of password list file: ')

    # TODO: refactor to remove default / handle clean file error

    print('[+] Using default password for ' + target_host)
    if connect(target_host, user_name, 'admin'):
        print("\n")
        print("------------DEFAULT-LOGIN-FOUND-------------------")
        print("\n")
        print("[+] FTP Login succeeded on host " + target_host)
        print("[+] UserName: " + user_name)
        print("[+] Password: admin")
        print("-------------------------------------------------")
        print("\n")
        ftp_recon(target_host, user_name, "admin")
    else:
        print('[-] FTP default login failed on host')

        # try brute force using dictionary file
        passwords_file = open(passwords_file_path, 'r')

        for line in passwords_file.readlines():
            # clean lines in dictionary file
            password = line.strip('\r').strip('\n')

            if connect(target_host, user_name, password):
                # password found
                print("\n")
                print("-------------------LOGIN-FOUND-------------------")
                print("\n")
                print("[+] FTP Login succeeded on host " + target_host)
                print("[+] UserName: " + user_name)
                print("[+] Password: " + password)
                print("-------------------SCAN-RESULTS------------------")
                print("\n")
                ftp_recon(target_host, user_name, password)
                print("\n")
                exit(0)

            else:
                # password NOT found
                print("\n")
                print("[-] FTP Login failed on host " + target_host)
                print("[-] UserName: " + user_name)
                print("[-] Password: " + password)
                print("-------------------------------------------------")
        else:
            print("[-] Error: Connection failed!")
            exit(0)


# noinspection PyListCreation
def ip_range(start_ip, end_ip):
    """enumerates ip addresses from a range"""
    # currently creates a full LAN scan from any ip passed in
    print(" [+] starting ip range...\n", start_ip, end_ip, "\n")
    start = list(map(int, start_ip.split(".")))
    # 12.13.14.15 => [12,13,14,15]
    end = list(map(int, end_ip.split(".")))
    print(start, " to ", end)
    temp = start
    ip_address_range = []

    ip_address_range.append(start_ip)
    while temp != end:
        start[3] += 1
        for i in (3, 2, 1):
            if temp[i] == 256:
                temp[i] = 0
                temp[i - 1] += 1
                print("[+] Adding to list...")
        ip_address_range.append(".".join(map(str, temp)))
    print("[+] Scan range created from ", start, " to ", end)
    print("[+] ", len(ip_address_range), " IP addresses to scan")
    return ip_address_range


def print_banner(conn_sock, tgt_port, tgt_host, is_connect_scan):
    """module that prints banner info from port if open"""
    print(conn_sock, tgt_port, tgt_host, is_connect_scan)
    if is_connect_scan:
        try:
            # send data to the target, if port 80 then send GET HTTP

            if tgt_port == 80:
                conn_sock.send("GET HTTP/1.1 \r\n")
            elif tgt_port == 21:
                ftp_module(tgt_host)
            else:
                # if not port 80 then just send a carriage return
                conn_sock.send("\r\n")
            # receive data from the target, number is bytes for the buffer size
            results = conn_sock.recv(4096)
            # print the banner
            print('[+] Banner:\n' + str(results))
        except:
            # if no banner, send fail msg
            print('[-] Banner not available')
    else:
        try:
            # send data to the target, if port 80 then send GET HTTP
            if tgt_port == 80:
                conn_sock.send("GET HTTP/1.1 \r\n")
            else:
                # if not port 80 then just send a carriage return
                conn_sock.send("\r\n")
            # receive data from the target, number is bytes for the buffer size
            results = conn_sock.recv(4096)
            # print the banner
            print('[+] Banner:\n' + str(results))
        except:
            # if no banner, send fail msg
            print('[-] Banner not available!')


def conn_scan(tgt_host, tgt_port, is_connect_scan):
    """module connects to ports and prints response msg"""
    try:
        # create the socket object
        conn_sock = socket(AF_INET, SOCK_STREAM)
        # try to connect with the target
        conn_sock.connect((tgt_host, tgt_port))
        print('[+] tcp port %d open' % tgt_port)
        print_banner(conn_sock, tgt_port, tgt_host, is_connect_scan)
    except:
        # print failure results
        # print('[-] tcp port %d closed' % tgtPort)
        pass
    finally:
        # close the socket object
        conn_sock.close()


def udp_conn_scan(tgt_host, port, is_connect_scan):
    """"connection scanner that uses UDP not TCP"""
    try:
        # create socket with AF_INET (ipv4) & Datagram (UDP)
        conn_sock = socket(AF_INET, SOCK_DGRAM)
        # try to connect with host
        conn_sock.connect(tgt_host, port)
        print("[+] UDP port %d open" % port)
        print_banner(conn_sock, port, tgt_host, is_connect_scan)
    except:
        # TODO: print fail msg if print_closed arg == True
        # print('[-] UDP port %d closed' % port)
        pass


def resolve_host(tgt_host, tgt_ports, is_connect_scan, is_udp):
    """ Resolves the hostname / target ip """

    try:
        # get ip from domain, else throw error msg
        tgtIP = gethostbyname(str(tgt_host))
    except:
        print("[-] Error: Unknown Host")
        exit(0)

    try:
        # print the resolved domain, or the ip if no resolution
        tgt_name = gethostbyaddr(tgtIP)
        print("[+] Hostname IP resolution")
        print("-------- Scan Result for: " + tgt_name[0] + " -----")
    except:
        print("-------- Scan Result for: " + tgtIP + " -----")
    # set default timeout and ICMP ping host
    setdefaulttimeout(1)
    can_ping_host = ping_host(tgtIP)
    # if host is live print response
    if can_ping_host:
        print("[+] Host responds to ICMP Ping ")
        pass
    else:
        # print("[-] No ICMP Ping response ")
        # TODO: add a arg for show / hide closed hosts & ports
        pass

    # check protocol and run port scan loop
    if is_udp:
        for port in tgt_ports:
            port = int(port)
            udp_conn_scan(tgt_host, port, is_connect_scan)
        print("\n[+] Completed UDP Scan.\n")
    # then run the tcp port scan loop
    for port in tgt_ports:
        port = int(port)
        conn_scan(tgt_host, port, is_connect_scan)
    print("\n[+] Completed TCP Scan.\n")


def mgmt_module(ipv4_ip_address, ipv4_host_list, port_numbers, is_network_scan, is_connect_scan, is_udp):
    """ direct activity and control program using top level args """

    if is_network_scan:
        # network scan, loop through address range
        random.shuffle(ipv4_host_list)
        for addr in ipv4_host_list:
            resolve_host(addr, port_numbers, is_connect_scan, is_udp)
    else:
        # not a network, scan single IP address
        resolve_host(ipv4_ip_address, port_numbers, is_connect_scan, is_udp)


def domain_check(ipv4_ip_address):

    # check for domain name && network scan flag
    domain_dot_check = ipv4_ip_address.split(".")
    host_name = gethostbyname(str(ipv4_ip_address))

    try:
        if domain_dot_check[1] == "com" or "net" or "org" or "io" or "gov" or "edu":
            # domain passed && network scan flag > get ip > generate network > portscan loop
            domain_ip = gethostbyname(str(ipv4_ip_address))
            ipv4_ip_address = domain_ip
    except IndexError:
        is_hostname = input("[-] Is target address a hostname? y/n ")
        if is_hostname == "y":
            ipv4_ip_address = host_name
        else:
            print("[-] ERROR: address cannot be resolved as IP, Domain or Host")
            exit(0)

    return ipv4_ip_address


def network_option(ipv4_ip_address, ipv4_host_list):
    """check network scan option"""

    ipv4_ip_address = domain_check(ipv4_ip_address)
    check_host_bit = list(map(int, ipv4_ip_address.split(".")))
    if check_host_bit[3] > 0:
        # reset the host bit
        check_host_bit[3] = 0

    # network flag = true
    start_net_ip = ipaddress.ip_address(
        str(check_host_bit[0]) + "." + str(check_host_bit[1]) + "." + str(check_host_bit[2]) + "." + str(
            check_host_bit[3]))
    end_net_ip = ipaddress.ip_address(
        str(check_host_bit[0]) + "." + str(check_host_bit[1]) + "." + str(check_host_bit[2]) + "." + str(254))
    print("[+] Network scan engaged, scanning targets from: " + str(start_net_ip) + " to " + str(end_net_ip))

    for targetAddress in range(int(start_net_ip), int(end_net_ip)):
        ipv4_host_list.append(ipaddress.IPv4Address(targetAddress))
    print(ipv4_host_list)
    return ipv4_host_list


def port_parse(port_numbers):
    """parse the port numbers out of input args"""
    for port in port_numbers:
        try:
            # check for number 22 vs range 22-26
            port_int = int(port)
            port = port_int
        except ValueError:
            port_split = port.split("-")
            port_range = range(int(port_split[0]), int(port_split[1]))
            port_numbers.remove(port)
            for new_port in port_range:
                port_numbers.append(new_port)
    # return is to handle basic scan calls from serpent.py
    return port_numbers


def parse():
    """parse any arguments passed into the cmd line"""

    parser = argparse.ArgumentParser(prog='scanner.py',
                                     description='''Simple Wireless Network Utility''',
                                     epilog='''Created by K''',
                                     usage='%(prog)s [-h] address [-p] [port-port,port,+] [-n] [-c]'
                                     )
    parser.add_argument("address", type=str, help="Target Address : 8.8.8.8 or google.com")
    parser.add_argument("-p", "--ports", type=str, default="20-25,80,443,8000,8080", help="Ports to scan : 20-25,80")
    parser.add_argument("-n", "--network", action="store_true", help="Scan network : X.X.X.1-254")
    parser.add_argument("-c", "--connect", action="store_true", help="Connect to discovered hosts")
    parser.add_argument("-u", "--udp", action="store_true", help="include UDP scan")

    args = parser.parse_args()
    ipv4_host_list = []

    # store the input args
    is_connect_scan = args.connect
    is_udp = args.udp
    ipv4_ip_address = args.address
    is_network_scan = args.network
    port_numbers = args.ports.split(",")

    if is_network_scan:
        ipv4_host_list = network_option(ipv4_ip_address, ipv4_host_list)
    else:
        ipv4_host_list.append(ipv4_ip_address)
    # call the port parse module to handle port numbers
    parsed_port_numbers = port_parse(port_numbers)
    mgmt_module(ipv4_ip_address, ipv4_host_list, parsed_port_numbers, is_network_scan, is_connect_scan, is_udp)


def main():
    # Parse args passed in then run mgmt module
    parse()


if __name__ == '__main__':
    # call the main function
    main()
