"""
Module for RotateTask in the iLovePDF Python API.
Provides functionality to handle PDF rotation tasks.
"""

# pylint: disable=abstract-method

from .task import ProcessTask


class RotateTask(ProcessTask):
    """
    RotateTask for the iLovePDF Python API.
    Handles PDF rotation tasks.
    """

    def __init__(self, public_key, secret_key, make_start=True):
        super().__init__(public_key, secret_key, make_start, tool="rotate")
