#!/usr/bin/env python3
# -*- coding: UTF8 -*-

#ifndef MAIN_PY
#define MAIN_PY

"""
    doo - utility to run user predefined commands

   Copyright (C) 2016-2019 Fargetton Renan <renan.fargetton<at>.com > 
   GNU GPLv3 or later

"""
#TODO:
# * check : add numeric keys to every command (force what is currently --numeric-id)
# * 
# * finish separate package build
#   * check for dependencies
# * Implement all the changes for options described in --help
#     * --strandardize
# * arch install : modify PKGBUILD
# * nb : default config file ?
# 
# * PUBLISH 
# 
# * «doo -g» without mentionned name : print a list of available files
# * verify the program is running with python3
# * predictable ids : always generate the same unique_key : hash functions ? Or force -w option ?
# * parse command line
# * write the modified key to .doo file when there is duplicate keys (option -?)
# * propose to edit command/config file when created
# * make better template and default conf file
# * tests !
# * default command to execute : default + d,D,0 ? 
# * 

import sys

#from shared_data_and_options import *
#from options_parsing import process_options,process_cmdline_only_options,sort_options_and_arguments
from doo.options_parsing import *
from doo.file_parsing import check_then_parse_file
from doo.command_choice_and_execution  import ask_then_exit_or_choice,user_choice,execute
from doo.standardize_config_file import standardize
#from  import *

def main(argv=None):
    if argv is None:
        argv = sys.argv
    # etc., replacing sys.argv with argv in the getopt() call.
    (opts, args) = sort_options_and_arguments(sys.argv[1:])

    # process cmdline-only options (needs to be early for debug flag)
    use_a_global_command_file = process_cmdline_only_options(opts)

    if options.debug:
        print("argv: ",argv)
        print("opts: ",opts)
        print("args: ",args)

    # process arguments into a string
    key =''
    for w in args:
        key += str(w) + ' '
    key = key.strip()
    if options.debug:
        print("cmdline key: '" + key + "'")

    # read global config file
    check_then_parse_file(options.global_config_file,"global config",options.global_config_file_template)

    # read choosen command file
    if options.debug:
        print("Using global commands ? : " + str(use_a_global_command_file) )
    if use_a_global_command_file:
        # read global command file
        check_then_parse_file(options.global_command_file,"global command",options.command_file_template)
    else:
        # read local command file
        check_then_parse_file(options.local_command_file,"command",options.command_file_template)

    # process the rest of command lines options
    # nb : command lines options must be processed after command file is read because it can overwrite options
    process_options(opts)

    if not options.colors:
        remove_colors_and_bold()

    if options.debug:
        print('###### data.keys_to_id :')
        print(data.keys_to_id)
        print('###### data.commands :')
        print(data.commands)
        print('###### END (data.commands)')


    try:
        if options.standardize:
            if options.debug:
                print('Standardizing local command file ...')
            standardize(options.local_command_file)
        
        if key:
            # the key was given in the command line
            key_exists = execute(key)
            if not key_exists:
                ask_then_exit_or_choice('Show options ?')
            else:
               sys.exit(0) # or 1, or whatever

        user_choice()
        while options.loop:
            ask_then_exit_or_choice('Continue ?')
    except KeyboardInterrupt:
        sys.exit(0) # or 1, or whatever

if options.debug:
    print("__name__ value: ", __name__)
if __name__ == "__main__":
    # execute only if run as a script
    #sys.exit(main(sys.argv[1]))
    sys.exit(main())

#endif // MAIN_PY
