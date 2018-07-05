"""

Simple wireless network toolkit menu

usage: python menu.py

notes: TODO: import mods/ check fs/ valid input/ args pass/ error handling/

"""

import os
from platform import system as system_name  # Returns the system/OS name
import time
import ipTools as scanner
import tcp_sniff
import bin_sniff
import dir_serve
import v_server


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
        [4] Exit
        """)
    user_option = input('Select an option to continue...\n>')
    print(user_option)
    try:
        if int(user_option) < 4:
            sub_options(int(user_option))
        else:
            print('Goodbye User...')
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
        # END OF SCANNER sub options here
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
            folder_server = dir_serve
            try:
                # run iptools module
                dir_port = int(input("Please enter a port number to serve folder on\n>"))
                user_option = input('Press enter to begin serving contents of /Desktop/html\n>')
                print("[+] Starting Python Folder Server on port %s..." % dir_port)
                folder_server.run(port=dir_port)
            except Exception as e:
                print("[-] Error: Ending Reverse Shell Listener...")
                # handle errors from run module and end socket connection if needed
                time.sleep(1)
                exit(0)
            # LAN FILE SHARING SERVER
            main_options()
        # end server sub_options
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
        # SNIFFERS sub options here
    else:
        ban('Invalid Option', '!')
        time.sleep(1)
        main_options()

    print('Exiting IpTools...')
    exit(0)

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
