"""
Copyright © 2023, ARCHADEPT LTD. All Rights Reserved.
"""

# Standard deps
import logging
import sys

# Non-standard deps
import colorlog

# Local deps
from . import args

def init():
    """ Initialize logging infrastructure. """

    # We simply print colored strings, no other fancy formatting.
    formatter = colorlog.ColoredFormatter('%(log_color)s%(message)s')

    # DEBUG and INFO verbosity messages go to stdout.
    stdout = colorlog.StreamHandler(sys.stdout)
    stdout.setFormatter(formatter)
    stdout.setLevel(logging.DEBUG)
    stdout.addFilter(lambda record: record.levelno <= logging.INFO)

    # WARNING and ERROR verbosity messages go to stderr.
    stderr = colorlog.StreamHandler()
    stderr.setFormatter(formatter)
    stderr.setLevel(logging.WARNING)

    # Add handlers to top-level logger.
    logger = colorlog.getLogger('archadept')
    logger.addHandler(stdout)
    logger.addHandler(stderr)

    # Top-level logger level is determined by the command-line args.
    level = logging.INFO
    if args.debug:
        level = logging.DEBUG
    elif args.quiet:
        level = logging.WARNING
    logger.setLevel(level)

def _log(funcname:str, *args:object) -> None:
    """ Underlying implementation of debug(), info(), warn(), and err().
        Logs any number of strings/objects to either stdout or stderr at
        INFO, DEBUG, WARNING, or ERROR verbosity. """
    logfunc = getattr(colorlog.getLogger('archadept'), funcname)
    for arg in args:
        logfunc(str(arg))

def debug(*args:object):
    """ Log any number of strings/objects to stdout at DEBUG verbosity.
        @note DEBUG logging is only enabled by top-level '-D'. """
    _log('debug', *args)

def info(*args:object):
    """ Log any number of strings/objects to stdout at INFO verbosity.
        @note INFO logging is suppressed by top-level '-Q'. """
    _log('info', *args)

def warn(*args:object): 
    """ Log any number of strings/objects to stderr at WARNING verbosity. """
    _log('warning', *args)

def err(*args:object):
    """ Log any number of strings/objects to stderr at ERROR verbosity. """
    _log('error', *args)

