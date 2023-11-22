#!/usr/bin/env python3
'''
We create a unit, that will be the test_ unit by ln -s simoultaneously. Runs with 'pytest'
'''
from cmd_ai.version import __version__
from fire import Fire
from cmd_ai import config


HELP = """
.h      help
.q      quit
.r      run code
.l      show tokens
.l number ... limit tokens
________________ ROLES
.a   assistent
.t   translator
.c   coder
.d   dalle
________________ MODEL
.i   use dalle
.v   use vision
"""


if __name__ == "__main__":
    print("i... in the __main__ of unitname of cmd_ai")
    Fire()
