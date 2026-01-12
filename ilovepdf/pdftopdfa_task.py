"""Handles PDF to PDF/A conversion workflows using the iLovePDF API."""

from typing import Literal

from .task import Task
from .validators import BoolValidator, ChoiceValidator

PDFA_CONFORMANCE_OPTIONS = {
    "pdfa-1b",
    "pdfa-1a",
    "pdfa-2b",
    "pdfa-2u",
    "pdfa-2a",
    "pdfa-3b",
    "pdfa-3u",
    "pdfa-3a",
}


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


class PdfToPdfATask(Task):
    """Handles PDF to PDF/A conversion using the iLovePDF API.

    Args:
        public_key (str | None): API public key. Uses the ILOVEPDF_PUBLIC_KEY
            environment variable when omitted.
        secret_key (str | None): API secret key. Uses the ILOVEPDF_SECRET_KEY
            environment variable when omitted.
        make_start (bool): Whether to start the task automatically. Default is False.

    Example:
        task = PdfToPdfATask(public_key="your_public_key", secret_key="your_secret")
        task.add_file("/path/to/document.pdf")
        task.conformance = "pdfa-1a"
        task.execute()
        task.download("/path/to/output.pdf")
    """

    _tool = "pdfa"

    _DEFAULT_PAYLOAD = {
        "conformance": "pdfa-2b",
        "allow_downgrade": True,
    }

    @property
    def conformance(self) -> ConformanceType:
        """Gets the PDF/A conformance level.

        Returns:
            ConformanceType: The current value. Default is "pdfa-2b".
        """
        return self._get_attr("conformance")

    @conformance.setter
    def conformance(self, value: ConformanceType) -> None:
        """Sets the PDF/A conformance level.

        Args:
            value (ConformanceType): Must match ``PDFA_CONFORMANCE_OPTIONS``.

        Raises:
            InvalidChoiceError: If the provided value is not supported.
        """
        ChoiceValidator.validate(value, PDFA_CONFORMANCE_OPTIONS, "conformance")
        self._set_attr("conformance", value)

    @property
    def allow_downgrade(self) -> bool:
        """Gets whether conformance downgrade is allowed.

        Returns:
            bool: True when downgrade is permitted. Default is True.
        """
        return self._get_attr("allow_downgrade")

    @allow_downgrade.setter
    def allow_downgrade(self, value: bool) -> None:
        """Sets whether conformance downgrade is permitted.

        Args:
            value (bool): Must be a boolean value.

        Raises:
            TypeError: If ``value`` is not a boolean.
        """
        BoolValidator.validate(value, "allow_downgrade")
        self._set_attr("allow_downgrade", value)
