"""
Copyright © 2023, ARCHADEPT LTD. All Rights Reserved.
"""

# Standard deps
import os
from pathlib import Path

# Local deps
from . import args
from . import error

root = None
""" Path to the root directory that was mounted in the Docker container. """

container_id = None
""" ID of the Docker container. """

