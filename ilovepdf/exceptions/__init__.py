"""Exception package for iLovePDF Python library.

This package contains custom exception classes used throughout the iLovePDF API integration.
"""

from .auth_exception import AuthException  # noqa
from .download_exception import DownloadException  # noqa
from .not_implemented_exception import NotImplementedException  # noqa
from .path_exception import PathException  # noqa
from .process_exception import ProcessException  # noqa
from .signature_exception import SignatureException  # noqa
from .start_exception import StartException  # noqa
from .task_exception import TaskException  # noqa
from .upload_exception import UploadException  # noqa

__all__ = [
    "AuthException",
    "DownloadException",
    "NotImplementedException",
    "PathException",
    "ProcessException",
    "SignatureException",
    "StartException",
    "TaskException",
    "UploadException",
]
