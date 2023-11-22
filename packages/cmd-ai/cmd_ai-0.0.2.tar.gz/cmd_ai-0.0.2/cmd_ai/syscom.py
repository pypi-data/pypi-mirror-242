#!/usr/bin/env python3
'''
We create a unit, that will be the test_ unit by ln -s simoultaneously. Runs with 'pytest'
'''
from cmd_ai.version import __version__
from fire import Fire
from cmd_ai import config
from console import fg
import sys

from cmd_ai import texts

# print("v... unit 'unitname' loaded, version:",__version__)

def process_syscom( cmd):
    if cmd.strip() == ".q":
        sys.exit(0)
    if cmd.strip() == ".h":
        print(texts.HELP)
    else:
        print(f"!... {fg.red} unknown system command {fg.default}")

if __name__ == "__main__":
    print("i... in the __main__ of unitname of cmd_ai")
    Fire()
