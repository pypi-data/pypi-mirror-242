"""
Copyright © 2023, ARCHADEPT LTD. All Rights Reserved.
"""

# Import and initialize the ArchAdept CLI module.
import archadeptcli
archadeptcli.init()
from archadeptcli import *

def main_init():
    pass

def main():
    try:
        if args.command == 'init':
            main_init()
        else:
            Error.UNIMPLEMENTED_FUNCTION(append=f'main_{args.command}()')
    except Exception as e:
        Error.UNGRACEFUL_EXIT(e, append='crashed unexpectedly')

