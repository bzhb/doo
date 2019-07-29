#!/usr/bin/env python
# -*- coding: UTF8 -*-
import os
import sys
import shutil
from shutil import copyfile
import termios, tty
from shared_data_and_options import *

def adjust_width(s,width):
    if len(s) > width:
        # string needs to be truncated
        if width >= 1:
            return (s[:(width-1)]+'…').ljust(width)
        else:
            # given width is 0 (or negative) return empty string
            return ""
    else:
        return s.ljust(width)

def print_command_menu():
    show_comments = True
    show_commands = True
    #rows, columns = os.popen('stty size', 'r').read().split()
    term = shutil.get_terminal_size((80, 20))
    term_width = term.columns
    term_height = term.lines

    # We assign the optimal width for each field
    if global_vars.max_keys_width < 6:
        keys_field_width = 6 # len("Id(s):")
    else:
        keys_field_width = global_vars.max_keys_width +1 # +1 is for ':'
    if global_vars.max_comment_width == 0:
        comment_field_width = 0 # comment column is not gowing to be displayed
        show_comments = False
    elif global_vars.max_comment_width < 9:
        comment_field_width = 9 # len(" Comment ")
    else:
        comment_field_width = global_vars.max_comment_width +2 # +2 is for space at beginning and end of comment
    if global_vars.max_command_width < 8:
        command_field_width = 9 # len("> Command")
    else:
        command_field_width = global_vars.max_command_width + 2 # +2 is for '> ' at beginning of command

    if options.debug:
        print('Terminal width:',term_width)
        print('Max widths: ', global_vars.max_keys_width,',',global_vars.max_comment_width,',',global_vars.max_command_width)
        print('Fields width: ', keys_field_width,',',comment_field_width,',',command_field_width)

    if  keys_field_width + comment_field_width + command_field_width <= term_width :
        # The table colums fits into the terminal
        if options.debug:
            print('The table fits into the terminal')
    else:
        # though choice here about what to scrap
        if options.debug:
            print("The table doesn't fit into the terminal")
        if keys_field_width <= term_width :
            # we dispay all the keys (it fits)
            remaining_width = term_width - keys_field_width
            if comment_field_width == 0:
                # no comments.
                command_field_width = remaining_width
            else:
                # split the remaing space 30%/70% between comment/command
                comment_field_width = min( comment_field_width , remaining_width*3//10 )
                if comment_field_width < 9:
                    # Not useful to display the comment if column is too small
                    comment_field_width = 0
                    show_comments = False
                remaining_width = remaining_width - comment_field_width
                if command_field_width > remaining_width:
                    command_field_width = remaining_width
                else :
                    # in this case the command_field does not take all of assigned 70%, the remaining space can be used by the comment field
                    comment_field_width = term_width - keys_field_width - command_field_width
                    show_comments = True
                    if comment_field_width < 9:
                        # Not useful to display the comment if column is too small
                        comment_field_width = 0
                        show_comments = False
        else:
            # it is needed to cut into the keys field / comments and commands not displayed
            keys_field_width = term_width
            comment_field_width = 0
            command_field_width = 0
            show_commands = False
            show_comments = False
    if global_vars.max_comment_width == 0:
        show_comments = False
        comment_field_width = 0

    print(term_mode.TITLEBLUE+adjust_width('Id(s)',keys_field_width-1),end=':')
    if show_comments:
        print(term_mode.TITLEGREEN+adjust_width(' Comment ',comment_field_width),end='')
    if show_commands:
        print(term_mode.TITLE+adjust_width('> Command',command_field_width)+term_mode.NORMAL)
    else:
        # return to next line and normal mode
        print(term_mode.NORMAL)
    printed_lines = 1
    for (keys_list,comment,command) in data.commands.values() :
        if printed_lines == term_height-1 :
            # wait for more
            stdinFileDesc = sys.stdin.fileno() #store stdin's file descriptor
            oldStdinTtyAttr = termios.tcgetattr(stdinFileDesc) #save stdin's tty attributes so I can reset it later

            try:
                print(term_mode.TITLEBLUE + "-- More --" + term_mode.NORMAL,end="\r")
                os.system('setterm -cursor off')
                tty.setraw(stdinFileDesc) #set the input mode of stdin so that it gets added to char by char rather than line by line
                char = sys.stdin.read(1) #read 1 byte from stdin (indicating that a key has been pressed)
                if char == "q":
                     if options.verbose:
                        print('Exit')
                     sys.exit(0) # or 1, or whatever
            finally:
                termios.tcsetattr(stdinFileDesc, termios.TCSADRAIN, oldStdinTtyAttr) #reset stdin to its normal behavior
                os.system('setterm -cursor on')
                #print("\r") # bring back the cursor at the beginning of the line (to remove "-- More --")

            printed_lines = 0
        keys_str = ''
        for key in keys_list:
            keys_str += key + ','
        keys_str = keys_str[:-1]
        keys_str = adjust_width(keys_str,keys_field_width -1)
        print(term_mode.BLUE+term_mode.BOLD + keys_str + ':',end=term_mode.NORMAL)
        if show_comments:
            comment = adjust_width(comment,comment_field_width -2)
            print(term_mode.GREEN+' '+comment,end=' ')
        if show_commands:
            command = adjust_width(command,command_field_width -2)
            print(term_mode.NORMAL+'> '+command)
        else:
            # return to next line
            print(term_mode.NORMAL)
        printed_lines += 1
