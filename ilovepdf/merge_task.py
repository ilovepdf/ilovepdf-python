"""
Module for handling PDF merge tasks using the iLovePDF API.
"""

# pylint: disable=abstract-method

from .task import ProcessTask


class MergeTask(ProcessTask):
    """
    Class to handle the merge PDF task using the iLovePDF API.
    """

    def __init__(self, public_key, secret_key, make_start=True):
        super().__init__(public_key, secret_key, make_start, tool="merge")
