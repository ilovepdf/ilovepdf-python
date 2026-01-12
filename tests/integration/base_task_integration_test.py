"""Base class for iLovePDF Task integration tests.

Provides common setup, teardown, and utility methods for integration tests
involving iLovePDF Task classes (e.g., CompressTask, ProtectTask, etc.).

Example:
    class MyTaskTest(BaseIlovePdfTaskIntegrationTest):
        task_class = CompressTask
"""

import os
import shutil
from pathlib import Path
from typing import Generic, TypeVar

import pytest

from ilovepdf.task import Task

_OUTPUT_COUNTER_FILE = Path("/tmp/ilovepdf_output_counter.txt")


def get_and_increment_global_counter() -> int:
    """
    Gets the global output file counter from a temporary file,
    increments it, and saves it. Returns the previous value (the number to use).

    Returns:
        int: The previous counter value.
    """
    if not _OUTPUT_COUNTER_FILE.exists():
        _OUTPUT_COUNTER_FILE.write_text("1", encoding="utf-8")
        return 1

    # Read current value, increment, and save
    try:
        current = int(_OUTPUT_COUNTER_FILE.read_text(encoding="utf-8").strip())
    except (ValueError, OSError):
        current = 1

    _OUTPUT_COUNTER_FILE.write_text(str(current + 1), encoding="utf-8")
    return current


T = TypeVar("T", bound=Task)


# pylint: disable=protected-access
class BaseTaskIntegrationTest(Generic[T]):
    """
    Base class for iLovePDF Task integration tests.

    Provides common setup, teardown, and utility methods for integration tests involving
    iLovePDF Task classes (e.g., CompressTask, ProtectTask, etc.).

    Attributes:
        public_key (str): iLovePDF public API key from environment.
        secret_key (str): iLovePDF secret API key from environment.
        folder_sample_path (str): Base path for sample files.
        sample_file_path (str): Path to the sample PDF file for testing.
        task_class (type[Task]): The Task class to instantiate (must be set by
            subclass).
        task (Task | None): Instance of the Task class.
        downloaded_file (str | None): Path to the downloaded output file.

    Example:
        class MyTaskTest(BaseIlovePdfTaskIntegrationTest):
            task_class = CompressTask
    """

    # Class-level attributes with default values
    public_key: str = os.environ.get("ILOVEPDF_PUBLIC_KEY", "")
    secret_key: str = os.environ.get("ILOVEPDF_SECRET_KEY", "")
    folder_sample_path: str = os.environ.get(
        "FOLDER_SAMPLE_PATH", os.path.join("tests", "integration", "files_samples")
    )
    sample_file_path: str = "sample.pdf"
    task_class: type[T]
    task: T
    downloaded_file: str | None = None

    @pytest.fixture(scope="class", autouse=True)
    def setup_class(self):
        """
        Sets up class-level requirements before running any integration tests.

        Skips tests if required environment variables or sample folders are missing.

        Example:
            # Used automatically by pytest before running tests in the class.
        """
        if not self.public_key or not self.secret_key:
            pytest.skip("iLovePDF API credentials not found in environment variables.")

        if not os.path.exists(self.folder_sample_path):
            pytest.skip(f"Sample folder path not found at {self.folder_sample_path}.")

        # Configure sample_file_path for use in tests
        self.sample_file_path = self.resolve_sample_file_path(self.sample_file_path)

    @pytest.fixture(autouse=True)
    def setup_task(self):
        """
        Sets up a new Task instance before each integration test and performs cleanup
            after.

        This fixture is automatically used for each test method.

        Example:
            # Used automatically by pytest before each test.
        """
        if self.task_class is None:
            raise NotImplementedError(
                "Subclasses must set 'task_class' to a valid Task class."
            )

        # Create a new Task instance before each test
        self.task = self.task_class(self.public_key, self.secret_key)
        self.downloaded_file = None

        yield

        # Cleanup after test: remove downloaded file and delete remote task
        if self.downloaded_file and os.path.exists(self.downloaded_file):
            self.maybe_copy_output_file()
            os.remove(self.downloaded_file)

        if hasattr(self, "task") and getattr(self.task, "task_id", None):
            try:
                self.task.delete()
            except (AttributeError, RuntimeError, OSError):
                pass

    def resolve_sample_file_path(self, filename: str) -> str:
        """
        Resolves and returns the full path of the sample file.

        Args:
            filename (str): Name of the sample file.

        Returns:
            str: Full path to the sample file.

        Raises:
            pytest.skip: If the sample file does not exist.

        Example:
            path = self.resolve_sample_file_path("image_sample.jpg")
        """
        full_path = os.path.join(self.folder_sample_path, filename)
        if not os.path.exists(full_path):
            pytest.skip(f"Sample file not found at {full_path}.")
        return full_path

    def maybe_copy_output_file(
        self, keep_env_var: str = "ILOVEPDF_KEEP_OUTPUT_DIR"
    ) -> str | None:
        """
        Copies the output file to a persistent location if the specified environment
        variable is set.

        Args:
            keep_env_var (str): Name of the environment variable that contains the
                output directory path.

        Returns:
            str | None: Path to the copied file, or None if no copy was made.

        Example:
            copied_path = self.maybe_copy_output_file()
        """
        keep_dir = os.getenv(keep_env_var)
        if (
            not keep_dir
            or not self.downloaded_file
            or not os.path.exists(self.downloaded_file)
        ):
            return None

        # Use a global counter file to avoid output filename collisions across tests.
        os.makedirs(keep_dir, exist_ok=True)
        counter = get_and_increment_global_counter()

        class_name = self.__class__.__name__
        original_filename = os.path.basename(self.downloaded_file)
        dest_filename = f"{counter}_{class_name}_{original_filename}"
        dest_path = os.path.join(keep_dir, dest_filename)

        shutil.copy(self.downloaded_file, dest_path)
        return dest_path

    def add_sample_file(self, filename: str | None = None):
        """
        Adds a sample file to the task.


        Args:
            filename (str | None): Optional name of the sample file to add.
            If not provided, uses the default sample file path.

        Returns:
            dict: The uploaded file object as returned by the task.

        Example:
            file_obj = self.add_sample_file("image_sample.jpg")
        """
        filename = self.resolve_sample_file_path(filename or self.sample_file_path)
        return self.task.add_file(filename)

    def execute_task(self) -> None:
        """
        Execute the task and assert that it succeeded.

        Raises:
            AssertionError: If the task did not succeed.

        Example:
            self.execute_task()
        """

        task_status = self.task_class._task_status
        if not task_status:
            raise ValueError("Task status is not defined")

        self.task.execute()
        assert self.task.status == task_status, (
            f"Task failed with status: {self.task.status}. "
            f"Message: {getattr(self.task, 'status_message', '')}."
        )

    def download_result(self, output_filename: str) -> None:
        """
        Download the result file and assert its existence and non-zero size.

        Args:
            output_filename (str): Name to use for the downloaded file.

        Raises:
            AssertionError: If the downloaded file does not exist or is empty.

        Example:
            self.download_result("output.jpg")
        """
        self.task.set_output_filename(output_filename)
        self.task.download()
        self.downloaded_file = output_filename

        assert os.path.exists(
            self.downloaded_file
        ), f"Downloaded file '{self.downloaded_file}' does not exist."
        assert (
            os.path.getsize(self.downloaded_file) > 0
        ), f"Downloaded file '{self.downloaded_file}' is empty."
