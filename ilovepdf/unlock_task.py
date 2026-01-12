# pylint: disable=abstract-method
"""
Module for UnlockTask in the iLovePDF Python API.

This module defines the UnlockTask class, which handles PDF unlocking tasks,
removing password protection from PDF files.
"""
from .task import ProcessTask


class UnlockTask(ProcessTask):
    """
    UnlockTask for the iLovePDF Python API.
    Handles PDF unlocking tasks, removing password protection from PDF files.
    """

    def __init__(self, public_key, secret_key, make_start=True):
        super().__init__(public_key, secret_key, make_start, tool="unlock")

    def add_file(self, file_path, extra_params=None):
        self._validate_file_extension(file_path)
        return super().add_file(file_path, extra_params)
