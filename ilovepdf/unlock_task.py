"""
Module for UnlockTask in the iLovePDF Python API.

This module defines the UnlockTask class, which handles PDF unlocking tasks,
removing password protection from PDF files.
"""

from .task import Task


class UnlockTask(Task):
    """
    Handles PDF unlocking tasks, removing password protection from PDF files.

    Args:
        public_key (str, optional): API public key.
            Uses ILOVEPDF_PUBLIC_KEY env variable if not provided.
        secret_key (str, optional): API secret key.
            Uses ILOVEPDF_SECRET_KEY env variable if not provided.
        make_start (bool, optional): Start the task immediately. Default is False.

    Example:
        task = UnlockTask(public_key="your_public_key", secret_key="your_secret_key")

    """

    _tool = "unlock"
