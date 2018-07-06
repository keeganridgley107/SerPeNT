"""

Serpent: Simple wireless network toolkit

usage: python serpent.py

notes: TODO: import mods/ check fs/ valid input/ args pass/ error handling/

"""

import os
from platform import system as system_name  # Returns the system/OS name
import time
import ipTools as scanner
import tcp_sniff
import bin_sniff
import dir_serve3
import v_server
import web_crawl


#################################################################################


def full_path(folder, location='Desktop'):
    """takes in name of folder and location and returns a full path to it"""
    # do a quick OS check then append dir path to location, default is 'Desktop'
    if system_name().lower() == 'windows':
        # else if windows path equals
        path = os.path.join(os.path.join(os.environ['USERPROFILE']), location)
    else:
        # if unix desktop path equals
        path = os.path.join(os.path.join(os.path.expanduser('~')), location)
    dir_path = path + "\\" + folder
    return dir_path


def ban(text, style_character='*', width=37, lines=0):
    """Frame the name with the style_character."""
    print('\n')
    frame_line = style_character * (width - len(text))
    print(frame_line)
    time.sleep(0.1)
    print('{0} {1} {0}'.format(style_character, text).center(width - len(text), '#'))
    time.sleep(0.1)
    print(frame_line)
    for num in range(lines):
        time.sleep(0.1)
        print('\n')
    time.sleep(0.5)


def cls():
    """clear the screen via mass printing newline"""
    print('\n' * 100)


#################################################################################


def main_options():
    """main level menu for user selection"""

    ban('Options', '#')
    print(
        """
        [1] Scanner
        [2] Servers
        [3] Sniffers
        [4] Scrapers
        [5] Exit
        """)
    user_option = input('Select an option to continue...\n>')
    try:
        if int(user_option) < 5:
            sub_options(int(user_option))
        else:
            print('Exiting IpTools...')
            exit(0)
    except ValueError:
        main_options()


def sub_options(user_option):
    """handle the main options and pass args to modules"""

    if user_option == 1:
        # SCANNER sub options here

        ban('Scanner', '#')
        # show banner and load scanner module
        ip_scan = scanner

        # TODO: parse inputs to match call sig from scanner
        # 'scanner address [-p] [port-port,port,+] [-n] [-c]'

        is_lan_scan = input('Target or LAN scan? T/L\n>')
        is_connect_scan = input('Attempt brute force connection to live hosts? y/n\n>')
        address = input('Enter ip address to target:\n>')
        port_numbers = input('Enter port numbers to target:\n>')

        # TODO: add parser into menu sub_option logic, pass parsed args to scanner.mgmtModule()

        main_options()
    # SCANNER sub options
    elif user_option == 2:
        # SERVERS sub options here

        ban('Servers', '#', lines=1)
        # list server modules
        print(
            """
            [1] LAN File Sharing Server
            [2] Reverse Shell Server (PyRat Listener)
            [3] Back
            """)
        user_option = input('Select an option to continue...\n>')
        user_option = int(user_option)
        # convert int from str
        if user_option == 3:
            # user selected back
            main_options()
        elif user_option == 2:
            # REVERSE SHELL SERVER OPTIONS
            ban('Reverse Shell Server')
            time.sleep(1)
            py_rat_server = v_server
            try:
                # run iptools module
                port_number = int(input('Enter a port for server to listen on\n>'))
                print("[+] Starting Python Reverse Shell Listener on port %s..." % port_number)
                py_rat_server.main(port_number)
            except Exception as e:
                print("[-] Error: Ending Reverse Shell Listener...")
                # handle errors from run module and end socket connection if needed
                time.sleep(1)
                exit(0)
            # REVERSE SHELL SERVER OPTIONS
            main_options()
        elif user_option == 1:
            # LAN FILE SHARING SERVER
            ban('File Sharing Server')
            time.sleep(1)
            folder_server = dir_serve3
            try:
                # run iptools module
                # dir_port = int(input("Please enter a port number to serve folder on\n>"))
                user_option = input('Press enter to begin serving contents of /home\n>')
                # print("[+] Starting Python Folder Server on port %s..." % dir_port)
                folder_server.run()
            except Exception as e:
                print("[-] Error: Ending Folder Server...")
                # handle errors from run module and end socket connection if needed
                time.sleep(1)
                main_options()
            # LAN FILE SHARING SERVER
            main_options()
    # SERVER sub options
    elif user_option == 3:
        # SNIFFERS sub options here
        ban('Sniffers', '#')
        print(
            """
            [1] Binary Traffic Sniffer
            [2] TCP/ICMP/UDP Traffic Sniffer
            [3] Back
            """)
        user_option = input('Select an option to continue...\n>')
        user_option = int(user_option)
        # convert int from str
        if user_option == 3:
            # user selected back
            main_options()
        elif user_option == 2:
            # TCP SNIFFER OPTIONS
            ban("Traffic Sniffer")
            sniff = tcp_sniff
            press_key = input('Press Enter to begin Traffic Sniffer...\n>')
            try:
                sniff.start_sniffing()
            except (KeyboardInterrupt, OSError):
                print("[-] Error: Ending Traffic Sniffer...")
                time.sleep(1)
            # TCP SNIFFER OPTIONS
            main_options()
        elif user_option == 1:
            # BINARY SNIFFER OPTIONS
            ban("Binary Sniffer")
            time.sleep(1)
            sniff = bin_sniff
            press_key = input('Press Enter to begin Binary Sniffer...\n>')
            try:
                sniff.start_sniffing()
                # run iptools module
            except (KeyboardInterrupt, OSError):
                print("[-] Error: Ending Binary Sniffer...")
                time.sleep(1)
            # BINARY SNIFFER OPTIONS
            main_options()
    # SNIFFERS sub options
    elif user_option == 4:
        # Scrapers sub options here

        ban('Scrapers', '#', lines=1)
        # list server modules
        print(
            """
            [1] HTML links -> CSV
            [2] Back
            """)
        user_option = input('Select an option to continue...\n>')
        user_option = int(user_option)
        # convert int from str
        if user_option == 2:
            # user selected back
            main_options()
        elif user_option == 1:
            # SCRAPER SUB OPTIONS
            ban('HTML Link Scraper')
            time.sleep(1)
            # create instance of iptool in local scope
            link_scraper = web_crawl
            try:
                # run iptools module
                link_scraper.get_site()
                ban("WIN")
                print("[+] Links added to /ip_tools/index.csv file")
                time.sleep(0.2)
                print("[+] Returning to main menu...")
                time.sleep(1)
                cls()
            except Exception as e:
                print("[-] Error: Ending HTML Link Scraper...")
                # handle errors from run module and end socket connection if needed
                print("[-] Error Message: %s " % e)
                time.sleep(1)
                # no need to kill menu.py, return to main to try again or exit gracefully
                main_options()
            # SCRAPER SUB OPTIONS
            main_options()

        # end HTML_scraper sub options
    # SCRAPER sub options
    else:
        ban('Invalid Option', '!')
        time.sleep(1)
        main_options()

    # hacky error handler for cli calls
    main_options()


#################################################################################


def welcome():
    """display banner clear screen & sleep thread 1 sec"""
    cls()
    ban("\\= IPTOOLS =/", '#')
    time.sleep(1)
    print('\n')
    time.sleep(0.1)
    print('\n')
    time.sleep(0.1)
    ban("= Created by K =", '#', lines=2)
    time.sleep(1)
    print('\n')
    time.sleep(0.1)
    print('\n')
    time.sleep(0.1)
    print('\n')
    time.sleep(0.1)
    print('\n')
    time.sleep(0.1)
    cls()


def main():
    # get user input passed in then run mgmt module
    welcome()
    main_options()


if __name__ == '__main__':
    # call the main function
    main()
