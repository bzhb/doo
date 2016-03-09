#!/usr/bin/env python3
# -*- coding: UTF8 -*-

#ifndef DO_PY
#define DO_PY

"""do command

    Read command in the .do file in the local folder and execute the choosen command

    .do format: each line should be in the format:
        [id[,alternative_ids]:][comment]>command
    with :
        id : a unique identifier used to identify the command to run. Can contain any printable character
        alternative_ids: one or more optional ids separated by a comma.
        comment: an optional comment or description on the command
        command: the actual command to run

    if id is omitted, one will be automatically generated (from the line number and random characters).
    examples:
        0: default command > ls -l
        1, kill the fox > killall firefox
        > ls -a
"""
import sys
import subprocess
import getopt
import random
import string

# Default options:
debug = True
local_config_file ='.do'
global_config_file ='~/.config/do/do.conf'
no_global_config = False
verbose = True
loop = False
colors = False
no_confirm = False
shell='zsh'

commands = {}
keys_to_id = {}

def process(arg):
    pass

def generate_unique_key(key):
    while keys_to_id.get(key) != None:
        # if key is already used, append a random ascii character to the key
        key += random.choice(string.ascii_lowercase)
    return key

def parse_command_file(filename):
    with open(filename) as command_file:
        for i,line in enumerate(command_file):
            if line[0] == '#':
                # commented lines get ignored
                if verbose:
                    print('line ',i,' is commented. Ignored.')
            elif False:
                # if line is an option line
                pass #TODO: deal with options lines
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
                    # By default we attribute the line number as key for the command
                    keys = str(i)
                keys_list = keys.split(',')
                for j,key in enumerate(keys_list) :
                    key = generate_unique_key( key.strip() )
                    keys_list[j] = key
                    keys_to_id[key]= i
                (comment,separator,command) = rest_of_line.partition('>')
                commands[i] = ( keys_list , comment.strip(),command.strip() )

def print_available_commands():
    keys_field_size = 20
    comment_field_size = 40
    command_field_size = 40
    #TODO: find a smarter way to calculate the size for each field
    print('Identifier'.ljust(keys_field_size),'| ','Comment'.ljust(comment_field_size),'| ','Command'.ljust(command_field_size))
    print(''.ljust(keys_field_size + comment_field_size + command_field_size + 4,'-'))
    for (keys_list,comment,command) in commands.values() :
        keys_str = ''
        for key in keys_list:
            keys_str += key + ','
        keys_str = keys_str[:-1]
        keys_str = keys_str[:keys_field_size].ljust(keys_field_size)
        comment = comment[:comment_field_size].ljust(comment_field_size)
        command = command[:command_field_size].ljust(command_field_size)
        print(keys_str,': ',comment,'>',command)

def execute(choice):
    id = keys_to_id[choice]
    (keys_list,comment,command) = commands[id]
    confirmation = input('Run command ? > ' + command + ' [Y/n]')
    if confirmation:
        if confirmation[0] in 'nN':
            print('Abort')
        else:
            subprocess.run([command],shell=True)
    else:
        subprocess.run([command],shell=True)

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

    parse_command_file('.do')
    if debug:
        print('###### keys_to_id :')
        print(keys_to_id)
        print('###### commands :')
        print(commands)
        print('###### END (commands)')
    print_available_commands()
    choice = input('Enter identifier of the command you want to run: ')
    if not choice:
        choice='default'
    if verbose:
        print('Choice is : ',choice)
    execute(choice)

if __name__ == "__main__":
    sys.exit(main())
#endif // DO_PY
