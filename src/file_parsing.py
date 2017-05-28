#!/usr/bin/env python
# -*- coding: UTF8 -*-
import random
import string
from shared_data_and_options import *
from options_parsing import sort_options_and_arguments,process_options


def generate_unique_key(key):
    """ utility function to garantee no name collisions for keys """
    while data.keys_to_id.get(key) != None:
        # if key is already used, append a random ascii character to the key
        #key += random.choice(string.ascii_lowercase)
        key += random.choice(string.digits)
    return key

def parse_command_file(filename):
    with open(filename) as command_file:
        # n is not 0 when an other command file has already been read
        n = len(data.commands)
        for i,line in enumerate(command_file):
            line = line.strip()
            if line == '':
                if options.verbose:
                    print('line ',i,' is empty. Ignored.')
            elif line[0] == '#':
                # commented lines get ignored
                if options.verbose:
                    print('line ',i,' is commented. Ignored.')
            elif line[0] == '-':
                # this line is an option line
                if options.debug:
                    print("Option line is: "+line)
                (opts, args) = sort_options_and_arguments(line.split())
                if options.debug:
                    print("opts: ",opts)
                    print("args: ",args)
                process_options(opts)
            else:
                #(key_list,comment,command)= parse(line)
                (keys,separator,rest_of_line) = line.partition(':')
                if not separator:
                    # means the separator ':' is not present in the string
                    rest_of_line = keys
                    # By default we attribute the line number as key for the command
                    keys = str(n+i)
                elif not keys:
                    # means no keys where given (line starts with ':')
                    # By default we attribute the line number (starting at line 0) as key for the command
                    keys = str(n+i)
                # split and remove empty keys
                keys_list = [k for k in keys.split(',') if k.strip() ]
                if options.debug:
                    print("keys_list:",keys_list)
                keys_width = 0
                has_numeric_key = False
                for j,key in enumerate(keys_list) :
                    key = generate_unique_key( key.strip() )
                    keys_width += len(key) + 1 # the +1 is for the comma between keys
                    keys_list[j] = key
                    data.keys_to_id[key]= n+i
                    if key.isdecimal():
                        has_numeric_key = True
                    if key == 'default':
                        #nb: if several commands have the default key, only the first one will not be modified by generate_unique_keys, so no need to worry about multiple command with default flag
                        options.has_default_command = True
                if options.add_numeric_key and not has_numeric_key:
                    # add a numeric key, if necessary, as FIRST key
                    key = generate_unique_key(str(n+i))
                    keys_width += len(key) + 1 # the +1 is for the comma between keys
                    keys_list.insert(0,key)
                    data.keys_to_id[key]= n+i
                    has_numeric_key = True
                if keys_width > 0:
                    keys_width -= 1 # because no comma after last key
                if keys_width > global_vars.max_keys_width:
                    global_vars.max_keys_width = keys_width
                (comment,separator,command) = rest_of_line.partition('>')
                if not separator:
                    # If no separator is given, we assume the whole string is just a command
                    command = comment
                    comment = ''
                comment = comment.strip()
                l = len(comment)
                if l > global_vars.max_comment_width:
                    global_vars.max_comment_width = l
                command = command.strip()
                l = len(command)
                if l > global_vars.max_command_width:
                    global_vars.max_command_width = l
                data.commands[n+i] = ( keys_list , comment , command )

def check_then_parse_file(filename,str_filetype,template):
    if options.debug:
        print("Using ",str_filetype," file: ", filename)
    try:
        parse_command_file(filename)
    except FileNotFoundError:
        print(term_mode.TITLEYELLOW + "Warning: no {} file '{}'".format(str_filetype,filename)+term_mode.NORMAL )
        ans = input(term_mode.YELLOW + "Do you want to create one from template ?"+ term_mode.TITLEYELLOW  + '[Y/n]'+term_mode.NORMAL )
        if ans and (ans[0] in 'nN'):
             if options.verbose:
                print("No ",str_filetype," file created")
        else:
             if options.verbose:
                print("Creating ",str_filetype," file...")
             #TODO more security checks
             os.makedirs(options.global_config_dir, exist_ok=True)
             copyfile( template , filename )
             if options.verbose:
                print("Done")
             parse_command_file(filename)
