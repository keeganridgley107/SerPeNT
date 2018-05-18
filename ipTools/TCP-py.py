"""template for modules to be added to iptools.py mgmt controller """

import argparse

def main():

    # parse args
    parser = argparse.ArgumentParser(prog='TCP-py',
                                     description='''TCPython IP Address & Port Scanner''',
                                     epilog='''Coded by K as part of PyTools''',
                                     usage='%(prog)s [-h] address [ports]'
                                     )
    parser.add_argument("address", type=str,  help="The IP address / domain : 8.8.8.8 or google.com")
    parser.add_argument("-p", "--ports", type=str, default="80", help="The ports to scan : 22,23,80")
    args = parser.parse_args()

    # store the args values with a default port number
    ipaddress = args.address
    portNumbers = args.ports.split(",")

if __name__ == '__main__':
    # call the main function
    main()
