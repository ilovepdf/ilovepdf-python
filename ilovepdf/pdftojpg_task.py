"""Handles PDF to JPG conversion tasks using the iLovePDF API.

Provides the PdfToJpgTask class to configure and execute PDF to JPG conversion.
Allows selection of conversion mode: 'pages' (convert each page to JPG) or
'extract' (extract images from PDF).

Example:
    task = PdfToJpgTask("public_key", "secret_key")
    task.add_file("sample.pdf")
    task.pdfjpg_mode = "extract"
    task.execute()
    task.download()
"""

from typing import Literal

from ilovepdf.task import Task
from ilovepdf.validators import ChoiceValidator

PdfJpgModeType = Literal["pages", "extract"]
PDFJPG_MODE_OPTIONS = {"pages", "extract"}


class PdfToJpgTask(Task):
    """
    Handles PDF to JPG conversion tasks using the iLovePDF API.

    Allows configuration of conversion mode (pages or extract).

    Example:
        task = PdfToJpgTask("public_key", "secret_key")
        task.add_file("sample.pdf")
        task.pdfjpg_mode = "extract"
        task.execute()
        task.download()
    """

    _tool = "pdfjpg"

    _DEFAULT_PAYLOAD = {
        "pdfjpg_mode": "pages",
    }

    @property
    def pdfjpg_mode(self) -> PdfJpgModeType:
        """
        Gets the current PDF to JPG conversion mode.

        Returns:
            PdfJpgModeType: The current mode. Default is 'pages'.
        """
        return self._get_attr("pdfjpg_mode")

    @pdfjpg_mode.setter
    def pdfjpg_mode(self, value: PdfJpgModeType):
        """
        Sets the PDF to JPG conversion mode.

        Args:
            value (PdfJpgModeType): Must be one of PDFJPG_MODE_OPTIONS.

        Raises:
            InvalidChoiceError: If the provided value is not valid.
        """
        ChoiceValidator.validate(value, PDFJPG_MODE_OPTIONS, "pdfjpg_mode")
        self._set_attr("pdfjpg_mode", value)
