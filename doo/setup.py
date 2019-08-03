#!/usr/bin/env python3
# -*- coding: UTF8 -*-

#ifndef SETUP_PY
#define SETUP_PY

"""
    doo - utility to run user predefined commands

   Copyright (C) 2016-2019 Fargetton Renan < code.renan.f<at>gmail.com > 
   GNU GPLv3 or later

"""
from setuptools import setup, find_packages

setup(
    name="Doo",
    version="0.0.4.1",
    packages=find_packages(),
    #packages=(
    #        'doo',
    #),
    scripts=[],

    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
    install_requires=[
        # 'docutils>=0.3'
    ],

    package_data={
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.txt', '*.rst'],
        # And include any *.msg files found in the 'hello' package, too:
        'hello': ['*.msg'],
        #'doo': [
        #        'data/*',
        #        'config/doo.conf',
        #],
    },

    # La syntaxe est "nom-de-commande-a-creer = package.module:fonction".
    entry_points = {
        'console_scripts': [
            'doo = doo.main:main',
        ],
    },
    # metadata to display on PyPI
    author="Renan Fargetton",
    author_email="code.renan.f@gmail.com",
    description="Doo - utility to run user predefined commands",
    keywords="doo,utility,command,developpers",
    #url="http://",   # project home page, if any
    project_urls={
        # "Bug Tracker": "https://",
        # "Documentation": "https://",
        "Source Code": "https://github.com/bzhb/doo",
    },
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
#        'Development Status :: 3 - Alpha',
#        'Development Status :: 4 - Beta',
#        'Development Status :: 5 - Production/Stable',
#        'Development Status :: 6 - Mature',
#        'Development Status :: 7 - Inactive',
        'Environment :: Console',
        'License :: OSI Approved :: GNU General Public Licence version 3 or later'
    ]

)


#endif // SETUP_PY
