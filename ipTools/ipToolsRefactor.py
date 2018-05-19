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

    banner_print("Create Report")
    load_scan_profile = input('[+] Use a Scan Profile? (y or n) ')
    if load_scan_profile == "y":
        # Load scan_profile.txt and list profiles
        scan_profiles = open('Setup_files/ipTools.config', 'r')
        scan_profiles_items = scan_profiles.readlines()
        scan_templates = []

        # loop populates scan_templates
        for line in scan_profiles_items:
            # clean lines in dictionary file
            config_line = line.strip('\r').strip('\n')

            if len(config_line) > 2 and config_line[:2] == "$$":
                # scan name = new profile
                scan_name = config_line[2:]
                scan_templates.append({"Scan Name": scan_name})

            elif len(config_line) > 2 and config_line[0] == "$" and config_line[1] != "$":
                # scan option
                scan_option_value = config_line.split("=")
                profile_num = len(scan_templates)
                scan_templates[profile_num - 1][scan_option_value[0]] = scan_option_value[1]
        # list options with number
        for profile in range(0, len(scan_templates)):
            print('[' + str(profile) + ']', ' ', scan_templates[profile]['Scan Name'])
        scan_profiles.close()
        scan_profile_id = input("[+] Please Enter a Number: ")
        if int(scan_profile_id) <= len(scan_templates):
            # valid selection
            print("[+] Selected: ", scan_templates[int(scan_profile_id)]['Scan Name'])
    elif load_scan_profile == "n":
        # TODO: finish custom report creation module
        # create a new report based on custom scan_profile
        # single ip or network scan?
        # ports to scan?
        # passive or active?
        # generate or load dict / rule files for target?
        pass
    else:
        # bad input son. try again.
        banner_print("BAD INPUT")
        create_report()

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
