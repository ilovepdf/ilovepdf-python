"""Choice validation utilities for ilovepdf-python library.

Provides the ChoiceValidator class for validating values against a set
of allowed choices.
"""

from typing import Any, Iterable

from ilovepdf.exceptions import InvalidChoiceError


# pylint: disable=too-few-public-methods
class ChoiceValidator:
    """Validates that values are among allowed choices.

    Example:
        validator = ChoiceValidator()
        validator.validate("jpg", ["jpg", "png", "gif"])
        validator.validate(90, {0, 90, 180, 270}, "rotation")
    """

    @staticmethod
    def validate(
        value: Any,
        allowed: Iterable[Any],
        param_name: str = "parameter",
        cls_error: type[Exception] = InvalidChoiceError,
    ) -> None:
        """Validates if a value is among the allowed choices.

        Args:
            value (Any): The value to validate.
            allowed (Iterable[Any]): The set of allowed values.
            param_name (str, optional): The name of the parameter. Default is
                "parameter".
            cls_error (type[Exception], optional): The exception class to
                raise if validation fails. Default is InvalidChoiceError.

        Raises:
            InvalidChoiceError or cls_error: If value is not among allowed
                choices.

        Example:
            ChoiceValidator.validate("jpg", ["jpg", "png"])
            ChoiceValidator.validate(90, {0, 90, 180, 270}, "angle")
        """
        allowed = list(allowed)
        try:
            allowed_display = ", ".join(map(str, allowed))
        except TypeError:
            allowed_display = str(allowed)

        error_message = (
            f"Invalid value `{param_name}`: value must be one of " f"{allowed_display}."
        )

        if value not in allowed:
            raise cls_error(error_message)
