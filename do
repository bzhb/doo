#!/usr/bin/env python3
# -*- coding: UTF8 -*-

#ifndef DO_PY
#define DO_PY

"""do command
NAME
    do - utility to run user predefined commands

SYNOPSIS
    do [OPTIONS] [ID]

DESCRIPTION
    Read command in the .do file in the local folder and execute the choosen command


COMMAND-LINE AND CONFIG FILES OPTIONS

    --debug
        Debug mode with additional prints

    --config-file=FILE
        Use the specified file instead of .do

    --global_config_file=FILE
        Use the specified file instead of ~/.config/do/do.conf

    -g --no-global-config
        Use only the config in the local folder

    -v --verbose

    -l --loop
        After running a command the program doesn't quit and ask for running a new command, until the user hit q or ^C

    -c --colors

    -f --no-confirm
        No confirmation is asked before running the command

CONFIG FILES
    .do format: each command line should be in the format:
        [id[,alternative_ids]:][comment]>command
    with :
        id : a unique identifier used to identify the command to run. Can contain any printable character. 
        alternative_ids: one or more optional ids separated by a comma.
        comment: an optional comment or description on the command
        command: the actual command to run

    if id is omitted, one will be automatically generated (from the line number and random characters).
    If no id is given when running the do command, the command with identifier "default" is going to be executed

    examples of config:
        0: default command > ls -l
        1, kill the fox > killall firefox
        > ls -a
EXAMPLES
AUTHOR
COPYRIGHT
"""
import os
import shutil
import sys
import subprocess
import getopt
import random
import string

#TODO:
# * nice interrupt with ^C
# * remove Traceback when doing ^C
# * read global config file
# * loop mode
# * parse commandline
# * verify the program is running with python3
# * add a q,quit key in loop mode
# * write the modified key to .do file when there is duplicate keys (option -w ?)
# * add numeric keys to every command (option --numeric-id)
# * write numeric keys into .do files
# * add calculation for the space taken by keys / comment / command
# * put keys in bold font
# * ignore lines with no commands
# * remove empty keys (for instance if there is a trailing comma)
# * use --more if there is not enough lines
# * add Warning when there is no options file in the current directory

# Default options:
#debug = True
debug = False
local_config_file ='.do'
global_config_file ='~/.config/do/do.conf'
no_global_config = False
#verbose = True
verbose = False
#loop = True
loop = False
colors = False
no_confirm = False
shell='zsh'
add_numeric_key_to_every_command = False
shell_width = 100

commands = {}
keys_to_id = {}
max_keys_width = 0
max_comment_width = 0
max_command_width = 0

class term_mode:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   TITLEBLUE = '\033[0;37;44m'
   GREEN = '\033[92m'
   TITLEGREEN = '\033[0;30;42m'
   TITLE = '\033[0;30;47m'
   YELLOW = '\033[93m'
   TITLEYELLOW = '\033[0;30;43m'
   RED = '\033[91m'
   TITLERED = '\033[0;37;41m'
   TITLE = '\033[0;30;47m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   NORMAL = '\033[0m'



def process_options(opts_string):
    pass

def generate_unique_key(key):
    while keys_to_id.get(key) != None:
        # if key is already used, append a random ascii character to the key
        key += random.choice(string.ascii_lowercase)
    return key

def parse_command_file(filename):
    global max_keys_width,max_comment_width,max_command_width
    with open(filename) as command_file:
        for i,line in enumerate(command_file):
            line = line.strip()
            if line == '':
                if verbose:
                    print('line ',i,' is empty. Ignored.')
            elif line[0] == '#':
                # commented lines get ignored
                if verbose:
                    print('line ',i,' is commented. Ignored.')
            elif line[0] == '-':
                # if line is an option line
                process_options(line)
            else:
                #(key_list,comment,command)= parse(line)
                (keys,separator,rest_of_line) = line.partition(':')
                if not separator:
                    # means the separator ':' is not present in the string 
                    # By default we attribute the line number as key for the command
                    rest_of_line = keys
                    keys = str(i)
                elif not keys:
                    # means no keys where given (line starts with ':')
                    # By default we attribute the line number (starting at line 0) as key for the command
                    keys = str(i)
                keys_list = keys.split(',')
                keys_width = 0
                for j,key in enumerate(keys_list) :
                    key = generate_unique_key( key.strip() )
                    keys_width += len(key) + 1 # the +1 is for the comma between keys
                    keys_list[j] = key
                    keys_to_id[key]= i
                if keys_width > 0:
                    keys_width -= 1 # because no comma after last key
                if keys_width > max_keys_width:
                    max_keys_width = keys_width
                (comment,separator,command) = rest_of_line.partition('>')
                if not separator:
                    # If no separator is given, we assume the whole string is just a command
                    command = comment
                    comment = ''
                comment = comment.strip()
                l = len(comment)
                if l > max_comment_width:
                    max_comment_width = l
                command = command.strip()
                l = len(command)
                if l > max_command_width:
                    max_command_width = l
                commands[i] = ( keys_list , comment , command )

def adjust_width(s,width):
    #TODO: in case the string is truncated, add '...'
    return s[:width].ljust(width)

def print_available_commands():
    global max_keys_width,max_comment_width,max_command_width
    keys_field_width = 20
    comment_field_width = 40
    command_field_width = 40
    #TODO: find a smarter way to calculate the width for each field
    #rows, columns = os.popen('stty size', 'r').read().split()
    term = shutil.get_terminal_size((80, 20))
    term_width = term.columns
    if debug:
        print('Terminal width:',term_width)
        print('Max widths: ', max_keys_width,',',max_comment_width,',',max_command_width)
    if max_keys_width + max_comment_width + max_command_width + 3 < term_width :
        # The array lines fill in the terminal
        if debug:
            print('The array fit into the terminal')
        keys_field_width = max_keys_width
        comment_field_width = max_comment_width
        command_field_width = max_command_width
    else:
        # though choice here about what to scrap
        if debug:
            print("The array doesn't fit into the terminal")
        keys_field_width = max_keys_width
        comment_field_width = max_comment_width
        command_field_width = max_command_width
        pass
    show_comments = True
    if max_comment_width == 0:
        show_comments = False
        comment_field_width = 0
    print(term_mode.TITLEBLUE,'Id(s)'.ljust(keys_field_width),end=' :')
    if show_comments:
        print(term_mode.TITLEGREEN,'Comment'.ljust(comment_field_width),end='')
    print(term_mode.TITLE,'> Command'.ljust(command_field_width),term_mode.NORMAL)
    #print(''.ljust(keys_field_width + comment_field_width + command_field_width + 4,'-'))
    for (keys_list,comment,command) in commands.values() :
        keys_str = ''
        for key in keys_list:
            keys_str += key + ','
        keys_str = keys_str[:-1]
        keys_str = adjust_width(keys_str,keys_field_width)
        comment = adjust_width(comment,comment_field_width)
        command = adjust_width(command,command_field_width)
        print(term_mode.BLUE+term_mode.BOLD,keys_str,':',end=term_mode.NORMAL)
        if show_comments:
            print(term_mode.GREEN,'',end=comment)
        print(term_mode.NORMAL,'>',command)

def execute(choice):
    id = keys_to_id.get(choice)
    if id == None:
        print(term_mode.TITLERED,"This id doesn't exist. Abort.")
    else:
        (keys_list,comment,command) = commands[id]
        confirmation = input(term_mode.YELLOW + 'Run command ? '+ term_mode.NORMAL+'> '  + command +' '+ term_mode.TITLEYELLOW  + '[Y/n]' + term_mode.NORMAL)
        if confirmation:
            if confirmation[0] in 'nN':
                if verbose:
                    print('Abort')
            else:
                subprocess.run([command],shell=True)
        else:
            subprocess.run([command],shell=True)

def choose_command():
    choice = input(term_mode.BLUE + term_mode.BOLD + 'Enter id of the command to run:'+ term_mode.NORMAL+' '+ term_mode.BLUE+ term_mode.BOLD).strip()
    if not choice:
        choice='default'
    if verbose:
        print('Choice is : ',choice)
    execute(choice)

def main(argv=None):
    if argv is None:
        argv = sys.argv
    # etc., replacing sys.argv with argv in the getopt() call.
    # parse command line options
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h", ["help"])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err) # will print something like "option -a not recognized"
        print("for help use --help")
        sys.exit(2)
    # process options
    for o, a in opts:
        if o in ("-h", "--help"):
            print(__doc__)
            sys.exit(0)
    # process arguments
    for arg in args:
        process(arg) # process() is defined elsewhere

    parse_command_file(local_config_file)
    if debug:
        print('###### keys_to_id :')
        print(keys_to_id)
        print('###### commands :')
        print(commands)
        print('###### END (commands)')
    print_available_commands()
    choose_command()
    while loop:
        print_available_commands()
        choose_command()

if __name__ == "__main__":
    sys.exit(main())
#endif // DO_PY
