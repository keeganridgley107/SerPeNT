"""Automated wireless network utility
Usage: ipTools.py [-h] ADDRESS [-n] [-p] <PORT,PORT,+>
"""

# IMPORT MODULES
import argparse
from socket import *
import ipaddress
import ftplib
import random
from platform import system as system_name  # Returns the system/OS name
from subprocess import call as system_call  # Execute a shell command

###########################
# Main TODO: add argv for passive / active ; tie to connect or print open ports logic
###########################

##########################################################################################
# CURRENT MODULES : network scan / port scan / ftp password brute-force
##########################################################################################


def pingHost(host):
    """
    Returns True if host (str) responds to a ping request.
    Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
    """
    # TODO: hide ping system_call results, print isHostLive Y or N

    # Ping command count option as function of OS
    param = '-n' if system_name().lower() == 'windows' else '-c'

    # Building the command. "ping -c 1 google.com" for Unix || "ping -n 1 google.com" for windows
    command = ['ping', param, '1', host]

    # Pinging
    isHostLive = system_call(command) == 0
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
        print("[+] FTP service: " + welcome)
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
    """Main module for ftp server tools"""

    print('')
    targetHostAddress = tgtHost
    userName = input('Enter FTP UserName: ')
    passwordsFilePath = input('Enter path to Passwords.txt file: ')

    # TODO: refactor to remove default creds => manual or dict.txt for both pass/user

    print('[+] Using default password for ' + targetHostAddress)
    if connect(targetHostAddress, userName, 'admin'):
        print("")
        print("------------DEFAULT-LOGIN-FOUND-------------------")
        print("")
        print("[+] FTP Login succeeded on host " + targetHostAddress)
        print("[+] UserName: " + userName)
        print("[+] Password: admin")
        print("-------------------------------------------------")
        print("")
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
                print("")
                print("-------------------LOGIN-FOUND-------------------")
                print("")
                print("[+] FTP Login succeeded on host " + targetHostAddress)
                print("[+] UserName: " + userName)
                print("[+] Password: " + password)
                print("-------------------SCAN-RESULTS------------------")
                print("")
                ftpRecon(targetHostAddress, userName, password)
                print("")
                exit(0)

            else:
                # password NOT found
                print("")
                print("[-] FTP Login failed on host")
                print("[-] UserName: " + userName)
                print("[-] Password: " + password)
                print("-------------------------------------------------")
        else:
            print("[-] Error: Could not clean dict file!")


def ipRange(start_ip, end_ip):
    """enumerates ip addresses from a range"""
    # currently creates a full LAN scan from any ip passed in
    # TODO: needs logic to handle range scans i.e "10.2.24.26-206"
    start = list(map(int, start_ip.split(".")))
    # 12.13.14.15 => [12,13,14,15]
    end = list(map(int, end_ip.split(".")))

    temp = start
    ip_range = []

    ip_range.append(start_ip)
    while temp != end:
        start[3] += 1
        for i in (3, 2, 1):
            if temp[i] == 256:
                temp[i] = 0
                temp[i - 1] += 1
        ip_range.append(".".join(map(str, temp)))
    print("[+] Scan range created from ", start, " to ", end)
    print("[+] ", len(ip_range), " IP addresses to scan")
    return ip_range


def printBanner(connSock, tgtPort, tgtHost, isConnectScan):
    """module that prints banner info from port if open"""
    if isConnectScan:
        try:
            # send data to the target, if port 80 then send GET HTTP

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
            print('[-] Banner not available')


def connScan(tgtHost, tgtPort):
    """module connects to ports and prints response msg"""
    try:
        # create the socket object
        connSock = socket(AF_INET, SOCK_STREAM)
        # try to connect with the target
        connSock.connect((tgtHost, tgtPort))
        print('[+] tcp port %d open' % tgtPort)
        printBanner(connSock, tgtPort, tgtHost)
    except:
        # print failure results
        print('[-] tcp port %d closed' % tgtPort)
    finally:
        # close the socket object
        connSock.close()


def resolveHost(tgtHost, tgtPorts, isConnectScan):
    """ Resolves the hostname / target ip """

    try:
        # get ip from domain, else throw error msg
        tgtIP = gethostbyname(str(tgtHost))
    except:
        print("[-] Error: Unknown Host")
        exit(0)

    try:
        # print the resolved domain, or the ip if no resolution
        tgtName = gethostbyaddr(tgtIP)
        print("[+] Hostname IP resolution")
        print("-------- Scan Result for: " + tgtName[0] + " -----")
    except:
        print("[-} Cannot resolve hostname")
        print("-------- Scan Result for: " + tgtIP + " -----")

    setdefaulttimeout(1)

    canPingHost = pingHost(tgtIP)
    if canPingHost:
        print("[+] Host responds to ICMP Ping ")
        for port in tgtPorts:
            connScan(tgtHost, int(port))
    else:
        print("[-] No ICMP Ping response ")


def mgmtModule(ipv4Ipaddress, ipv4HostList, portNumbers, isNetworkScan, isConnectScan):
    """ direct activity and control program using top level args """

    if isNetworkScan:
        # network scan, loop through address range
        random.shuffle(ipv4HostList)
        for addr in ipv4HostList:
            resolveHost(addr, portNumbers, isConnectScan)
    else:
        # not a network, scan single IP address
        resolveHost(ipv4Ipaddress, portNumbers, isConnectScan)


def domainCheck(ipv4Ipaddress):

    # check for domain name && network scan flag
    domainCheck = ipv4Ipaddress.split(".")
    hostName = gethostbyname(str(ipv4Ipaddress))

    try:
        if domainCheck[1] == "com" or "net" or "org":
            # domain passed && network scan flag > get ip > generate network > portscan loop
            domainIP = gethostbyname(str(ipv4Ipaddress))
            ipv4Ipaddress = domainIP
    except IndexError:
        isHostname = input("[-] Is target address a hostname? y/n ")
        if isHostname == "y":
            ipv4Ipaddress = hostName
        else:
            print("[-] ERROR: address cannot be resolved as IP, Domain or Host")

    return ipv4Ipaddress


def networkOption(ipv4Ipaddress, ipv4HostList):
    """check network scan option"""

    ipv4Ipaddress = domainCheck(ipv4Ipaddress)
    checkHostBit = list(map(int, ipv4Ipaddress.split(".")))
    if checkHostBit[3] > 0:
        # reset the host bit if the network flag is true
        checkHostBit[3] = 0

    # network address passed in and network flag = true
    startNetIp = ipaddress.ip_address(
        str(checkHostBit[0]) + "." + str(checkHostBit[1]) + "." + str(checkHostBit[2]) + "." + str(
            checkHostBit[3]))
    endNetIp = ipaddress.ip_address(
        str(checkHostBit[0]) + "." + str(checkHostBit[1]) + "." + str(checkHostBit[2]) + "." + str(254))
    print("[+] Network scan engaged, scanning targets from: " + str(startNetIp) + " to " + str(endNetIp))

    for targetAddress in range(int(startNetIp), int(endNetIp)):
        ipv4HostList.append(ipaddress.IPv4Address(targetAddress))
    print(ipv4HostList)
    return ipv4HostList

def portParse(portNumbers):
    """parse the port numbers out of input args"""
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


def parse():
    """parse any arguments passed into the cmd line"""

    parser = argparse.ArgumentParser(prog='ipTools.py',
                                     description='''Simple Wireless Network Utility''',
                                     epilog='''Created by K''',
                                     usage='%(prog)s [-h] address [-p] [port-port,port,+] [-n] [-c]'
                                     )
    parser.add_argument("address", type=str, help="Target Address : 8.8.8.8 or google.com")
    parser.add_argument("-p", "--ports", type=str, default="20-25,80,443,8000,8080", help="Ports to scan : 20-25,80")
    parser.add_argument("-n", "--network", action="store_true", help="Scan network : X.X.X.1-254")
    parser.add_argument("-c", "--connect", action="store_true", help="Connect to discovered hosts")

    args = parser.parse_args()

    ipv4HostList = []

    # store the input args
    isConnectScan = args.connect
    ipv4Ipaddress = args.address
    isNetworkScan = args.network
    portNumbers = args.ports.split(",")

    if isNetworkScan:
        ipv4HostList = networkOption(ipv4Ipaddress, ipv4HostList)
    else:
        ipv4HostList.append(ipv4Ipaddress)
    # call the port parse module to handle port numbers
    portParse(portNumbers)
    # print("Sent to mgmt module:\n")
    # print(ipv4Ipaddress, "\n", ipv4HostList, "\n")
    # print(portNumbers, "\n", isNetworkScan, "\n", isConnectScan)
    mgmtModule(ipv4Ipaddress, ipv4HostList, portNumbers, isNetworkScan, isConnectScan)


def main():
    # Parse args passed in then run mgmt module
    parse()


if __name__ == '__main__':
    # call the main function
    main()
