"""Unit tests for the ProtectTask class in the ilovepdf module.

This module contains unit tests for the ProtectTask class, which is part of the ilovepdf module.
The tests cover initialization, password setting, dictionary representation, and file addition validation.
"""

import pytest

from ilovepdf import ProtectTask


class TestProtectTask:
    """Unit tests for the ProtectTask class."""

    @pytest.fixture
    def protect_task(self):
        """Fixture that creates a ProtectTask instance for testing."""
        task = ProtectTask("public_key", "secret_key", make_start=False)
        return task

    def test_initialization_sets_default_values(self, protect_task):
        """
        Ensure ProtectTask is initialized with default values.
        Checks that the default password is None and the tool is set to 'protect'.
        """
        assert protect_task.password is None, "Default password should be None"
        assert protect_task.tool == "protect", "Tool should be set to 'protect'"

    def test_set_password_assigns_password_correctly(self, protect_task):
        """
        Ensure set_password assigns the password correctly.
        """
        protect_task.set_password("my_password")
        assert (
            protect_task.password == "my_password"
        ), "Password attribute should match the set value"
        assert (
            protect_task._to_dict()["password"]  # pylint: disable=protected-access
            == "my_password"
        ), "Password should be present in the dictionary representation"

    def test_to_dict_includes_password(self, protect_task):
        """
        Ensure that _to_dict includes the password when set.
        """
        protect_task.set_password("my_password")
        assert (
            protect_task._to_dict()["password"]  # pylint: disable=protected-access
            == "my_password"
        ), "Password should be included in the dictionary representation"

    def test_set_password_raises_on_empty_or_non_string(self, protect_task):
        """
        Ensure set_password raises ValueError if password is empty or not a string.
        """
        with pytest.raises(ValueError):
            protect_task.set_password("")
        with pytest.raises(ValueError):
            protect_task.set_password(None)
        with pytest.raises(ValueError):
            protect_task.set_password(12345)

    def test_add_file_raises_on_non_pdf(self, protect_task, tmp_path):
        """
        Ensure add_file raises ValueError if file is not a PDF.
        """
        # Create a dummy txt file
        txt_file = tmp_path / "not_a_pdf.txt"
        txt_file.write_text("This is not a PDF file.")
        with pytest.raises(ValueError):
            protect_task.add_file(str(txt_file))

        # Create a file with .pdf extension but wrong content
        fake_pdf = tmp_path / "fake.pdf"
        fake_pdf.write_text("Not really a PDF")
        with pytest.raises(ValueError):
            protect_task.add_file(str(fake_pdf))
