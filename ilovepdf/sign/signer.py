"""Module containing the ReceiverAbstract class for handling receiver information."""

from typing import Literal, Optional

from ilovepdf.abstract_task_element import AbstractTaskElement
from ilovepdf.file import File
from ilovepdf.validators import ChoiceValidator, StringValidator

from .signer_file import SignerFile

SignerType = Literal["signer", "validator", "viewer"]
SIGNER_TYPE_OPTIONS = {"signer", "validator", "viewer"}


class Signer(AbstractTaskElement):
    """Abstract class Receivers that participate in the signature"""

    _DEFAULT_PAYLOAD = {
        "name": None,
        "email": None,
        "phone": None,
        "files": [],
        "type": "signer",
        "access_code": None,
        "force_signature_type": None,
    }

    REQUIRED_FIELDS = ["name", "email", "files"]

    def __init__(
        self, *args, name: Optional[str] = None, email: Optional[str] = None, **kwargs
    ):
        """
        Initializes a Signer instance.

        Args:
            name (Optional[str]): The name of the signer.
            email (Optional[str]): The email address of the signer.

        Example:
            signer = Signer(name="John Doe", email="mark@email.com")
        """
        super().__init__(*args, **kwargs)
        if name:
            self.name = name
        if email:
            self.email = email

    # Getters and Setters of name
    @property
    def name(self):
        """Get the name of the signer."""
        return self._get_attr("name")

    @name.setter
    def name(self, value):
        """
        Sets the name of the signer.

        Args:
            value (str): Must be a non-empty string. Uses StringValidator for
                validation.
        """
        StringValidator.validate(value, "name")
        self._set_attr("name", value)

    # Getters and Setters of email
    @property
    def email(self):
        """Get the email address of the signer."""
        return self._get_attr("email")

    @email.setter
    def email(self, value):
        """
        Sets the email address of the signer.

        Args:
            value (str): Must be a non-empty string. Uses StringValidator for
                validation.
        """
        StringValidator.validate(value, "email")
        self._set_attr("email", value)

    # Getters and Setters of phone
    @property
    def phone(self):
        """Get the phone number of the signer."""
        return self._get_attr("phone")

    @phone.setter
    def phone(self, value):
        """
        Sets the phone number of the signer.

        Args:
            value (str): Should be a valid string (not None). Uses StringValidator for
                validation.
        """
        StringValidator.validate_type(value, "phone")
        self._set_attr("phone", value)

    # Getters and Setters of type
    @property
    def type(self):
        """Get the type of the signer."""
        return self._get_attr("type")

    @type.setter
    def type(self, value):
        ChoiceValidator.validate(value, SIGNER_TYPE_OPTIONS, "type")
        self._set_attr("type", value)

    @property
    def files(self):
        """Get the list of files associated with the Signer.

        Returns:
            list: List of SignerFile objects.
        """
        return self._get_attr("files")

    def add_signer_file(self, file: SignerFile):
        """Add a SignerFile to the file's elements list.

        Args:
            file (SignerFile): The file to add.

        Returns:
            SignerFile: The added SignerFile object.
        """
        if not isinstance(file, SignerFile):
            raise TypeError("file must be a SignerFile object.")
        self.files.append(file)
        return file

    def add_file(self, file: File) -> SignerFile:
        """Add a File to the file's elements list.

        Args:
            file (File): The file to add.

        Returns:
            SignerFile: The added SignerFile object.
        """
        if not isinstance(file, File):
            raise TypeError("file must be a File object.")
        return self.add_signer_file(SignerFile(file))
