"""
Custom exception classes for float value validation in the iLovePDF Python library.

This module defines exceptions for type and value errors related to float parameters,
following project documentation and style guidelines.

Example:
    raise NotAFloatError("Value must be of type float.")
    raise FloatOutOfRangeError("Value must be between 0.0 and 1.0.")
"""


class NotAFloatError(TypeError):
    """
    Exception raised when a value is not of type float.

    Args:
        message (str): Error message. Default is "Value must be of type float."

    Example:
        raise NotAFloatError()
        raise NotAFloatError("Invalid opacity: value must be a float.")
    """

    def __init__(self, message: str = "Value must be of type float."):
        # pylint: disable=useless-super-delegation
        super().__init__(message)


class InvalidFloatValueError(ValueError):
    """
    Exception raised when a float value is invalid.

    Args:
        message (str): Error message. Default is "Invalid float value provided."

    Example:
        raise InvalidFloatValueError()
        raise InvalidFloatValueError("Invalid scale: must be a positive float.")
    """

    def __init__(self, message: str = "Invalid float value provided."):
        # pylint: disable=useless-super-delegation
        super().__init__(message)


class FloatOutOfRangeError(ValueError):
    """
    Exception raised when a float value is outside the allowed range.

    Args:
        message (str): Error message. Default is "Value is outside the allowed range."

    Example:
        raise FloatOutOfRangeError()
        raise FloatOutOfRangeError("Opacity must be between 0.0 and 1.0.")
    """

    def __init__(self, message: str = "Value is outside the allowed range."):
        # pylint: disable=useless-super-delegation
        super().__init__(message)


class NegativeFloatError(ValueError):
    """
    Exception raised when a negative float is not allowed.

    Args:
        message (str): Error message. Default is "Negative values are not permitted."

    Example:
        raise NegativeFloatError()
        raise NegativeFloatError("Scale cannot be negative.")
    """

    def __init__(self, message: str = "Negative values are not permitted."):
        # pylint: disable=useless-super-delegation
        super().__init__(message)


class ZeroFloatError(ValueError):
    """
    Exception raised when zero is not allowed as a float value.

    Args:
        message (str): Error message. Default is "Zero is not a valid value for this
            parameter."

    Example:
        raise ZeroFloatError()
        raise ZeroFloatError("Scale factor must be greater than zero.")
    """

    def __init__(self, message: str = "Zero is not a valid value for this parameter."):
        # pylint: disable=useless-super-delegation
        super().__init__(message)


class FloatNotInAllowedSetError(ValueError):
    """
    Exception raised when a float value is not in the allowed set.

    Args:
        message (str): Error message. Default is "Value is not in the allowed set."

    Example:
        raise FloatNotInAllowedSetError()
        raise FloatNotInAllowedSetError(
            "Invalid opacity: value must be one of [0.0, 0.5, 1.0]."
        )
    """

    def __init__(self, message: str = "Value is not in the allowed set."):
        # pylint: disable=useless-super-delegation
        super().__init__(message)
