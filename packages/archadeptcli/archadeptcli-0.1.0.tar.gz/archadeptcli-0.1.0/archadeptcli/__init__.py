"""
Copyright © 2023, ARCHADEPT LTD. All Rights Reserved.
"""

# Local deps
from . import args
from . import log
from . import error
from .error import Error

def init() -> None:
    args.init()
    log.init()
    error.init()

