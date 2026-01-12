"""Exception classes for the iLovePDF Python API."""

from .base_custom_exception import BaseCustomException


class TaskException(BaseCustomException):
    """
    Exception raised for errors related to tasks in the iLovePDF Python API.
    """


class TooManyFilesError(ValueError):
    """
    Exception raised when more than one file is added to a task that only allows one.

    Args:
        message (str): Error message. Default is "Only one file is allowed for this
            task."

    Example:
        raise TooManyFilesError()
        raise TooManyFilesError("OfficePdfTask can only handle one file at a time.")
    """

    def __init__(self, message: str = "Only one file is allowed for this task."):
        super().__init__(message)
