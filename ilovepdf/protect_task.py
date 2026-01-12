"""Handles PDF protection tasks using the iLovePDF API.

Provides the ProtectTask class to set passwords and permissions on PDF files.
"""

from .task import Task
from .validators import StringValidator


class ProtectTask(Task):
    """
    Handles PDF protection tasks using the iLovePDF API.

    Allows setting a password to protect PDF files. The password must be a non-empty
    string and must be set before executing the task.

    Example:
        task = ProtectTask(public_key="your_public_key", secret_key="your_secret")
        task.add_file("/path/to/document.pdf")
        task.password = "mysecurepassword"
        task.execute()
        task.download("/path/to/output.pdf")
    """

    _tool = "protect"

    _DEFAULT_PAYLOAD = {
        "password": None,
    }

    REQUIRED_FIELDS = ["password"]

    @property
    def password(self) -> str:
        """
        Gets the password used to protect the PDF.

        Raises:
            NotImplementedError: Always, as the password cannot be accessed directly.
        """
        raise NotImplementedError("Password cannot be accessed directly")

    @password.setter
    def password(self, value: str) -> None:
        """
        Sets the password used to protect the PDF.

        Args:
            value (str): Must be a non-empty string.

        Raises:
            TypeError: If the password is not a string.
            ValueError: If the password is an empty string.
        """

        StringValidator.validate(value, "password")
        self._set_attr("password", value)
