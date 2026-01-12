"""Unit tests for the BaseCustomException class in the ilovepdf module.

These tests verify the correct behavior of BaseCustomException, including
initialization, attribute storage, and string representation.
"""

import pytest

from ilovepdf.exceptions import BaseCustomException

# pylint: disable=protected-access


class TestBaseCustomException:
    """Unit tests for BaseCustomException."""

    def test_initialization_with_message_only(self):
        """
        Test that BaseCustomException initializes with just a message.
        """
        exc = BaseCustomException("Test error message")
        assert exc.response_body is None
        assert exc.code is None
        assert exc.errors is None

    def test_initialization_with_response_body(self):
        """
        Test that BaseCustomException initializes with message and response_body.
        """
        response = {"status": "error"}
        exc = BaseCustomException("Test error", response_body=response)
        assert exc.response_body == response
        assert exc.code is None
        assert exc.errors is None

    def test_initialization_with_code(self):
        """
        Test that BaseCustomException initializes with message and code.
        """
        exc = BaseCustomException("Test error", code=500)
        assert exc.response_body is None
        assert exc.code == 500
        assert exc.errors is None

    def test_initialization_with_errors(self):
        """
        Test that BaseCustomException initializes with message and errors.
        """
        errors = {"field": "Invalid value"}
        exc = BaseCustomException("Test error", errors=errors)
        assert exc.response_body is None
        assert exc.code is None
        assert exc.errors == errors

    def test_initialization_with_all_params(self):
        """
        Test that BaseCustomException initializes with all parameters.
        """
        response = {"status": "error"}
        errors = {"field": "Invalid"}
        exc = BaseCustomException(
            "Test error", response_body=response, code=400, errors=errors
        )
        assert exc.response_body == response
        assert exc.code == 400
        assert exc.errors == errors

    def test_str_with_message_only(self):
        """
        Test that __str__() returns only the message when no errors or response.
        """
        exc = BaseCustomException("Test error message")
        # The exception stores all args in self.args tuple, so str() includes them
        assert "Test error message" in str(exc)

    def test_str_with_errors(self):
        """
        Test that __str__() includes errors in the output when present.
        """
        errors = {"field": "Invalid"}
        exc = BaseCustomException("Test error", errors=errors)
        result = str(exc)
        assert "Test error" in result
        assert str(errors) in result
        assert "(" in result
        assert ")" in result

    def test_str_with_response_body_and_no_errors(self):
        """
        Test that __str__() includes response_body when errors are not present.
        """
        response = {"status": "error"}
        exc = BaseCustomException("Test error", response_body=response)
        result = str(exc)
        assert "Test error" in result
        assert str(response) in result
        assert "(" in result
        assert ")" in result

    def test_str_with_errors_priority_over_response_body(self):
        """
        Test that __str__() prioritizes errors over response_body.
        """
        response = {"status": "error"}
        errors = {"field": "Invalid"}
        exc = BaseCustomException("Test error", response_body=response, errors=errors)
        result = str(exc)
        assert "Test error" in result
        assert str(errors) in result

    def test_exception_is_instance_of_exception(self):
        """
        Test that BaseCustomException is an instance of Exception.
        """
        exc = BaseCustomException("Test error")
        assert isinstance(exc, Exception)

    def test_exception_can_be_raised_and_caught(self):
        """
        Test that BaseCustomException can be raised and caught properly.
        """
        with pytest.raises(BaseCustomException) as exc_info:
            raise BaseCustomException("Test error", code=400)

        assert exc_info.value.code == 400
