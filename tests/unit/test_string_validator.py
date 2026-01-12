"""Unit tests for the StringValidator class in the ilovepdf.validators module.

These tests verify correct behavior and parameter validation for string type and
non-empty checks.
"""

import pytest

from ilovepdf.validators.string_validator import StringValidator


class TestStringValidator:
    """
    Unit tests for StringValidator.

    Covers:
    - Type validation (must be str)
    - Non-empty string validation
    - Combined validation
    """

    def test_validate_type_accepts_str(self):
        """Test that validate_type accepts a string."""
        StringValidator.validate_type("test")
        StringValidator.validate_type("")

    def test_validate_type_rejects_non_str(self):
        """Test that validate_type rejects non-string values."""
        with pytest.raises(TypeError):
            StringValidator.validate_type(123)
        with pytest.raises(TypeError):
            StringValidator.validate_type(None)
        with pytest.raises(TypeError):
            StringValidator.validate_type(3.14)
        with pytest.raises(TypeError):
            StringValidator.validate_type(["a", "b"])
        with pytest.raises(TypeError):
            StringValidator.validate_type({"a": 1})

    def test_validate_type_error_message_with_param_name(self):
        """Test that validate_type raises an error with a custom parameter name."""
        with pytest.raises(
            TypeError, match="Invalid my_param: value must be a string."
        ):
            StringValidator.validate_type(123, "my_param")

    def test_validate_not_empty_accepts_non_empty_string(self):
        """Test that validate_not_empty accepts a non-empty string."""
        StringValidator.validate_not_empty("abc")
        StringValidator.validate_not_empty(" ")

    def test_validate_not_empty_rejects_empty_string(self):
        """Test that validate_not_empty rejects an empty string."""
        with pytest.raises(ValueError):
            StringValidator.validate_not_empty("")
        # With param name
        with pytest.raises(
            ValueError, match="Invalid file_name: value must not be an empty string."
        ):
            StringValidator.validate_not_empty("", "file_name")

    def test_validate_combined_accepts_valid_string(self):
        """Test that validate_combined accepts a valid string."""
        StringValidator.validate("hello")
        StringValidator.validate("world", "param")

    def test_validate_combined_rejects_non_str(self):
        """Test that validate_combined rejects non-string values."""
        with pytest.raises(TypeError):
            StringValidator.validate(42)
        with pytest.raises(TypeError):
            StringValidator.validate(None, "param")

    def test_validate_combined_rejects_empty_string(self):
        """Test that validate_combined rejects empty strings."""
        with pytest.raises(ValueError):
            StringValidator.validate("")
        with pytest.raises(ValueError):
            StringValidator.validate("", "my_param")
