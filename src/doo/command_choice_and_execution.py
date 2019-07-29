#!/usr/bin/env python
# -*- coding: UTF8 -*-

import sys
import subprocess
#from subprocess import run
from shared_data_and_options import *
from print_table import print_command_menu


def execute(choice):
    id = data.keys_to_id.get(choice)
    if id == None:
        print(term_mode.TITLERED+"id '{}' doesn't exist. Abort.".format(choice)+term_mode.NORMAL)
        return 0
    else:
        (keys_list,comment,command) = data.commands[id]
        if options.no_confirm:
            if options.verbose:
                print(term_mode.NORMAL + term_mode.YELLOW + 'Running command: '+ term_mode.NORMAL+'> '  + command + term_mode.NORMAL)
            subprocess.run([command],shell=True)
        else:
            confirmation = input(term_mode.NORMAL + term_mode.YELLOW + 'Run command ? '+ term_mode.NORMAL+'> '  + command +' '+ term_mode.TITLEYELLOW  + '[Y/n]' + term_mode.NORMAL)
            if confirmation:
                if confirmation[0] in 'nN':
                    if options.verbose:
                        print('Abort')
                else:
                    subprocess.run([command],shell=True)
            else:
                subprocess.run([command],shell=True)
    return 1

def choose_command():
    choice = input(term_mode.YELLOW + 'Enter id [or (q)uit] :'+ term_mode.NORMAL+' '+ term_mode.BLUE+ term_mode.BOLD).strip()
    print(term_mode.NORMAL)
    if not choice:
        if options.has_default_command:
            choice='default'
        else:
            if options.verbose:
                print('No choice made.')
    if choice:
        if options.verbose:
            print(term_mode.NORMAL + 'Choice is : ',choice)
        if choice in ["quit","q","exit"]:
            sys.exit(0) # or 1, or whatever
        else:
            execute(choice)
    else:
        # No choice made and no default command, so doing nothing
        if options.verbose:
            print('No command to execute.')
        pass

def user_choice():
    print_command_menu()
    choose_command()

def ask_then_exit_or_choice(question):
    ans = input(term_mode.YELLOW + question + ' ' + term_mode.NORMAL+' '+ term_mode.TITLEYELLOW  + '[Y/n]' + term_mode.NORMAL)
    if ans and (ans[0] in 'nN'):
         if options.verbose:
            print('Exit')
         sys.exit(0) # or 1, or whatever
    else:
        user_choice()
