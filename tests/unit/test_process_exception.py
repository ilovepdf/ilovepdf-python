"""Unit tests for the ProcessException class in the ilovepdf module.

These tests verify the correct behavior of ProcessException, including
initialization, error storage, and retrieval methods.
"""

import pytest

from ilovepdf.exceptions import ProcessException

# pylint: disable=protected-access


class TestProcessException:
    """Unit tests for ProcessException."""

    def test_initialization_with_message_only(self):
        """
        Test that ProcessException initializes with just a message.
        """
        exc = ProcessException("Test error message")
        assert exc.errors is None
        assert exc.code is None

    def test_initialization_with_errors(self):
        """
        Test that ProcessException initializes with message and errors.
        """
        errors = {"field": "Invalid value"}
        exc = ProcessException("Test error", errors=errors)
        assert exc.errors == errors
        assert exc.code is None

    def test_initialization_with_code(self):
        """
        Test that ProcessException initializes with message and code.
        """
        exc = ProcessException("Test error", code=500)
        assert exc.errors is None
        assert exc.code == 500

    def test_initialization_with_all_params(self):
        """
        Test that ProcessException initializes with all parameters.
        """
        errors = {"field": "Invalid value"}
        exc = ProcessException("Test error", errors=errors, code=400)
        assert exc.errors == errors
        assert exc.code == 400

    def test_get_errors_with_none(self):
        """
        Test that get_errors() returns None when no errors are set.
        """
        exc = ProcessException("Test error")
        assert exc.get_errors() is None

    def test_get_errors_with_dict(self):
        """
        Test that get_errors() returns the errors dictionary.
        """
        errors = {"field1": "error1", "field2": "error2"}
        exc = ProcessException("Test error", errors=errors)
        assert exc.get_errors() == errors

    def test_get_errors_with_list(self):
        """
        Test that get_errors() returns the errors list.
        """
        errors = ["error1", "error2"]
        exc = ProcessException("Test error", errors=errors)
        assert exc.get_errors() == errors

    def test_get_code_with_none(self):
        """
        Test that get_code() returns None when no code is set.
        """
        exc = ProcessException("Test error")
        assert exc.get_code() is None

    def test_get_code_with_value(self):
        """
        Test that get_code() returns the error code.
        """
        exc = ProcessException("Test error", code=429)
        assert exc.get_code() == 429

    def test_exception_is_instance_of_exception(self):
        """
        Test that ProcessException is an instance of Exception.
        """
        exc = ProcessException("Test error")
        assert isinstance(exc, Exception)

    def test_exception_can_be_raised_and_caught(self):
        """
        Test that ProcessException can be raised and caught properly.
        """
        with pytest.raises(ProcessException) as exc_info:
            raise ProcessException("Test error", code=500)

        assert exc_info.value.code == 500
        assert exc_info.value.get_code() == 500
