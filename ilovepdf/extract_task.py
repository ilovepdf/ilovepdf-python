"""Handles PDF extraction tasks using the iLovePDF API.

Provides the ExtractTask class to configure and execute PDF extraction.
Allows extraction of text from PDF files.
"""

from .task import Task
from .validators import BoolValidator


class ExtractTask(Task):
    """
    Handles PDF extraction tasks using the iLovePDF API.

    Args:
        public_key (str, optional): API public key.
            Uses ILOVEPDF_PUBLIC_KEY env variable if not provided.
        secret_key (str, optional): API secret key.
            Uses ILOVEPDF_SECRET_KEY env variable if not provided.
        make_start (bool, optional): Start the task immediately. Default is False.

    Example:
        task = ExtractTask(public_key="your_public_key", secret_key="your_secret_key")
    """

    _tool = "extract"

    _DEFAULT_PAYLOAD = {
        "detailed": False,
    }

    @property
    def detailed(self) -> bool:
        """
        Gets the current detailed extraction setting.

        Returns:
            bool: The current detailed extraction setting.
        """
        return self._get_attr("detailed")

    @detailed.setter
    def detailed(self, value: bool):
        """
        Includes the following PDF properties separated by a comma: PageNo, XPos, YPos,
            Width, FontName, FontSize, Length and Text.

        Default: False

        Example:
            task.detailed = True
        """
        BoolValidator.validate(value, "detailed")
        self._set_attr("detailed", value)
