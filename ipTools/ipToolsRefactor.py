"""Automated wireless network utility
Usage: ipTools.py [-h]
"""

# IMPORT MODULES
import argparse
from socket import *
import ipaddress
import ftplib



def recon():
    """run scans and add results to report file"""


def reports():
    """view, save, and export scan reports"""


def banner_print(text_string):
    """print the input as a banner on the terminal"""
    banner_size = len(text_string)


def setup():
    """create a report or edit settings"""

    # print SETUP banner
    print("***********")
    print("*  SETUP  *")
    print("")
    print("[1] Create a Report")
    print("[2] Edit Settings")
    print("")

    # grab user input, handle bad selections
    setup_input = input("Please Enter a Number: ")
    if setup_input == "1":
        # create a new report, scan_profile or custom
        x = 0
    elif setup_input == "2":
        # edit the scan profiles / ipTools.config text files
        x = 0
    else:
        # bad selection, try again
        print("[-] ERROR: Bad selection, Try Again.")
        setup()


def main():
    """run setup module to begin interactive utility"""
    print('[+] Starting Network Scanner... ')
    setup()


if __name__ == '__main__':
    # call the main function
    main()
