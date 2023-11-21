"""
Copyright © 2023, ARCHADEPT LTD. All Rights Reserved.
"""

# Standard deps
import json
import string
import sys
import traceback
from typing import NoReturn, Union

# Local deps
from . import log

def _die(*args:object) -> NoReturn:
    """ Log an error message and abort the script. """
    log.err(*args)
    sys.exit(1)

class UID():
    """ Class representing a unique ID in the range [0 .. 65,535] inclusive
        and encoded as a Base16 string. """

    alphabet = '0123456789ABCDEF'
    """ Base16 alphabet. """

    def __init__(self, uid_str:str) -> None:
        """ Constructor.
            :param uid_str Base16 encoded unique ID. """
        if len(uid_str) != 4:
            _die(f'bad unique ID \'{uid_str}\': must be of length 4')
        unit = 1
        self.uid_str = uid_str
        self.uid_int = 0
        for c in uid_str:
            if c not in UID.alphabet:
                _die(f'bad unique ID \'{uid_str}\': digit \'{c}\' not valid in Base16')
            self.uid_int += UID.alphabet.find(c) * unit
            unit *= 16

    def __int__(self) -> int:
        return self.uid_int

    def __str__(self) -> str:
        return self.uid_str

    def __hash__(self) -> int:
        return int(self)

    def __eq__(self, other) -> bool:
        return self.uid_str == other.uid_str

class Error():
    """ Class representing all errors that can be raised at runtime. """

    _registered_errors = dict()
    """ Dict mapping UIDs to registered Error objects. """

    @classmethod
    def register(cls, uid:Union[str, UID], name:str) -> None:
        """ Register a new error.

            Once registered, an error can be referenced using its name as an
            attribute of the Error class, for example if the error's name is
            'BAD_ARGS' then it can be referenced via 'Error.BAD_ARGS'.

            Furthermore, an error can be raised (thereby killing the script)
            by calling it, for example 'Error.BAD_ARGS()'.

            Any number of positional arguments can be passed to the invocation
            which will be sequentially logged at ERROR verbosity before the
            script is killed, which can help to provide additional contextual
            information regarding what went wrong.

            In particular, passing a caught Exception object through to the
            invocation will dump a traceback along with the actual Exception
            info.

            :param uid Unique ID for the new error.
            :name Name of the new error e.g. 'BAD_ARGS'. """
        def __die(msg:str) -> NoReturn:
            _die(f'unable to register new error with uid=\'{uid}\' name=\'{name}\': {msg}')
        if isinstance(uid, str):
            uid = UID(uid)
        elif not isinstance(uid, UID):
            __die(f'expected uid to be either a raw Base16 encoded unique ID or a wrapped UID object but got {type(uid)}')
        if uid in Error._registered_errors:
            __die(f'unique ID \'{uid}\' already assigned to \'{Error._registered_errors[uid].name}\'')
        e = Error()
        e.uid = uid
        e.name = name
        cls._registered_errors[uid] = e
        setattr(cls, name, e)

    def __call__(self, *objs:object, append:str=None) -> NoReturn:
        """ Raise this error, thereby killing the script.

            :param objs Any number of strings/objects to log at ERROR verbosity
                        before killing the script. Exception objects will dump
                        a traceback along with the actual Exception info. Dicts
                        and lists will be pretty-printed using JSON.

            :param append Optional string to append to the final error message,
                          for example append='foo bar baz' would append to give
                          '[ArchAdept error #1234] EXAMPLE_ERROR: foo bar baz'. """
        stack = None
        s = ''
        for obj in objs:
            if isinstance(obj, dict) or isinstance(obj, list):
                s += json.dumps(obj, indent=4) + '\n'
            elif isinstance(obj, Exception):
                stack = ''.join(traceback.format_exception(obj))
                stack = stack.rstrip()
            else:
                s += str(obj) + '\n'
        s += f'\n[ArchAdept error #{self.uid}] {self.name}'
        if append is not None:
            s += f': {append}'
        if stack is None:
            stack = 'Traceback (most recent call last):\n' + ''.join(traceback.format_stack()[:-1])
        _die(stack.rstrip(), '', s.lstrip(), f'For help with this error, see https://archadept.com/help/errors and search for "{self.uid}".')

def init():
    """ Register all known errors. """

    # EB01 to EBFF reserved for catching bugs in archadeptcli itself. """
    Error.register('EB01', 'UNGRACEFUL_EXIT')
    Error.register('EB02', 'UNIMPLEMENTED_FUNCTION')

    # EF01 to EFFF reserved for file handling errors.
    Error.register('EF01', 'CONFIG_FILE_PATH')

