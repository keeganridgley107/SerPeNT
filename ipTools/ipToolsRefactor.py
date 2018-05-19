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


def banner_print(text_string, style_character='*'):
    """print the input as a banner on the terminal"""

    frame_line = style_character * (len(text_string) + 4)
    print(frame_line)
    print('{0} {1} {0}'.format(style_character, text_string))
    print(frame_line)
    print("")


def setup():
    """create a report or edit settings"""

    # print SETUP banner
    banner_print("SETUP")
    # print setup options
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
        # user fat fingers = call setup() again
        setup()

    # setup sub functions
    def create_report():
        """build a new report from scan profile or custom"""
        report = """"""


def main():
    """run setup module to begin interactive utility"""
    print('[+] Starting Network Scanner... ')
    setup()


if __name__ == '__main__':
    # call the main function
    main()
