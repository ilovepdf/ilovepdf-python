"""
Custom exception classes for integer value validation in the iLovePDF Python library.

This module defines exceptions for type and value errors related to integer parameters,
following project documentation and style guidelines.

Example:
    raise NotAnIntError("Value must be of type int.")
    raise IntOutOfRangeError("Value must be between 1 and 10.")
"""


class NotAnIntError(TypeError):
    """
    Exception raised when a value is not of type int.

    Args:
        message (str): Error message. Default is "Value must be of type int."

    Example:
        raise NotAnIntError()
        raise NotAnIntError("Invalid width: value must be an integer.")
    """

    def __init__(self, message: str = "Value must be of type int."):
        # pylint: disable=useless-super-delegation
        super().__init__(message)


class InvalidIntValueError(ValueError):
    """
    Exception raised when an integer value is invalid.

    Args:
        message (str): Error message. Default is "Invalid integer value provided."

    Example:
        raise InvalidIntValueError()
        raise InvalidIntValueError("Invalid page number: must be a positive integer.")
    """

    def __init__(self, message: str = "Invalid integer value provided."):
        # pylint: disable=useless-super-delegation
        super().__init__(message)


class IntOutOfRangeError(ValueError):
    """
    Exception raised when an integer value is outside the allowed range.

    Args:
        message (str): Error message. Default is "Value is outside the allowed range."

    Example:
        raise IntOutOfRangeError()
        raise IntOutOfRangeError("Quality must be between 1 and 100.")
    """

    def __init__(self, message: str = "Value is outside the allowed range."):
        # pylint: disable=useless-super-delegation
        super().__init__(message)


class NegativeIntError(ValueError):
    """
    Exception raised when a negative integer is not allowed.

    Args:
        message (str): Error message. Default is "Negative values are not permitted."

    Example:
        raise NegativeIntError()
        raise NegativeIntError("Width cannot be negative.")
    """

    def __init__(self, message: str = "Negative values are not permitted."):
        # pylint: disable=useless-super-delegation
        super().__init__(message)


class ZeroIntError(ValueError):
    """
    Exception raised when zero is not allowed as an integer value.

    Args:
        message (str): Error message. Default is "Zero is not a valid value for this
            parameter."

    Example:
        raise ZeroIntError()
        raise ZeroIntError("Page count must be greater than zero.")
    """

    def __init__(self, message: str = "Zero is not a valid value for this parameter."):
        # pylint: disable=useless-super-delegation
        super().__init__(message)


class IntNotInAllowedSetError(ValueError):
    """
    Exception raised when an integer value is not in the allowed set.

    Args:
        message (str): Error message. Default is "Value is not in the allowed set."

    Example:
        raise IntNotInAllowedSetError()
        raise IntNotInAllowedSetError(
            "Invalid rotation: value must be one of [90, 180, 270]."
        )
    """

    def __init__(self, message: str = "Value is not in the allowed set."):
        # pylint: disable=useless-super-delegation
        super().__init__(message)
