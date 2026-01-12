"""Provides a FloatValidator class for validating float values.

Includes methods for type checking, positive validation, range validation,
and allowed options validation for float values.
"""

from typing import Any, Optional, Set

from ilovepdf.exceptions import FloatOutOfRangeError, InvalidChoiceError


class FloatValidator:
    """Validator for float values with various constraints."""

    @staticmethod
    def validate_type(value: Any, param_name: Optional[str] = None) -> None:
        """
        Validates that the value is a float.

        Args:
            value (float): The value to validate.
            param_name (Optional[str]): The name of the parameter (for error messages).

        Raises:
            TypeError: If the value is not a float.
        """
        if not isinstance(value, (float, int)):
            name = f" for {param_name}" if param_name else ""
            raise TypeError(f"Value{name} must be a float." + str(type(value)))

    @staticmethod
    def validate_positive(value: float, param_name: Optional[str] = None) -> None:
        """
        Validates that the value is a positive float (> 0).

        Args:
            value (float): The value to validate.
            param_name (Optional[str]): The name of the parameter (for error messages).

        Raises:
            FloatOutOfRangeError: If the value is not positive.
        """
        FloatValidator.validate_type(value, param_name)
        if value <= 0:
            name = f" for {param_name}" if param_name else ""
            raise FloatOutOfRangeError(f"Value{name} must be a positive float.")

    @staticmethod
    def validate_range(
        value: float,
        min_value: float,
        max_value: float,
        param_name: Optional[str] = None,
    ) -> None:
        """
        Validates that the value is within the specified range [min_value, max_value].

        Args:
            value (float): The value to validate.
            min_value (float): Minimum allowed value.
            max_value (float): Maximum allowed value.
            param_name (Optional[str]): The name of the parameter (for error messages).

        Raises:
            FloatOutOfRangeError: If the value is outside the allowed range.
        """
        FloatValidator.validate_type(value, param_name)
        if not min_value <= value <= max_value:
            name = f" for {param_name}" if param_name else ""
            raise FloatOutOfRangeError(
                f"Value{name} must be between {min_value} and {max_value}."
            )

    @staticmethod
    def validate_options(
        value: float, options: Set[float], param_name: Optional[str] = None
    ) -> None:
        """
        Validates that the value is among the allowed options.

        Args:
            value (float): The value to validate.
            options (Set[float]): Allowed float values.
            param_name (Optional[str]): The name of the parameter (for error messages).

        Raises:
            InvalidChoiceError: If the value is not among the allowed options.
        """
        FloatValidator.validate_type(value, param_name)
        if value not in options:
            name = f" for {param_name}" if param_name else ""
            raise InvalidChoiceError(
                f"Invalid value{name}: must be one of {sorted(options)}."
            )
