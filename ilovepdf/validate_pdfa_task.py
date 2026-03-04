"""Handles PDF/A compliance validation using the iLovePDF API.

Provides the ValidatePdfATask class to check if a PDF file is PDF/A compliant.
Allows configuration of the PDF/A conformance level and downgrade policy.

Example:
    task = ValidatePdfATask(public_key="your_public_key", secret_key="your_secret")
    task.add_file("/path/to/document.pdf")
    task.conformance = "pdfa-1a"
    task.allow_downgrade = True
    task.execute()
    result = task.validation_result
    if result and result.get("status") == "Conformant":
        print("The file is PDF/A compliant.")
"""

from typing import Any, Literal

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


class ValidatePdfATask(Task):
    """Handles PDF/A compliance validation using the iLovePDF API.

    Args:
        public_key (str | None): API public key. Uses the ILOVEPDF_PUBLIC_KEY
            environment variable when omitted.
        secret_key (str | None): API secret key. Uses the ILOVEPDF_SECRET_KEY
            environment variable when omitted.
        make_start (bool): Whether to start the task automatically. Default is False.

    Example:
        task = ValidatePdfATask(public_key="your_public_key", secret_key="your_secret")
        task.add_file("/path/to/document.pdf")
        task.conformance = "pdfa-1a"
        task.allow_downgrade = True
        task.execute()
        result = task.validation_result
        if result and result.get("status") == "Conformant":
            print("The file is PDF/A compliant.")
    """

    _tool = "validatepdfa"

    _DEFAULT_PAYLOAD = {
        "conformance": "pdfa-2b",
        "allow_downgrade": True,
    }

    allowed_extensions = ["pdf"]

    def __init__(
        self,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self._validation_result: dict[str, Any] | None = None

    @property
    def conformance(self) -> ConformanceType:
        """
        Gets the PDF/A conformance level.

        Returns:
            ConformanceType: The current value. Default is "pdfa-2b".
        """
        return self._get_attr("conformance")

    @conformance.setter
    def conformance(self, value: ConformanceType) -> None:
        """
        Sets the PDF/A conformance level.

        Args:
            value (ConformanceType): Must match PDFA_CONFORMANCE_OPTIONS.

        Raises:
            InvalidChoiceError: If the provided value is not supported.
        """
        ChoiceValidator.validate(value, PDFA_CONFORMANCE_OPTIONS, "conformance")
        self._set_attr("conformance", value)

    @property
    def allow_downgrade(self) -> bool:
        """
        Gets whether conformance downgrade is allowed.

        Returns:
            bool: True when downgrade is permitted. Default is True.
        """
        return self._get_attr("allow_downgrade")

    @allow_downgrade.setter
    def allow_downgrade(self, value: bool) -> None:
        """
        Sets whether conformance downgrade is permitted.

        Args:
            value (bool): Must be a boolean value.

        Raises:
            TypeError: If value is not a boolean.
        """
        BoolValidator.validate(value, "allow_downgrade")
        self._set_attr("allow_downgrade", value)

    def execute(self) -> "ValidatePdfATask":
        """
        Executes the PDF/A validation task.

        Returns:
            ValidatePdfATask: Self for chaining.

        Raises:
            Exception: If the API call fails or the response is invalid.
        """
        super().execute()
        self._extract_validation_result()
        return self

    @property
    def validation_result(self) -> dict[str, Any] | None:
        """
        Get the PDF/A validation result after execution.

        Returns:
            dict[str, Any] | None: The validation result dictionary, or None if not
                executed.

        Example:
            result = task.validation_result
            if result and result.get("status") == "Conformant":
                print("The file is PDF/A compliant.")
        """
        return self._validation_result

    def _extract_validation_result(self) -> None:
        """Extracts the validation result from the API response."""
        result = getattr(self, "result", None)
        if result and isinstance(result, dict):
            validations = result.get("validations")
            if isinstance(validations, list) and validations:
                self._validation_result = validations[0]
            else:
                self._validation_result = None
        else:
            self._validation_result = None
