"""Handles PDF form detection tasks using the iLovePDF API.

Provides the FormsDetectTask class to configure and execute PDF form field detection.
Identifies form fields contained in PDF documents.
"""

from .task import Task


class FormsDetectTask(Task):
    """
    Handles PDF form detection tasks using the iLovePDF API.

    Args:
        public_key (str, optional): API public key.
            Uses ILOVEPDF_PUBLIC_KEY env variable if not provided.
        secret_key (str, optional): API secret key.
            Uses ILOVEPDF_SECRET_KEY env variable if not provided.
        make_start (bool, optional): Start the task immediately. Default is False.

    Example:
        task = FormsDetectTask(public_key="public_key", secret_key="secret_key")
        task.add_file("document.pdf")
        task.execute()
        task.download("output_folder")
    """

    _tool = "formsdetect"
