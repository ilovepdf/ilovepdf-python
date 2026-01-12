"""
Unit tests for BaseFile and File classes from ilovepdf.file.

These tests cover:
- Initialization and default values
- Property setters and validation
- Error handling for invalid input
- Required fields enforcement

All tests use pytest and custom abstract test bases for consistency.
"""

import pytest

from ilovepdf.file import BaseFile, File

from .base_test import AbstractBaseFileTest, AbstractUnitFileTest


# pylint: disable=protected-access
class TestBaseFile(AbstractBaseFileTest):
    """
    Unit tests for the BaseFile class.

    Covers initialization, default values, property validation, and error handling.
    """

    _task_class = BaseFile

    @pytest.mark.parametrize(
        "server_filename, filename",
        [
            ("any_server_filename", "any_filename"),
            ("some_server_filename", "some_filename"),
        ],
    )
    def test_initialization_and_payload(self, server_filename, filename):
        """
        Test initialization and payload content for various input values.

        Asserts that attributes and payload are set correctly.
        """
        file = self._task_class(server_filename, filename)
        assert file.server_filename == server_filename
        assert file.filename == filename
        assert file._to_payload() == {
            "server_filename": server_filename,
            "filename": filename,
        }

    def test_initialization_sets_default_values(
        self, my_task
    ):  # pylint: disable=unused-argument
        """
        Test that BaseFile._DEFAULT_PAYLOAD contains expected default values.
        """
        assert BaseFile._DEFAULT_PAYLOAD == {
            "server_filename": None,
            "filename": None,
        }

    def test_set_filename(self, my_task):
        """
        Test setting the filename property with a valid string.
        """
        my_task.filename = "filename"
        assert my_task.filename == "filename"

    def test_set_filename_invalid(self, my_task):
        """
        Test that invalid values for filename raise ValueError or TypeError.
        """
        with pytest.raises(ValueError):
            my_task.filename = ""
        with pytest.raises(TypeError):
            my_task.filename = None
        with pytest.raises(TypeError):
            my_task.filename = 1234

    def test_set_server_filename(self, my_task):
        """
        Test setting the server_filename property with a valid string.
        """
        my_task.server_filename = "server_filename"
        assert my_task.server_filename == "server_filename"

    def test_set_server_filename_invalid(self, my_task):
        """
        Test that invalid values for server_filename raise ValueError or TypeError.
        """
        with pytest.raises(ValueError):
            my_task.server_filename = ""
        with pytest.raises(TypeError):
            my_task.server_filename = None
        with pytest.raises(TypeError):
            my_task.server_filename = 1234

    def test_missing_required_fields_raises(self, my_task):
        """
        Test that MissingPayloadFieldError is raised when required fields are missing.
        """
        self.assert_missing_required_fields_raise(
            my_task, ["server_filename", "filename"]
        )


class TestFile(AbstractUnitFileTest, TestBaseFile):
    """
    Unit tests for the File class.

    Covers initialization, property validation, and error handling for File.
    """

    _task_class = File

    def test_initialization_sets_default_values(self, my_task):
        """
        Test that File._DEFAULT_PAYLOAD contains expected default values.
        """
        assert my_task._DEFAULT_PAYLOAD == {
            "server_filename": None,
            "filename": None,
            "pdf_pages": None,
            "pdf_page_number": None,
            "pdf_forms": None,
        }

    @pytest.mark.parametrize(
        "server_filename, filename",
        [
            ("any_server_filename", "any_filename"),
            ("some_server_filename", "some_filename"),
        ],
    )
    def test_initialization_and_payload(self, server_filename, filename):
        """
        Test initialization and payload content for various input values.

        Asserts that attributes and payload are set correctly.
        """
        file = self._task_class(server_filename, filename)
        assert file.server_filename == server_filename
        assert file.filename == filename
        assert file._to_payload() == {
            "server_filename": server_filename,
            "filename": filename,
            "pdf_pages": None,
            "pdf_page_number": None,
            "pdf_forms": None,
        }
