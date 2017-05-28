#!/usr/bin/env python
# -*- coding: UTF8 -*-
from os.path import expanduser
# for windows compability :
#from colorama import init
#init()


class data:
    commands = {}
    keys_to_id = {}
class global_vars:
    max_keys_width = 0
    max_comment_width = 0
    max_command_width = 0

class options:
    # Default options:
    debug = False
    loop = False
    colors = True
    verbose = False
    no_confirm = False
    add_numeric_key = False
    has_default_command = False

    no_system_install=False
    if no_system_install:
        # Options for testing in devel directory:
        global_config_file_template = 'usr_share/doo.conf'
        command_file_template = 'usr_share/template.doo'
        global_config_dir = expanduser('config/')
    else:
        # The files location in production:
        global_config_file_template = '/usr/share/doo/doo.conf'
        command_file_template = '/usr/share/doo/template.doo'
        global_config_dir = expanduser('~/.config/doo/')
    global_config_file = global_config_dir + 'doo.conf'
    global_command_file = global_config_dir + 'default.doo'
    local_command_file = '.doo'

class term_mode:
   PURPLE      = '\033[95m'
   CYAN        = '\033[96m'
   DARKCYAN    = '\033[36m'
   BLUE        = '\033[94m'
   TITLEBLUE   = '\033[0;37;44m'
   GREEN       = '\033[92m'
   TITLEGREEN  = '\033[0;30;42m'
   TITLE       = '\033[0;30;47m'
   YELLOW      = '\033[93m'
   TITLEYELLOW = '\033[0;30;43m'
   RED         = '\033[91m'
   TITLERED    = '\033[0;37;41m'
   TITLE       = '\033[0;30;47m'
   BOLD        = '\033[1m'
   UNDERLINE   = '\033[4m'
   NORMAL      = '\033[0m'

def remove_colors_and_bold():
   term_mode.PURPLE      = ''
   term_mode.CYAN        = ''
   term_mode.DARKCYAN    = ''
   term_mode.BLUE        = ''
   term_mode.TITLEBLUE   = ''
   term_mode.GREEN       = ''
   term_mode.TITLEGREEN  = ''
   term_mode.TITLE       = ''
   term_mode.YELLOW      = ''
   term_mode.TITLEYELLOW = ''
   term_mode.RED         = ''
   term_mode.TITLERED    = ''
   term_mode.TITLE       = ''
   term_mode.BOLD        = ''
   term_mode.UNDERLINE   = ''
   term_mode.NORMAL      = ''
