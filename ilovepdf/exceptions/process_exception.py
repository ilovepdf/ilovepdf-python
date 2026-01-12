"""Module containing custom exception classes for iLovePDF API tasks."""


class ProcessException(Exception):
    """
    Exception raised for errors during the processing phase in iLovePDF API tasks.
    """

    def __init__(self, message, errors=None, code=None):
        super().__init__(message)
        self.errors = errors
        self.code = code

    def get_errors(self):
        return self.errors

    def get_code(self):
        return self.code
