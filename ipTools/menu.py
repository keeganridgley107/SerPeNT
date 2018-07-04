"""

Simple wireless network toolkit menu

usage: python menu.py

notes: TODO: import mods/ check fs/ valid input/ args pass/ error handling/

"""

import os
from platform import system as system_name  # Returns the system/OS name
import time
import ipTools


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


def ban(text, style_character='*', width=37):
    """Frame the name with the style_character."""
    print('\n')
    frame_line = style_character * (width - len(text))
    print(frame_line)
    time.sleep(0.1)
    print('{0} {1} {0}'.format(style_character, text).center(width - len(text), '#'))
    time.sleep(0.1)
    print(frame_line)
    time.sleep(0.1)
    print('\n')
    time.sleep(0.5)


def cls():
    """clear the screen via mass printing newline"""
    print('\n' * 100)


#################################################################################


def parse():
    """parse any arguments needed then call modules"""

    ban("\\= IPTOOLS =/", '#')
    time.sleep(1)
    cls()
    ban('Options', '#')
    print(
        """
        [1] Scanner
        [2] Servers
        [3] Sniffers
        """)
    user_option = input('Select an option to continue...\n>')
    cls()
    if user_option != 1:
        ban('Invalid Option', '!')
        # bad selection, lets try this again...
        parse()
    main_options(int(user_option))


def main_options(user_option):
    """handle the main options and pass args to modules"""

    if user_option == 1:
        # SCANNER sub options here
        ban('Scanner', '#')

        # handle user_sub_option based on args needed for module

    elif user_option == 2:
        # SERVERS sub options here
        ban('Servers', '#')
    elif user_option == 3:
        # SNIFFERS sub options here
        ban('Sniffers', '#')
    else:
        ban('Invalid Option', '!')
        parse()

    print('Goodbye User...')
    exit(0)

#################################################################################


def main():
    # Parse args passed in then run mgmt module
    parse()


if __name__ == '__main__':
    # call the main function
    main()
