"""Module containing the ReceiverAbstract class for handling receiver
information."""

from typing import List, Optional

from ilovepdf.abstract_task_element import AbstractTaskElement
from ilovepdf.file import File
from ilovepdf.validators import StringValidator

from .element import Element

MAX_ELEMENTS = 1000


class SignerFile(AbstractTaskElement):
    """Represents a file to be signed in a signature task.

    Args:
        file (Optional[File]): The file object to be signed. If provided, it will be
            associated with this SignerFile instance.

    Example:
        signer_file = SignerFile(file=my_file)
    """

    _DEFAULT_PAYLOAD = {
        "server_filename": None,
        "elements": [],
    }
    REQUIRED_FIELDS = ["server_filename", "elements"]

    def __init__(self, file: Optional[File] = None):
        super().__init__()
        self._file = None
        if file:
            self.file = file

    @property
    def file(self) -> File | None:
        """Get the File object associated with the signer file."""
        return self._file

    @file.setter
    def file(self, file: File):
        """Set the File object associated with the signer file.

        Args:
            file (File): The File object to be associated.
                Must be a valid File instance.
        """
        self.server_filename = file.server_filename
        self._file = file

    # Getters and Setters of server_filename
    @property
    def server_filename(self):
        """Get the server filename of the file to be signed."""
        return self._get_attr("server_filename")

    @server_filename.setter
    def server_filename(self, value):
        """Set the server filename of the file to be signed.

        Args:
            value (str): The filename on the server.
        """
        StringValidator.validate(value, "server_filename")
        self._set_attr("server_filename", value)

    # Getters and Setters of elements
    @property
    def elements(self) -> List[Element]:
        """Get the list of elements associated with the file.

        Returns:
            list: List of Element objects.
        """
        return self._get_attr("elements")

    def add_element(self, element: Optional[Element] = None) -> Element:
        """Add an Element to the file's elements list.

        Args:
            element (Optional[Element]): The element to add. If None, a new Element
                is created.

        Returns:
            Element: The added Element object.
        """
        if len(self.elements) >= MAX_ELEMENTS:
            raise ValueError("Maximum number of elements reached")
        element = element or Element()
        if not isinstance(element, Element):
            raise TypeError("element must be an Element object.")
        self.elements.append(element)
        return element

    def _to_payload(self):
        if (self._file or self.server_filename) and not self.elements:
            self.add_element()

        return super()._to_payload()
