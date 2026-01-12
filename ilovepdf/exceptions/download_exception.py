"""Module containing custom exceptions for iLovePDF API."""

from .base_custom_exception import BaseCustomException


class DownloadException(BaseCustomException):
    """
    Exception raised for errors during file download in iLovePDF API.
    """
