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
from time import sleep

##########################################################################################
# CURRENT MODULES : network scan / port scan / ftp password brute-force
##########################################################################################


def pingHost(host):
    """
    Takes host address and returns True if host (str) responds to a ping request.

    Args: host address (string)

    Returns: Bool

    Note: Host may not respond to a ping (ICMP) request even if the hostname is valid.
    """

    # Ping command count option as function of OS
    param = '-n' if system_name().lower() == 'windows' else '-c'

    # Building the command. "ping -c 1 google.com" for Unix || "ping -n 1 google.com" for windows
    command = ['ping', param, '1', host]

    # Pinging
    # TODO: change to use check_output to not print pinging; only result
    # hostInfo = subprocess.check_output(['ping', param, '1', host], shell=True).decode("utf-8")
    # replyInfo = hostInfo.split("\n")
    # replyInfo = replyInfo[2]

    isHostLive = subprocess.call(command) == 0
    print("\n", flush=True)  # flush is kinda hacky workaround for above fix
    return isHostLive


def ftpRecon(host, user, password):
    """ recon ftp server once password is found """
    try:
        ftp = ftplib.FTP(host)
        ftp.login(user, password)
        welcome = ftp.getwelcome()
        ftpDir = ftp.dir()
        ftp.quit()
        print(" \n-------------------SCAN-REPORT-------------------")
        print("[+] FTP service: " + welcome + "\n")
        print("[+] Dir: " + ftpDir)
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


def ftpModule(tgtHost):
    """Main module for ftp service tools"""

    print('\n')
    targetHostAddress = tgtHost
    # get input for user name / list.txt
    userName = input('Enter FTP UserName: ')

    passwordsFilePath = "../Lists/" + \
        input('Enter name of password list file: ')

    # TODO: refactor to remove default / handle clean file error

    print('[+] Using default password for ' + targetHostAddress)
    if connect(targetHostAddress, userName, 'admin'):
        print("\n")
        print("------------DEFAULT-LOGIN-FOUND-------------------")
        print("\n")
        print("[+] FTP Login succeeded on host " + targetHostAddress)
        print("[+] UserName: " + userName)
        print("[+] Password: admin")
        print("-------------------------------------------------")
        print("\n")
        ftpRecon(targetHostAddress, userName, "admin")
    else:
        print('[-] FTP default login failed on host')

        # try brute force using dictionary file
        passwordsfile = open(passwordsFilePath, 'r')

        for line in passwordsfile.readlines():
            # clean lines in dictionary file
            password = line.strip('\r').strip('\n')

            if connect(targetHostAddress, userName, password):
                # password found
                print("\n")
                print("-------------------LOGIN-FOUND-------------------")
                print("\n")
                print("[+] FTP Login succeeded on host " + targetHostAddress)
                print("[+] UserName: " + userName)
                print("[+] Password: " + password)
                print("-------------------SCAN-RESULTS------------------")
                print("\n")
                ftpRecon(targetHostAddress, userName, password)
                print("\n")
                exit(0)

            else:
                # password NOT found
                print("\n")
                print("[-] FTP Login failed on host " + targetHostAddress)
                print("[-] UserName: " + userName)
                print("[-] Password: " + password)
                print("-------------------------------------------------")
        else:
            print("[-] Error: Connection failed!")
            exit(0)


def ipRange(start_ip, end_ip):
    """
    enumerates target ip addresses from a range

    Args:

        start ip address (string)
        end ip address (string)

    Returns: list of all ip addresses in range (list)
    """

    # TODO: fix this and add arg parse for target range
    # i.e x.x.x.100-254

    print(" [+] starting ip range...\n", start_ip, end_ip, "\n")
    start = list(map(int, start_ip.split(".")))
    # 12.13.14.15 => [12,13,14,15]
    end = list(map(int, end_ip.split(".")))
    print(start, " to ", end)
    temp = start
    ip_range = []

    ip_range.append(start_ip)
    while temp != end:
        start[3] += 1
        for i in (3, 2, 1):
            if temp[i] == 256:
                temp[i] = 0
                temp[i - 1] += 1
                print("[+] Adding to list...")
        ip_range.append(".".join(map(str, temp)))
    print("[+] Scan range created from ", start, " to ", end)
    print("[+] ", len(ip_range), " IP addresses to scan")
    return ip_range


def printBanner(connSock, tgtPort, tgtHost, isConnectScan):
    """
    module that prints banner info from port if open

    Args:

    Returns: 

    """

    # Note: Needs refactor => mv ftp to new function

    print(connSock, tgtPort, tgtHost, isConnectScan)
    if isConnectScan:
        # try to brute force FTP connection
        try:
            if tgtPort == 80:
                connSock.send("GET HTTP/1.1 \r\n")
            elif tgtPort == 21:
                ftpModule(tgtHost)
            else:
                # if not port 80 then just send a carriage return
                connSock.send("\r\n")
            # receive data from the target, number is bytes for the buffer size
            results = connSock.recv(4096)
            # print the banner
            print('[+] Banner:\n' + str(results))
        except:
            # if no banner, send fail msg
            print('[-] Banner not available')
    else:
        try:
            # send data to the target, if port 80 then send GET HTTP
            if tgtPort == 80:
                connSock.send("GET HTTP/1.1 \r\n")
            else:
                # if not port 80 then just send a carriage return
                connSock.send("\r\n")
            # receive data from the target, number is bytes for the buffer size
            results = connSock.recv(4096)
            # print the banner
            print('[+] Banner:\n' + str(results))
        except:
            # if no banner, send fail msg
            print('[-] Banner not available!')


def connScan(tgtHost, tgtPort, isConnectScan):
    """module connects to ports and prints response msg"""
    try:
        # create the socket object
        connSock = socket(AF_INET, SOCK_STREAM)
        # try to connect with the target
        connSock.connect((tgtHost, tgtPort))
        print("[+] tcp port {} open".format(str(tgtPort)))
        # printBanner(connSock, tgtPort, tgtHost, isConnectScan)
    except:
        # print failure results
        print("[-] tcp port {} closed".format(str(tgtPort)), end="\r", flush=True)
        pass
    finally:
        # close the socket object
        connSock.close()


def udp_connScan(tgtHost, port):
    """"
    connection scanner that uses UDP not TCP

    Args: 
        target host (string)
        target port (int)

    Returns: obj (dict)
    """
    try:
        # create socket with AF_INET (ipv4) & Datagram (UDP)
        connSock = socket(AF_INET, SOCK_DGRAM)
        # try to connect with host
        connSock.connect(tgtHost, port)
        response = {
            "open": True,
            "msg": "[+] UDP port {} open".format(str(port))
            }
        return response
        # printBanner(connSock, port, tgtHost)
    except:
        response = {"open": False,
        "msg": "[-] UDP port {} closed".format(str(port))
        }
        return response


def resolveHost(tgtHost, tgtPorts, isConnectScan, isUdp):
    """
    Resolves the hostname / target ip 
    """

    print("\n[+] Starting Hostname IP resolution...\n")
    sleep(1)

    try:
        # get ip from domain, else throw error msg
        tgtIP = gethostbyname(str(tgtHost))
    except:
        print("[-] Error: Unknown Host")
        exit(0)

    try:
        # print the resolved domain, or the ip if no resolution
        tgtName = gethostbyaddr(tgtIP)
        print("-------- Scanning : " + tgtName[0] + " -----\n")
    except:
        print("-------- Scanning : " + tgtIP + " -----\n")

    # set default timeout and ICMP ping host
    setdefaulttimeout(1)
    canPingHost = pingHost(tgtIP)
    # if host is live print response
    if canPingHost:
        print("[+] Host responds to ICMP Ping")
    else:
        print("[-] No ICMP Ping response ")

    # check protocol and run port scan loop
    if isUdp:
        print("\n[+] Starting UDP Scan...\n")
        for port in tgtPorts:
            port = int(port)
            results = udp_connScan(tgtHost, port)
            sleep(.06)
            # if open print; if closed print then flush stdout
            if results["open"] == True:
                input("fire")
                print(results["msg"])
            else:
                print("\r" + results["msg"], end="")
        print("\n[+] Completed UDP Scan.\n")
    
    print("\n[+] Starting TCP Scan...\n")
    # then run the tcp port scan loop
    for port in tgtPorts:
        port = int(port)
        connScan(tgtHost, port, isConnectScan)
    print("\n[+] Completed TCP Scan.\n")


def mgmtModule(ipv4Ipaddress, ipv4HostList, portNumbers, isNetworkScan, isConnectScan, isUdp):
    """
    direct activity and control program using top level args 
    """
    
    if isNetworkScan:
        # network scan, loop through address range
        random.shuffle(ipv4HostList)
        for addr in ipv4HostList:
            resolveHost(addr, portNumbers, isConnectScan, isUdp)
    else:
        # not a network, scan single IP address
        resolveHost(ipv4Ipaddress, portNumbers, isConnectScan, isUdp)


def domainCheck(ipv4Ipaddress):
    """
    Attempt to resolve hostname if domain is target

    Input: target param (string)

    Returns: Target address (string) 
    """
    domainCheck = ipv4Ipaddress.split(".")
    hostName = gethostbyname(str(ipv4Ipaddress))

    try:
        if domainCheck[1] == "com" or "net" or "org" or "io" or "gov" or "edu":
            # domain passed && network scan flag > get ip > generate network > portscan loop
            domainIP = gethostbyname(str(ipv4Ipaddress))
            ipv4Ipaddress = domainIP
    except IndexError:
        isHostname = input("[-] Is target address a hostname? y/n ")
        if isHostname == "y":
            ipv4Ipaddress = hostName
        else:
            print("[-] ERROR: address cannot be resolved as IP, Domain or Host")
            exit(0)

    return ipv4Ipaddress


def networkOption(ipv4Ipaddress, ipv4HostList):
    """
    Top level param equals a target range of X.X.X.1-254

    Inputs: target ip address (string), ip address list (list)

    Returns: ip address list (list)
    """
    original_param = ipv4Ipaddress
    ipv4Ipaddress = domainCheck(ipv4Ipaddress)
    checkHostBit = list(map(int, ipv4Ipaddress.split(".")))
    # Reset last bit of ip addr
    # 127.0.0.34 ==> 127.0.0.1
    if checkHostBit[3] > 0:
        checkHostBit[3] = 1

    startNetIp = ipaddress.ip_address(
        str(checkHostBit[0]) + "." + str(checkHostBit[1]) + "." + str(checkHostBit[2]) + "." + str(
            checkHostBit[3]))
    endNetIp = ipaddress.ip_address(
        str(checkHostBit[0]) + "." + str(checkHostBit[1]) + "." + str(checkHostBit[2]) + "." + str(254))
    print("[+] Network scan engaged, scanning targets from: " +
          str(startNetIp) + " to " + str(endNetIp))

    net_check = input("[?] Network scans are very slow. Proceed anyway? y/n\n")
    if net_check == "y":
        pass
    else:
        input("Press any key to exit...")
        exit(0)

    for targetAddress in range(int(startNetIp), int(endNetIp)):
        ipv4HostList.append(ipaddress.IPv4Address(targetAddress))
    return ipv4HostList


def portParse(portNumbers):
    """
    Parse port ranges into single array

    Input: array of ports : [80, 8000-8888]

    Returns: array of ports : [80,8000,8001,8002,...]
    """
    for port in portNumbers:
        try:
            # check for number 22 vs range 22-26
            port_int = int(port)
            port = port_int
        except ValueError:
            port_split = port.split("-")
            port_range = range(int(port_split[0]), int(port_split[1]))
            portNumbers.remove(port)
            for new_port in port_range:
                portNumbers.append(new_port)
    # return is to handle basic scan calls from serpent.py
    return portNumbers


def parse():
    """
    parse top level arguments 
    """

    parser = argparse.ArgumentParser(prog='scanner.py',
                                     description='''Simple Wireless Network Utility''',
                                     epilog='''Created by K''',
                                     usage='%(prog)s [-h] address [-p] [port-port,port,+] [-n] [-c]'
                                     )
    parser.add_argument("address", type=str,
                        help="Target Address : 8.8.8.8 or google.com")
    parser.add_argument("-p", "--ports", type=str,
                        default="20-25,80,443,8000,8080", help="Ports to scan : 20-25,80")
    parser.add_argument("-n", "--network", action="store_true",
                        help="Scan network : X.X.X.1-254")
    parser.add_argument("-c", "--connect", action="store_true",
                        help="Connect to discovered hosts")
    parser.add_argument("-u", "--udp", action="store_true",
                        help="include UDP scan")

    args = parser.parse_args()
    ipv4HostList = []

    # store the input args
    isConnectScan = args.connect
    isUdp = args.udp
    ipv4Ipaddress = args.address
    isNetworkScan = args.network
    portNumbers = args.ports.split(",")

    if isNetworkScan:
        ipv4HostList = networkOption(ipv4Ipaddress, ipv4HostList)
    else:
        ipv4HostList.append(ipv4Ipaddress)

    # call the port parse module to handle port numbers
    parsed_port_numbers = portParse(portNumbers)
    mgmtModule(ipv4Ipaddress, ipv4HostList, parsed_port_numbers,
               isNetworkScan, isConnectScan, isUdp)


def main():
    # Parse args passed in then run mgmt module
    parse()


if __name__ == '__main__':
    # call the main function
    main()
