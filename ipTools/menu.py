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


def ban(text, style_character='*'):
    """Frame the name with the style_character."""

    frame_line = style_character * (len(text) + 10)
    print(frame_line)
    time.sleep(0.2)
    print('{0} {1} {0}'.format(style_character, text))
    time.sleep(0.2)
    print(frame_line)
    time.sleep(0.2)



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
    user_option = input("""
    
    [1] Scanner
    [2] Servers
    [3] Sniffers
    
    Select an option to continue...
    
    >""")
    # welcome msg => help msg => main options => run


#################################################################################


def main():
    # Parse args passed in then run mgmt module
    parse()


if __name__ == '__main__':
    # call the main function
    main()
