"""Unit tests for integer error classes in the ilovepdf module.

These tests verify the correct behavior of integer validation error classes,
including initialization, error message formatting, and exception handling.
"""

import pytest

from ilovepdf.exceptions import (
    IntNotInAllowedSetError,
    IntOutOfRangeError,
    InvalidIntValueError,
    NegativeIntError,
    NotAnIntError,
    ZeroIntError,
)

# pylint: disable=protected-access


class TestNotAnIntError:
    """Unit tests for NotAnIntError exception."""

    def test_initialization_with_message(self):
        """
        Test that NotAnIntError initializes with a message.
        """
        exc = NotAnIntError("Value must be an integer")
        assert "Value must be an integer" in str(exc)

    def test_exception_is_instance_of_exception(self):
        """
        Test that NotAnIntError is an instance of Exception.
        """
        exc = NotAnIntError("error")
        assert isinstance(exc, Exception)

    def test_exception_can_be_raised_and_caught(self):
        """
        Test that NotAnIntError can be raised and caught properly.
        """
        with pytest.raises(NotAnIntError):
            raise NotAnIntError("Not an integer")

    def test_error_with_parameter_name(self):
        """
        Test that NotAnIntError can include parameter name in message.
        """
        exc = NotAnIntError("Parameter 'width' must be an integer")
        assert "width" in str(exc)


class TestInvalidIntValueError:
    """Unit tests for InvalidIntValueError exception."""

    def test_initialization_with_message(self):
        """
        Test that InvalidIntValueError initializes with a message.
        """
        exc = InvalidIntValueError("Invalid integer value provided")
        assert "Invalid integer value" in str(exc)

    def test_exception_is_instance_of_exception(self):
        """
        Test that InvalidIntValueError is an instance of Exception.
        """
        exc = InvalidIntValueError("error")
        assert isinstance(exc, Exception)

    def test_exception_can_be_raised_and_caught(self):
        """
        Test that InvalidIntValueError can be raised and caught properly.
        """
        with pytest.raises(InvalidIntValueError):
            raise InvalidIntValueError("Invalid value")

    def test_error_with_value_details(self):
        """
        Test that InvalidIntValueError can include value details.
        """
        exc = InvalidIntValueError("Invalid value: expected positive integer")
        assert "positive integer" in str(exc)


class TestNegativeIntError:
    """Unit tests for NegativeIntError exception."""

    def test_initialization_with_message(self):
        """
        Test that NegativeIntError initializes with a message.
        """
        exc = NegativeIntError("Value cannot be negative")
        assert "cannot be negative" in str(exc)

    def test_exception_is_instance_of_exception(self):
        """
        Test that NegativeIntError is an instance of Exception.
        """
        exc = NegativeIntError("error")
        assert isinstance(exc, Exception)

    def test_exception_can_be_raised_and_caught(self):
        """
        Test that NegativeIntError can be raised and caught properly.
        """
        with pytest.raises(NegativeIntError):
            raise NegativeIntError("Negative value not allowed")

    def test_error_with_parameter_name(self):
        """
        Test that NegativeIntError can include parameter name.
        """
        exc = NegativeIntError("Parameter 'count' cannot be negative")
        assert "count" in str(exc)


class TestZeroIntError:
    """Unit tests for ZeroIntError exception."""

    def test_initialization_with_message(self):
        """
        Test that ZeroIntError initializes with a message.
        """
        exc = ZeroIntError("Value cannot be zero")
        assert "cannot be zero" in str(exc)

    def test_exception_is_instance_of_exception(self):
        """
        Test that ZeroIntError is an instance of Exception.
        """
        exc = ZeroIntError("error")
        assert isinstance(exc, Exception)

    def test_exception_can_be_raised_and_caught(self):
        """
        Test that ZeroIntError can be raised and caught properly.
        """
        with pytest.raises(ZeroIntError):
            raise ZeroIntError("Zero is not allowed")

    def test_error_with_context(self):
        """
        Test that ZeroIntError can include context information.
        """
        exc = ZeroIntError("Quality parameter cannot be zero")
        assert "Quality" in str(exc)


class TestIntOutOfRangeError:
    """Unit tests for IntOutOfRangeError exception."""

    def test_initialization_with_message(self):
        """
        Test that IntOutOfRangeError initializes with a message.
        """
        exc = IntOutOfRangeError("Value out of range")
        assert "out of range" in str(exc)

    def test_exception_is_instance_of_exception(self):
        """
        Test that IntOutOfRangeError is an instance of Exception.
        """
        exc = IntOutOfRangeError("error")
        assert isinstance(exc, Exception)

    def test_exception_can_be_raised_and_caught(self):
        """
        Test that IntOutOfRangeError can be raised and caught properly.
        """
        with pytest.raises(IntOutOfRangeError):
            raise IntOutOfRangeError("Value must be between 1 and 100")

    def test_error_with_range_details(self):
        """
        Test that IntOutOfRangeError can include range details.
        """
        exc = IntOutOfRangeError("Value must be between 0 and 100")
        assert "0" in str(exc)
        assert "100" in str(exc)

    def test_error_with_provided_value(self):
        """
        Test that IntOutOfRangeError can include the provided value.
        """
        exc = IntOutOfRangeError("Value 150 is out of range (1-100)")
        assert "150" in str(exc)


class TestIntNotInAllowedSetError:
    """Unit tests for IntNotInAllowedSetError exception."""

    def test_initialization_with_message(self):
        """
        Test that IntNotInAllowedSetError initializes with a message.
        """
        exc = IntNotInAllowedSetError("Value not in allowed set")
        assert "allowed set" in str(exc)

    def test_exception_is_instance_of_exception(self):
        """
        Test that IntNotInAllowedSetError is an instance of Exception.
        """
        exc = IntNotInAllowedSetError("error")
        assert isinstance(exc, Exception)

    def test_exception_can_be_raised_and_caught(self):
        """
        Test that IntNotInAllowedSetError can be raised and caught properly.
        """
        with pytest.raises(IntNotInAllowedSetError):
            raise IntNotInAllowedSetError("Value must be 0, 90, 180, or 270")

    def test_error_with_allowed_values(self):
        """
        Test that IntNotInAllowedSetError can include allowed values.
        """
        exc = IntNotInAllowedSetError("Allowed values: {1, 2, 3, 4, 5}")
        assert "Allowed values" in str(exc)

    def test_error_with_provided_and_allowed(self):
        """
        Test that IntNotInAllowedSetError can include both provided and allowed values.
        """
        exc = IntNotInAllowedSetError("Value 7 is not in allowed set: {1, 2, 3}")
        assert "7" in str(exc)
        assert "allowed set" in str(exc)


class TestIntErrorsInheritance:
    """Unit tests for inheritance hierarchy of integer errors."""

    def test_all_int_errors_are_exceptions(self):
        """
        Test that all integer error classes inherit from Exception.
        """
        error_classes = [
            NotAnIntError,
            InvalidIntValueError,
            NegativeIntError,
            ZeroIntError,
            IntOutOfRangeError,
            IntNotInAllowedSetError,
        ]
        for error_class in error_classes:
            exc = error_class("test")
            assert isinstance(exc, Exception)

    def test_error_messages_are_strings(self):
        """
        Test that error messages are properly converted to strings.
        """
        error_classes = [
            NotAnIntError,
            InvalidIntValueError,
            NegativeIntError,
            ZeroIntError,
            IntOutOfRangeError,
            IntNotInAllowedSetError,
        ]
        for error_class in error_classes:
            exc = error_class("test message")
            assert isinstance(str(exc), str)
            assert "test message" in str(exc)
