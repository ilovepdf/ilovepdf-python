"""Integer validation utilities for ilovepdf-python library.

Provides the IntValidator class for validating integer values with various
constraints (type, positive, range, options).
"""

from typing import Any

from ilovepdf.exceptions import (
    IntNotInAllowedSetError,
    IntOutOfRangeError,
    NotAnIntError,
)
from ilovepdf.validators.choice_validator import ChoiceValidator


class IntValidator:
    """Validates integer values with various constraints.

    Provides static methods for validating:
    - Type validation (must be int)
    - Positive validation (must be > 0)
    - Non-negative validation (must be >= 0)
    - Range validation (must be within min/max)
    - Options validation (must be in allowed set)

    Example:
        validator = IntValidator()
        validator.validate_type(5)
        validator.validate_positive(10, "width")
        validator.validate_non_negative(0, "count")
        validator.validate_range(50, 1, 100, "quality")
    """

    @staticmethod
    def validate_type(value: Any, param_name: str = "parameter") -> None:
        """Validates that a value is of type int.

        Args:
            value (Any): Value to validate.
            param_name (str, optional): Name of the parameter. Default is
                "parameter".

        Raises:
            NotAnIntError: If value is not an integer.

        Example:
            IntValidator.validate_type(5)
            IntValidator.validate_type("abc", "width")
        """
        if not isinstance(value, int) or isinstance(value, bool):
            raise NotAnIntError(f"Invalid {param_name}: value must be an integer.")

    @staticmethod
    def validate_positive(value: Any, param_name: str = "parameter") -> None:
        """Validates that a value is a positive integer (greater than 0).

        Args:
            value (Any): Value to validate.
            param_name (str, optional): Name of the parameter. Default is
                "parameter".

        Raises:
            NotAnIntError: If value is not an integer.
            IntOutOfRangeError: If value is not positive.

        Example:
            IntValidator.validate_positive(5)
            IntValidator.validate_positive(10, "width")
        """
        IntValidator.validate_type(value, param_name)
        if value <= 0:
            raise IntOutOfRangeError(
                f"Invalid {param_name}: value must be a positive integer"
                f" (greater than 0)."
            )

    @staticmethod
    def validate_non_negative(value: Any, param_name: str = "parameter") -> None:
        """Validates that a value is a non-negative integer

        Args:
            value (Any): Value to validate.
            param_name (str, optional): Name of the parameter. Default is "parameter".

        Raises:
            NotAnIntError: If value is not an integer.
            IntOutOfRangeError: If value is negative.

        Example:
            IntValidator.validate_non_negative(0)
            IntValidator.validate_non_negative(5, "count")
        """
        IntValidator.validate_type(value, param_name)
        if value < 0:
            raise IntOutOfRangeError(
                f"Invalid {param_name}: value must be a non-negative integer"
                f" (0 or greater)."
            )

    @staticmethod
    def validate_range(
        value: Any,
        min_value: int,
        max_value: int,
        param_name: str = "parameter",
    ) -> None:
        """Validates that an integer value is within a specified range.

        Args:
            value (Any): Value to validate.
            min_value (int): Minimum allowed value (inclusive).
            max_value (int): Maximum allowed value (inclusive).
            param_name (str, optional): Name of the parameter. Default is
                "parameter".

        Raises:
            NotAnIntError: If value is not an integer.
            IntOutOfRangeError: If value is out of range.

        Example:
            IntValidator.validate_range(5, 1, 10)
            IntValidator.validate_range(15, 1, 10, "quality")
        """
        IntValidator.validate_type(value, param_name)
        if not min_value <= value <= max_value:
            raise IntOutOfRangeError(
                f"{param_name} must be between {min_value} and {max_value}."
            )

    @staticmethod
    def validate_options(
        value: Any, options: set[int], param_name: str = "parameter"
    ) -> None:
        """Validates that an integer value is among the allowed options.

        Args:
            value (Any): Value to validate.
            options (set[int]): Allowed integer values.
            param_name (str, optional): Name of the parameter. Default is
                "parameter".

        Raises:
            NotAnIntError: If value is not an integer.
            IntNotInAllowedSetError: If value is not in options.

        Example:
            IntValidator.validate_options(3, {1, 2, 3})
            IntValidator.validate_options(4, {1, 2, 3}, "mode")
        """
        IntValidator.validate_type(value, param_name)
        for opt in options:
            IntValidator.validate_type(opt, param_name)

        ChoiceValidator.validate(
            value, options, param_name, cls_error=IntNotInAllowedSetError
        )
