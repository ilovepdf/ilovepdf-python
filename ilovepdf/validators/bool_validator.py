"""Validator for boolean values.

Provides the BoolValidator class to validate boolean inputs for tasks and models.
"""

from ilovepdf.exceptions import InvalidChoiceError


# pylint: disable=too-few-public-methods
class BoolValidator:
    """Validates boolean values for input parameters.

    Example:
        validator = BoolValidator()
        validator.validate(True)
        validator.validate(False)
        # Raises InvalidChoiceError:
        validator.validate("true")
        validator.validate(1)
    """

    @staticmethod
    def validate(
        value: bool | None,
        param_name: str = "parameter",
    ) -> None:
        """
        Validates that the value is a boolean.

        Args:
            value (bool): Must be strictly True or False (not None or int).
            param_name (str, optional): Name of the parameter for error messages.

        Raises:
            InvalidChoiceError: If the value is not a valid boolean.
        """
        if not isinstance(value, bool):
            raise InvalidChoiceError(
                f"Invalid value for {param_name or 'boolean'}: must be a boolean."
            )


# bool_validator = BoolValidator()
