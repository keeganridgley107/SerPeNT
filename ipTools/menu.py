
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
    parser.add_argument("-u", "--udp", action="store_true", help="include UDP scan")

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
    portParse(portNumbers)
    mgmtModule(ipv4Ipaddress, ipv4HostList, portNumbers, isNetworkScan, isConnectScan, isUdp)


def main():
    # Parse args passed in then run mgmt module
    parse()


if __name__ == '__main__':
    # call the main function
    main()
