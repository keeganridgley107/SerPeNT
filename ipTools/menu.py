"""

Simple wireless network toolkit menu

usage: python menu.py

notes: TODO: import mods/ check fs/ valid input/ args pass/ error handling/

"""

import os
from platform import system as system_name  # Returns the system/OS name


def full_path(dir_name, location='Desktop'):
    """takes in a folder on the desktop and returns a full path to it"""
    # do a quick OS check then append dir path to home
    if system_name().lower() == 'windows':
        # else if windows path equals
        desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), location)
    else:
        # if unix desktop path equals
        desktop = os.path.join(os.path.join(os.path.expanduser('~')), location)
    dir_path = desktop + "\\" + dir_name
    return dir_path


def ban(text, style_character='*'):
    """Frame the name with the style_character."""

    frame_line = style_character * (len(text) + 4)
    print(frame_line)
    print('{0} {1} {0}'.format(style_character, text))
    print(frame_line)



def parse():
    """parse any arguments needed then call modules"""
    ban("\\= IPTOOLS =/", '#')
    exit(0)




def main():
    # Parse args passed in then run mgmt module
    parse()


if __name__ == '__main__':
    # call the main function
    main()
