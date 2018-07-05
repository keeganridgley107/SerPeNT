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
        # ip_scan.mgmtModule()

        exit(0)
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
            # CODE GOES HERE
            # REVERSE SHELL SERVER OPTIONS
            exit(0)
        elif user_option == 1:
            # LAN FILE SHARING SERVER
            # CODE GOES HERE
            # LAN FILE SHARING SERVER
            exit(0)
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
            ban("TCP_sniff")
            sniff = tcp_sniff
            try:
                sniff.start_sniffing()
            except KeyboardInterrupt:
                print("[-] Ending the sniffer...")
            # TCP SNIFFER OPTIONS
            exit(0)
        elif user_option == 1:
            # LAN FILE SHARING SERVER
            # CODE GOES HERE
            # LAN FILE SHARING SERVER
            exit(0)
        # SNIFFERS sub options here
    else:
        ban('Invalid Option', '!')
        main_options()

    print('Goodbye User...')
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
