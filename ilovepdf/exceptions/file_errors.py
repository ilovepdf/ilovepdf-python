"""
This module defines custom exception classes for file validation errors.

Classes:
    FileInvalidExtensionError: Raised when a file extension is not valid.
    FileTooLargeError: Raised when a file exceeds the maximum allowed size.
    FileTooSmallError: Raised when a file is smaller than the minimum allowed size.
    FileExtensionNotAllowed: Raised when a file extension is not allowed.
    FileSizeError: Raised when a file size is not within the allowed range.
"""


class FileInvalidExtensionError(ValueError):
    """
    Exception raised when a file extension is not valid.

    Args:
        message (str): Error message. Default is "Invalid file extension."

    Example:
        raise InvalidExtensionError()
        raise InvalidExtensionError("Only .jpg and .png files are allowed.")
    """

    def __init__(self, message: str = "Invalid file extension."):
        super().__init__(message)


class FileTooLargeError(ValueError):
    """
    Exception raised when a file exceeds the maximum allowed size.

    Args:
        message (str): Error message. Default is "File exceeds the maximum allowed
            size."

    Example:
        raise FileTooLargeError()
        raise FileTooLargeError("File example.pdf exceeds the maximum allowed size
            (10 MB).")
    """

    def __init__(self, message: str = "File exceeds the maximum allowed size."):
        super().__init__(message)


class FileTooSmallError(ValueError):
    """
    Exception raised when a file is smaller than the minimum allowed size.

    Args:
        message (str): Error message. Default is "File is smaller than the minimum
        allowed size."

    Example:
        raise FileTooSmallError()
        raise FileTooSmallError("File example.pdf is smaller than the minimum allowed
        size (1 MB).")
    """

    def __init__(self, message: str = "File is smaller than the minimum allowed size."):
        super().__init__(message)


class FileExtensionNotAllowed(ValueError):
    """
    Exception raised when a file extension is not allowed.

    Args:
        message (str): Error message. Default is "File extension is not allowed."

    Example:
        raise FileExtensionNotAllowed()
        raise FileExtensionNotAllowed("Only .jpg and .png files are allowed.")
    """

    def __init__(self, message: str = "File extension is not allowed."):
        super().__init__(message)


class FileSizeError(ValueError):
    """
    Exception raised when a file size is not within the allowed range.

    Args:
        message (str): Error message. Default is "File size is not within the allowed
            range."

    Example:
        raise FileSizeError()
        raise FileSizeError("File example.pdf size is not within the allowed range
            (1 MB to 10 MB).")
    """

    def __init__(self, message: str = "File size is not within the allowed range."):
        super().__init__(message)
