"""
This module provides the ExtractTask class for extracting text from PDF files using the 'Extract text' service.
"""

from .task import ProcessTask


class ExtractTask(ProcessTask):
    """
    Implements functionality to extract text from a PDF file and save it as plain text,
    using the 'Extract text' service.
    """

    DEFAULTS_VALUES = {
        "detailed": False,
    }

    def __init__(self, public_key=None, secret_key=None, make_start=True):
        super().__init__(public_key, secret_key, make_start, tool="extract")

    @property
    def detailed(self) -> bool:
        return self._params["detailed"]

    @detailed.setter
    def detailed(self, value: bool):
        """
        Includes the following PDF properties separated by a comma: PageNo, XPos, YPos, Width,
        FontName, FontSize, Length and Text.

        Default: False

        Example:
            task.detailed = True
        """
        self._params["detailed"] = bool(value)
