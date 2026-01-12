"""Module containing custom exception classes for iLovePDF API tasks."""


class ProcessException(Exception):
    """
    Exception raised for errors during the processing phase in iLovePDF API tasks.
    """

    def __init__(self, message, errors=None, code=None):
        super().__init__(message, errors, code)
        self.errors = errors
        self.code = code

    def get_errors(self):
        """Return the errors associated with the exception."""
        return self.errors

    def get_code(self):
        """Return the error code associated with the exception."""
        return self.code
