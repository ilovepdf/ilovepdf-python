"""
Module for RepairTask in the iLovePDF Python API.

This module provides the RepairTask class, which handles PDF repair tasks,
such as fixing corrupted PDF files.
"""

# pylint: disable=abstract-method

from .task import ProcessTask


class RepairTask(ProcessTask):
    """
    RepairTask for the iLovePDF Python API.
    Handles PDF repair tasks, such as fixing corrupted PDF files.
    """

    def __init__(self, public_key, secret_key, make_start=True):
        super().__init__(public_key, secret_key, make_start, tool="repair")

    def add_file(self, file_path, extra_params=None):
        if len(self.files) == 1:
            raise ValueError("RepairTask can only handle one file at a time.")
        return super().add_file(file_path, extra_params)
