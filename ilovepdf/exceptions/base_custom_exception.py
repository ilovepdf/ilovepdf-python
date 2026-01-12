"""Custom exception base class for application-specific error handling."""


class BaseCustomException(Exception):
    """Base exception class for custom application errors."""

    def __init__(self, message, response_body=None, code=None, errors=None):
        super().__init__(message, response_body, code, errors)
        self.response_body = response_body
        self.code = code
        self.errors = errors

    def __str__(self):
        base = super().__str__()
        if self.errors:
            return f"{base} ({self.errors})"
        if self.response_body:
            return f"{base} ({self.response_body})"
        return base
