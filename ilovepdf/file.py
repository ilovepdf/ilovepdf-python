"""Module for managing files with the iLovePDF API."""

import tempfile

from ilovepdf.validators import IntValidator, StringValidator

from .abstract_task_element import AbstractTaskElement


# pylint: disable=too-few-public-methods
class BaseFile(AbstractTaskElement):
    """Base class representing a base file managed by the iLovePDF API."""

    _DEFAULT_PAYLOAD = {
        "server_filename": None,
        "filename": None,
    }

    REQUIRED_FIELDS = ["server_filename", "filename"]

    def __init__(self, server_filename: str, filename: str):
        super().__init__()
        self.server_filename = server_filename
        self.filename = filename

    # Getters and Setters of filename
    @property
    def filename(self) -> str:
        """
        Gets the filename associated with the file.

        Returns:
            str: The filename. Default is None.
        """
        return self._get_attr("filename")

    @filename.setter
    def filename(self, value: str):
        """
        Sets the filename for the file.

        Args:
            value (str): The filename to associate.

        Raises:
            ValueError: If the filename is not a valid string.
        """
        StringValidator.validate(value, "filename")
        self._set_attr("filename", value)

    # Getters and Setters of server_filename
    @property
    def server_filename(self) -> str:
        """
        Gets the server filename associated with the file.

        Returns:
            str: The server filename. Default is None.
        """
        return self._get_attr("server_filename")

    @server_filename.setter
    def server_filename(self, value: str):
        """
        Sets the server filename for the file.

        Args:
            value (str): The server filename to associate.

        Raises:
            ValueError: If the server filename is not a valid string.
        """
        StringValidator.validate(value, "server_filename")
        self._set_attr("server_filename", value)

    @staticmethod
    def get_temp_filename(extension: str = "") -> str:
        """
        Returns a temporary filename with the given extension.

        Args:
            extension (str): The file extension to use.

        Returns:
            str: The path to the temporary file.
        """
        with tempfile.NamedTemporaryFile(suffix=extension) as temp_file:
            return temp_file.name


class File(BaseFile):
    """Represents a file uploaded to or managed by the iLovePDF API."""

    _DEFAULT_PAYLOAD = {
        "server_filename": None,
        "filename": None,
        "pdf_pages": None,
        "pdf_page_number": None,
        "pdf_forms": None,
    }

    @property
    def pdf_pages(self) -> int:
        """
        Gets the number of pages in the PDF file.

        Returns:
            int: The number of pages. Default is None.
        """
        return self._get_attr("pdf_pages")

    @pdf_pages.setter
    def pdf_pages(self, value: int):
        """
        Sets the number of pages in the PDF file.

        Args:
            value (int): Must be a positive integer.

        Raises:
            IntOutOfRangeError: If the value is not a positive integer.
        """
        IntValidator.validate_positive(value, "pdf_pages")
        self._set_attr("pdf_pages", value)

    @property
    def pdf_page_number(self) -> int:
        """
        Gets the current page number in the PDF file.

        Returns:
            int: The current page number. Default is None.
        """
        return self._get_attr("pdf_page_number")

    @pdf_page_number.setter
    def pdf_page_number(self, value: int):
        """
        Sets the current page number in the PDF file.

        Args:
            value (int): Must be a positive integer.

        Raises:
            IntOutOfRangeError: If the value is not a positive integer.
        """
        IntValidator.validate_positive(value, "pdf_page_number")
        self._set_attr("pdf_page_number", value)

    @property
    def pdf_forms(self) -> int:
        """
        Gets the number of forms in the PDF file.

        Returns:
            int: The number of forms. Default is None.
        """
        return self._get_attr("pdf_forms")

    @pdf_forms.setter
    def pdf_forms(self, value: int):
        """
        Sets the number of forms in the PDF file.

        Args:
            value (int): Must be a positive integer.

        Raises:
            IntOutOfRangeError: If the value is not a positive integer.
        """
        IntValidator.validate_positive(value, "pdf_forms")
        self._set_attr("pdf_forms", value)
