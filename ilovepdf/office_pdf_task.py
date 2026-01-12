"""Module for handling Office to PDF conversion tasks in iLovePDF."""

# pylint: disable=abstract-method


from .exceptions import TooManyFilesError
from .task import Task

FILE_EXTENSIONS = [
    "doc",
    "docx",
    "ppt",
    "pptx",
    "xls",
    "xlsx",
    "odt",
    "odp",
    "ods",
]


class OfficePdfTask(Task):
    """
    Class to handle the Office to PDF conversion task in iLovePDF.
    """

    _tool = "officepdf"
    _file_extension = FILE_EXTENSIONS

    def append_file(self, file):
        """Append a file to the task.

        Args:
            file (File): File to append.

        Raises:
            TooManyFilesError: If the task already has one file.

        Returns:
            File: The appended file.
        """
        if len(self.files) == 1:
            raise TooManyFilesError("OfficePdfTask can only handle one file at a time.")
        return super().append_file(file)
