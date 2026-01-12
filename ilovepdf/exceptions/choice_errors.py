"""
Custom exception class for choice validation in the iLovePDF Python library.

Defines an exception for cases where a parameter value is not among the allowed choices.

Example:
    raise InvalidChoiceError("Value must be one of: jpg, png, gif.")
"""


class InvalidChoiceError(ValueError):
    """
    Exception raised when a parameter value is not among the allowed choices.

    Args:
        message (str): Error message.
        Default is "Value is not among the allowed choices."

    Example:
        raise InvalidChoiceError()
        raise InvalidChoiceError("Invalid format: png. Allowed values are: jpg, gif.")
    """

    def __init__(self, message: str = "Value is not among the allowed choices."):
        # pylint: disable=useless-super-delegation
        super().__init__(message)
