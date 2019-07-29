#!/usr/bin/env python
# -*- coding: UTF8 -*-
import sys
import getopt
import pydoc
from shared_data_and_options import *
from documentation import doc_str


def process_cmdline_only_options(opts):
    use_a_global_command_file = False
    for o, a in opts:
        if o in ("-h", "--help"):
            pydoc.pager(doc_str)
            sys.exit(0)
        if o in ("-i", "--file"):
            options.local_command_file = expanduser(a)
        if o in ("-g", "--global-file"):
            options.global_command_file = options.global_config_dir + expanduser(a) + ".doo"
            if options.debug :
                print("global command file a=" + a)
            #TODO deal with empty "a" : "doo -g " should use default.doo or ask
            use_a_global_command_file = True
        if o in ("-d", "--debug"):
            options.debug=True
        #nb: add_numeric_key is not a commandline-only option but it must be processed early nontheless
        if o in ("-n", "--no-numkey"):
            options.add_numeric_key=False
    return use_a_global_command_file

def process_options(opts):
    if options.debug:
        print("Process options: "+ str(opts))
    for o, a in opts:
        if o in ("-f", "--no-confirm"):
            options.no_confirm=True
        if o in ("-F", "--force-confirm"):
            options.no_confirm=False
        if o in ("-v", "--verbose"):
            options.verbose=True
        if o in ("-o", "--loop"):
            options.loop=True
        if o in ("-c", "--no-colors"):
            options.colors=False
        if o in ("-C", "--force-colors"):
            options.colors=True
        if o in ("-n", "--no-numkey"):
            options.add_numeric_key=False
        if o in ("-s", "--standardize"):
            options.standardize=True

def sort_options_and_arguments(line):
    try:
        return getopt.getopt(line, "hi:g:dfFovcCns", ["help","file=","global-file=","debug","no-confirm","force-confirm","loop","verbose","no-colors","force-colors""no-numkey","standardize"])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err) # will print something like "option -a not recognized"
        print("for help use --help")
        sys.exit(2)
