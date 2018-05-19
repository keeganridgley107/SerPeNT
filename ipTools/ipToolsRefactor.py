"""interactive wireless network utility
Usage: ipTools.py [-h]
"""

# IMPORT MODULES
import argparse
from socket import *
import ipaddress
import ftplib


###############################################################################
# RECON


def recon():
    """run scans and add results to report file"""


###############################################################################
# REPORTS


def reports():
    """view, save, and export scan reports"""


###############################################################################
# SETUP

def setup():
    """create a report or edit settings"""

    # print SETUP banner
    banner_print("SETUP")
    # print setup options
    print("[1] Create a Report")
    print("[2] Edit Settings")
    print("")
    # TODO: refactor options menus into function => print_options(options, iterator=number)

    # grab user input, handle bad selections
    setup_input = input("[+] Please Enter a Number: ")
    if setup_input == "1":
        # create a new report, scan_profile or custom
        create_report()

    elif setup_input == "2":
        # edit the scan profiles / ipTools.config text files
        x = 0
    else:
        # bad selection, try again
        print("[-] ERROR: Bad selection, Try Again.")
        # user fat fingers = call setup() again
        setup()


def create_report():
    """create a report file using scan_profile or custom params"""

    load_scan_profile = input('[+] Use a Scan Profile? (y or n) ')
    if load_scan_profile == "y":
        # Load scan_profile.txt and list profiles
        scan_profiles = open('Setup_files/ipTools.config', 'r')

        for line in scan_profiles.readlines():
            # clean lines in dictionary file
            config_line = line.strip('\r').strip('\n')
            print("[+] config_line: ", config_line)

################################################################################
# PROGRAM UTILS


def banner_print(text_string, style_character='*'):
    """print the input as a banner on the terminal"""

    frame_line = style_character * (len(text_string) + 4)
    print(frame_line)
    print('{0} {1} {0}'.format(style_character, text_string))
    print(frame_line)
    print("")


################################################################################
# MAIN

def main():
    """run setup module to begin interactive utility"""
    print('[+] Starting Network Utility... ')
    setup()


if __name__ == '__main__':
    # call the main function
    main()
