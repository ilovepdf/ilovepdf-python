"""Handles PDF repair tasks using the iLovePDF API.

Provides the RepairTask class to fix corrupted PDF files.
"""

# pylint: disable=abstract-method

from .task import Task


class RepairTask(Task):
    """
    Handles PDF repair tasks using the iLovePDF API.

    Allows uploading a single PDF file to attempt repair of corruption or errors.

    Example:
        task = RepairTask(public_key="your_public_key", secret_key="your_secret")
        task.add_file("/path/to/corrupted.pdf")
        task.execute()
        task.download("/path/to/repaired.pdf")
    """

    _tool = "repair"

    def append_file(self, file: str):
        """
        Adds a PDF file to the repair task.

        Args:
            file (str): Path to the PDF file to repair.

        Raises:
            ValueError: If more than one file is added to the task.

        Returns:
            File: The added file object.
        """
        if len(self.files) == 1:
            raise ValueError("RepairTask can only handle one file at a time.")
        return super().append_file(file)
