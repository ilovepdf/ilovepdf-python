"""Exception class for signature processing errors in iLovePDF API."""

from .base_custom_exception import BaseCustomException


class SignatureException(BaseCustomException):
    """
    Exception raised for errors related to signature processing in iLovePDF API.
    """
