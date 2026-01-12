"""Unit tests for the UnlockTask class from ilovepdf.

This module contains tests to verify the correct behavior of UnlockTask,
including initialization and file validation logic.
"""

import pytest

from ilovepdf import UnlockTask


class TestUnlockTask:
    """Unit tests for the UnlockTask class from ilovepdf."""

    @pytest.fixture
    def unlock_task(self):
        """Fixture that creates an UnlockTask instance for testing."""
        # Use real initialization for functional tests
        task = UnlockTask("public_key", "secret_key", make_start=False)
        task.task = "dummy_task_id"  # Simulate started task for add_file validation
        return task

    def test_initialization_sets_tool_unlock(self, unlock_task):
        """
        Ensure UnlockTask is initialized with the correct tool value.
        """
        assert unlock_task.tool == "unlock", "Tool should be set to 'unlock'"

    def test_add_file_raises_on_non_pdf(self, unlock_task, tmp_path):
        """
        Ensure add_file raises ValueError if file is not a PDF.
        """
        # Create a dummy txt file
        txt_file = tmp_path / "not_a_pdf.txt"
        txt_file.write_text("This is not a PDF file.")
        with pytest.raises(ValueError):
            unlock_task.add_file(str(txt_file))

        # Create a file with .pdf extension but wrong content
        fake_pdf = tmp_path / "fake.pdf"
        fake_pdf.write_text("Not really a PDF")
        with pytest.raises(ValueError):
            unlock_task.add_file(str(fake_pdf))
