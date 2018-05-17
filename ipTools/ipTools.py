"""Automated wireless network utility
Usage: ipTools.py [-h] ADDRESS [-n] [-p] <PORT,PORT,+>
"""


import argparse
from socket import *
import ipaddress
import ftplib


##########################################################################################
# CURRENT MODULES : network scan / port scan / ftp password brute-force
##########################################################################################

def ftpRecon(host, user, password):
    """ recon ftp server once password is found"""
    try:
        ftp = ftplib.FTP(host)
        ftp.login(user, password)
        welcome = ftp.getwelcome()
        ftpDir = ftp.dir()
        ftp.quit()
        print("-------------------SCAN-REPORT-------------------")
        print("[+] FTP service: " + welcome)
        print("[+] Dir: " + ftpDir)
        print("")


    except:
        # error
        x = "useless"


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


    print('[+] Using default password for ' + targetHostAddress)
    if connect(targetHostAddress, userName, 'admin'):
        print("")
        print("-------------------LOGIN-FOUND-------------------")
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

        # open dictionary file passwords.txt
        passwordsfile = open(passwordsFilePath, 'r')

        for line in passwordsfile.readlines():
            # clean lines in dictionary file
            password = line.strip('\r').strip('\n')
            # print("[+] Testing: " + str(password))

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
            pass


def ipRange(start_ip, end_ip):
    """enumerates ip addresses from a range"""
    # currently creates a full LAN scan from any ip passed in
    # TODO: needs logic to create partial network scans i.e "10.2.24.26-206"
    # TODO: create module to create port ranges i.e. 20-24, 80, 8000-8080
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


def printBanner(connSock, tgtPort, tgtHost):
    """module that prints banner info from port if open"""
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


def portScan(tgtHost, tgtPorts):
    """ portScan is a badly named module """
    # todo: rename this module to resolveHost or something

    try:
        # get ip from domain, if not valid throw error msg
        tgtIP = gethostbyname(str(tgtHost))
    except:
        print("[-] Error: Unknown Host")
        exit(0)

    try:
        # print the resolved domain, or the ip if no resolution
        tgtName = gethostbyaddr(tgtIP)
        print("-------- Scan Result for: " + tgtName[0] + " -----")
    except:
        print("-------- Scan Result for: " + tgtIP + " -----")

    setdefaulttimeout(1)

    for port in tgtPorts:
        connScan(tgtHost, int(port))


def mgmtModule(ipv4Ipaddress, ipv4AddrRange, ipv4HostList, portNumbers):
    """ direct activity and control program """

    if len(ipv4HostList) == 1:
        # not a network, scan single IP address
        portScan(ipv4Ipaddress, portNumbers)
    else:
        # network scan, loop through address range
        for addr in ipv4HostList:
            portScan(addr, portNumbers)


def main():
    # Parse args passed in then run mgmt module
    parse()


def parse():
    """parse any arguments passed into the cmd line"""

    parser = argparse.ArgumentParser(prog='ipTools.py',
                                     description='''Automated Wireless Network Utility''',
                                     epilog='''Created by KeyMan for The OrthoFi Security Project''',
                                     usage='%(prog)s [-h] address [-n] [-p] [port,port,+]'
                                     )
    parser.add_argument("address", type=str, help="Target Address : 8.8.8.8 or google.com")
    parser.add_argument("-p", "--ports", type=str, default="80", help="Ports to scan : 22,23,80")
    parser.add_argument("-n", "--network", action="store_true", help="Scan network")
    args = parser.parse_args()

    ipv4HostList = []

    # store the args values with a default port number
    ipv4Ipaddress = args.address
    if args.network:
        # check for domain name && network scan flag
        domainCheck = ipv4Ipaddress.split(".")

        if domainCheck[1] == "com" or "net" or "org":
            # domain passed && network scan flag > get ip > generate network > portscan loop
            domainIP = gethostbyname(str(ipv4Ipaddress))
            ipv4Ipaddress = domainIP

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
        ipv4AddrRange = ipaddress.ip_network(startNetIp, strict=False)

        for targetAddress in range(int(startNetIp), int(endNetIp)):
            ipv4HostList.append(ipaddress.IPv4Address(targetAddress))
    else:
        ipv4AddrRange = ipv4Ipaddress
        # no network flag = single target scan

    portNumbers = args.ports.split(",")

    if len(ipv4HostList) <= 1:
        # if not a network scan, add the single ip in the hostlist
        ipv4HostList.append(ipv4Ipaddress)
    mgmtModule(ipv4Ipaddress, ipv4AddrRange, ipv4HostList, portNumbers)


if __name__ == '__main__':
    # call the main function
    main()
