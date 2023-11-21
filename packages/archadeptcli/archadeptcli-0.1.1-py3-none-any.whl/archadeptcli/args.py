"""
Copyright © 2023, ARCHADEPT LTD. All Rights Reserved.
"""

# Standard deps
import argparse
from pathlib import Path

debug = False
""" Enable logging debug verbosity messages to stdout.
    Set by top-level '-D', mutually exclusive with top-level '-Q'. """

quiet = False
""" Suppress logging info verbosity messages to stdout.
    Set by top-level '-Q' mutually exclusive with top-level '-D'. """

config_path = None
""" Path to the workspace config file to use.
    Defaults to '~/.config/archadept.cfg'. Set by top-level '-c PATH'. """

command = None
""" Chosen command e.g. 'init' if user invoked 'archadept init'. """

root = None
""" Root directory to mount at \'/usr/src/archadept\' in Docker container.
    Set by 'ROOT' argument of 'archadept init'. """

def init() -> None:
    """ Parse the command-line arguments into module-level variables accessible
        by any other module that has imported 'args'. """

    parser = argparse.ArgumentParser(prog='archadept')

    verbosity = parser.add_mutually_exclusive_group()

    verbosity.add_argument(
        '-D', '--debug',
        help='Enable logging debug messages; mutually exclusive with \'-Q\'.',
        action='store_true')

    verbosity.add_argument(
        '-Q', '--quiet',
        help='Quiten logging, only printing warnings/errors; mutually exclusive with \'-D\'.',
        action='store_true')

    parser.add_argument(
        '-c', '--config',
        metavar='PATH',
        help='Which workspace config file to use (default: \'~/.config/archadept.cfg\'',
        type=Path,
        default=Path('~/.config/archadept.cfg').expanduser())

    subparsers = parser.add_subparsers(
        help='command help',
        dest='command',
        required=True)

    init_parser = subparsers.add_parser('init', help='archadept init help')
    build_parser = subparsers.add_parser('build', help='archadept build help')
    clean_parser = subparsers.add_parser('clean', help='archadept clean help')
    run_parser = subparsers.add_parser('run', help='archadept run help')
    debug_parser = subparsers.add_parser('debug', help='archadept debug help')

    init_parser.add_argument(
        'root',
        metavar='ROOT',
        help='Root directory to mount in the Docker container at \'/usr/src/archadept\'.',
        type=Path)

    args = parser.parse_args()

    global debug
    debug = args.debug

    global quiet
    quiet = args.quiet

    global config_path
    config_path = args.config

    global command
    command = args.command

    if command == 'init':
        global root
        root = args.root

