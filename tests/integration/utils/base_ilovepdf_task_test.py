"""Base class for iLovePDF Task integration tests.

Provides common setup, teardown, and utility methods for tests involving
iLovePDF Task classes (e.g., CompressTask, ProtectTask, etc.).
"""

import inspect
import os
import unittest
from typing import Any, Callable, Optional


class BaseIlovePdfTaskTest(unittest.TestCase):
    """
    Base class for iLovePDF Task integration tests.

    Provides common setup, teardown, and utility methods for tests involving
    iLovePDF Task classes (e.g., CompressTask, ProtectTask, etc.).

    Attributes:
        public_key (str): iLovePDF public API key from environment.
        secret_key (str): iLovePDF secret API key from environment.
        sample_file_path (str): Path to the sample PDF file for testing.
        task_class (type): The Task class to instantiate (must be set by subclass).
        task (object): Instance of the Task class.
        downloaded_file (str): Path to the downloaded output file (if any).
    """

    public_key = os.environ.get("ILOVEPDF_PUBLIC_KEY")
    secret_key = os.environ.get("ILOVEPDF_SECRET_KEY")
    folder_sample_path = os.environ.get(
        "FOLDER_SAMPLE_PATH", "tests/integration/files_samples"
    )
    sample_file_path = "sample.pdf"  # Default; can be overridden in subclass

    task_class: Optional[Callable[[str, str], Any]] = (
        None  # Subclasses must set this to the appropriate Task class
    )

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        if not cls.public_key or not cls.secret_key:
            raise unittest.SkipTest(
                "iLovePDF API credentials not found in environment variables."
            )
        if cls.folder_sample_path:
            if not os.path.exists(cls.folder_sample_path):
                raise unittest.SkipTest(
                    f"Sample folder path not found at {cls.folder_sample_path}"
                )
        if cls.sample_file_path:
            cls.sample_file_path = os.path.join(
                cls.folder_sample_path, cls.sample_file_path
            )
            if not os.path.exists(cls.sample_file_path):
                raise unittest.SkipTest(
                    f"Sample file not found at {cls.sample_file_path}"
                )

    def setUp(self):

        if self.task_class is None or not inspect.isclass(self.task_class):
            raise NotImplementedError(
                f"Subclasses must set 'task_class' to a valid Task class, got: {self.task_class!r}"
            )
        # We've verified task_class is a class above, so it's safe to call
        # pylint: disable-next=not-callable
        self.task = self.task_class(self.public_key, self.secret_key)
        self.downloaded_file = None

    def tearDown(self):
        # Remove downloaded file if it exists
        if self.downloaded_file and os.path.exists(self.downloaded_file):
            os.remove(self.downloaded_file)
        # Attempt to delete the remote task if supported
        if hasattr(self, "task") and getattr(self.task, "task_id", None):
            try:
                self.task.delete()
            except (AttributeError, RuntimeError, OSError):
                pass  # Ignore errors on cleanup

    def add_sample_file(self):
        """
        Adds the sample file to the task and returns the uploaded file object.
        """
        return self.task.add_file(self.sample_file_path)

    def execute_task(self):
        """
        Executes the task and asserts that it succeeded.
        """
        self.task.execute()
        self.assertEqual(
            getattr(self.task, "status", None),
            "TaskSuccess",
            f"Task failed with status: {getattr(self.task, 'status', None)}"
            f"and message: {getattr(self.task, 'status_message', '')}",
        )

    def download_result(self, output_filename):
        """
        Downloads the result file and asserts its existence and non-zero size.
        """
        self.task.set_output_filename(output_filename)
        self.task.download()
        self.downloaded_file = output_filename
        self.assertTrue(
            os.path.exists(self.downloaded_file),
            f"Downloaded file '{self.downloaded_file}' does not exist.",
        )
        self.assertTrue(
            os.path.getsize(self.downloaded_file) > 0,
            f"Downloaded file '{self.downloaded_file}' is empty.",
        )
