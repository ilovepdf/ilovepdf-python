"""Module for PDF to PDF/A conversion task using the iLovePDF API."""

# pylint: disable=abstract-method

from typing import Literal

from .task import ProcessTask

PDFA_CONFORMANCES = [
    "pdfa-1b",
    "pdfa-1a",
    "pdfa-2b",
    "pdfa-2u",
    "pdfa-2a",
    "pdfa-3b",
    "pdfa-3u",
    "pdfa-3a",
]

ConformanceType = Literal[
    "pdfa-1b",
    "pdfa-1a",
    "pdfa-2b",
    "pdfa-2u",
    "pdfa-2a",
    "pdfa-3b",
    "pdfa-3u",
    "pdfa-3a",
]


class PdfToPdfATask(ProcessTask):
    """
    Class for PDF/A conversion task using the iLovePDF API.
    """

    DEFAULTS_VALUES = {
        "conformance": "pdfa-2b",
        "allow_downgrade": True,
    }

    def __init__(self, public_key=None, secret_key=None, make_start=True):
        super().__init__(public_key, secret_key, make_start, tool="pdfa")

    @property
    def conformance(self) -> str:
        return self._params["conformance"]

    @conformance.setter
    def conformance(self, value: ConformanceType):
        """
        PDF/A conformance level for the conversion task.

        Accepted values are: "pdfa-1b", "pdfa-1a", "pdfa-2b", "pdfa-2u", "pdfa-2a", "pdfa-3b", "pdfa-3u", "pdfa-3a".

        Default: "pdfa-2b"

        Example:
            task.conformance = "pdfa-1b"
        """
        if value not in PDFA_CONFORMANCES:
            raise ValueError(f"Invalid conformance: {value}")
        self._params["conformance"] = value

    @property
    def allow_downgrade(self) -> bool:
        return self._params["allow_downgrade"]

    @allow_downgrade.setter
    def allow_downgrade(self, value: Literal[True, False]):
        """
        Allows conformance downgrade in case of conversion error.

        Accepted values are: True, False.

        Default: True

        Example:
            task.allow_downgrade = True
        """
        self._params["allow_downgrade"] = bool(value)
