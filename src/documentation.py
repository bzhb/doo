#!/usr/bin/env python
# -*- coding: UTF8 -*-

doc_str="""doo command
NAME
    doo - utility to run user predefined commands

SYNOPSIS
    doo [OPTIONS] [COMMAND ID]

DESCRIPTION
    Console utility to execute user-defined command fron a .doo file in the local folder.

COMMAND ID
    Command identifier in the command file (.doo).

COMMAND-LINE ONLY OPTIONS

    -h --help
        Show help

    -i --file=FILE
        Use the specified configuration file from local directory instead of .doo

    -g --global-file=FILENAME
        Use the file ~/.config/doo/FILENAME.doo instead of local .doo file
        If no FILENAME is specified, reading ~/.config/doo/default.doo

    -d --debug
        Debug mode with additional prints


COMMAND-LINE AND CONFIG FILES OPTIONS

    -f --no-confirm
        No confirmation is asked before running the command

    -F --force-confirm
        User is asked confirmation before running the command. This is the default behavior, this option is only necessary to superseed options set in a config file

    -o --loop
        After running a command the program doesn't quit and ask for running a new command, until the user hit q or ^C

    -v --verbose

    -c --no-colors
        disable colors

    -C --force-colors
        This is the default behavior, this option is only necessary to superseed options set in a config file

    -w --write-ids
        Add a numeric id to every command without numeric id defined in config files
    -s --standardize (NOT IMPLEMENTED)
        edit the command file to put it the standard format (add missing delemiters and spaces to align text), put an intro for options, current .doo file is moved to .doo.old

LOCAL COMMAND FILE
    The command file in the local directory should be named .doo (or otherwise its name shoud be given with --file option).

    .doo format: each command line should be in the format:
        [id[,alternative_ids]:][comment]>command

    with :
        id             : a unique identifier used to identify the command to run.
        alternative_ids: one or more optional ids separated by a comma.
        comment        : an optional comment or description on the command
        command        : the actual command to run

    If id is omitted, one will be automatically generated (from the line number and random characters).
    If no id is given when running the doo command, the command with identifier "default" is going to be executed

    examples of config in .doo file:
        0,default: default command > ls -l
        1, kill the fox > killall firefox
        > ls -a

GLOBAL CONFIG FILES
    Global config files are in the ~/.config/doo/ repository

    doo.conf : this file is always parsed when doo command is used. This the designated location to define user default options. Although it is not recommended, it is possible to insert command lines in this file. In this case thoose commands will appear in the table everytime doo is run.

    FILENAME.doo : It is possible (and encouraged) to create or modify other global command files like FILENAME.doo to be used with the -g options, like : doo -g FILENAME.

EXAMPLES
    doo
    doo COMMAND_KEY
    doo -g system reboot (use ~/.config/doo/system.doo)

AUTHOR
    Fargetton Renan <renan.fargetton <at> .com > 2016

COPYRIGHT
   Copyright (C) 2016-2017  Fargetton Renan 

   GNU GPLv3 or later

   This program is free software; you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation; either version 3 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   To get a copy of the GNU General Public License write to the 
   Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, 
   Boston, MA 02110-1301  USA
"""
