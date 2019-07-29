#!/usr/bin/env python
# -*- coding: UTF8 -*-
from shutil import copyfile

from doo.shared_data_and_options import *

def write_file(file_str,dest_path):
    pass

# Prerequisite : global data.commands and data.keys_to_id has already been populated
def standardize(config_file_path):
    intro ="""# This is local configuration file for doo program
#
#    .doo format: each command line should be in the format:
#        [id[,alternative_ids]:][comment]>command
#    
#    with :
#        id             : a unique identifier used to identify the command to run. Can contain any printable character. 
#        alternative_ids: one or more optional ids separated by a comma.
#        comment        : an optional comment or description on the command
#        command        : the actual command to run
# 
#    If id is omitted, one will be automatically generated (from the line number and random characters).
#    If no id is given when running the doo command, the command with identifier "default" is going to be executed
# 
#    examples of command lines in .doo files:
#        0: default command > ls -l
#        1, kill the fox > killall firefox
#        > ls -a
#
#id : comment > command
"""
    pass
