"""Unit tests for ChoiceValidator.

Covers all validation methods of ChoiceValidator, including edge cases and error
handling with different value types and custom exceptions.
"""

import pytest

from ilovepdf.exceptions import IntNotInAllowedSetError, InvalidChoiceError
from ilovepdf.validators import ChoiceValidator

# pylint: disable=protected-access,too-few-public-methods


class TestChoiceValidatorBasic:
    """Tests for basic ChoiceValidator.validate() functionality."""

    def test_validate_with_valid_string_choice(self):
        """Test that valid string choices pass validation."""
        ChoiceValidator.validate("jpg", ["jpg", "png", "gif"])
        ChoiceValidator.validate("png", ["jpg", "png", "gif"])
        ChoiceValidator.validate("gif", ["jpg", "png", "gif"])

    def test_validate_with_valid_int_choice(self):
        """Test that valid integer choices pass validation."""
        ChoiceValidator.validate(0, [0, 90, 180, 270])
        ChoiceValidator.validate(90, [0, 90, 180, 270])
        ChoiceValidator.validate(180, [0, 90, 180, 270])
        ChoiceValidator.validate(270, [0, 90, 180, 270])

    def test_validate_with_invalid_string_choice(self):
        """Test that invalid string choices raise InvalidChoiceError."""
        with pytest.raises(InvalidChoiceError) as excinfo:
            ChoiceValidator.validate("bmp", ["jpg", "png", "gif"])
        assert "Invalid value `parameter`: value must be one of" in str(excinfo.value)
        assert "jpg, png, gif" in str(excinfo.value)

    def test_validate_with_invalid_int_choice(self):
        """Test that invalid integer choices raise InvalidChoiceError."""
        with pytest.raises(InvalidChoiceError) as excinfo:
            ChoiceValidator.validate(45, [0, 90, 180, 270])
        assert "Invalid value `parameter`: value must be one of" in str(excinfo.value)

    def test_validate_with_custom_param_name(self):
        """Test that custom parameter name appears in error message."""
        with pytest.raises(InvalidChoiceError) as excinfo:
            ChoiceValidator.validate("invalid", ["a", "b", "c"], param_name="format")
        assert "Invalid value `format`:" in str(excinfo.value)

    def test_validate_with_none_value(self):
        """Test that None can be validated as a choice."""
        ChoiceValidator.validate(None, [None, "a", "b"])

        with pytest.raises(InvalidChoiceError):
            ChoiceValidator.validate(None, ["a", "b", "c"])


class TestChoiceValidatorWithSet:
    """Tests for ChoiceValidator with set-based allowed values."""

    def test_validate_with_valid_choice_in_set(self):
        """Test that valid choices in set pass validation."""
        ChoiceValidator.validate(1, {1, 2, 3})
        ChoiceValidator.validate("low", {"low", "medium", "high"})

    def test_validate_with_invalid_choice_in_set(self):
        """Test that invalid choices raise error."""
        with pytest.raises(InvalidChoiceError) as excinfo:
            ChoiceValidator.validate(4, {1, 2, 3})
        assert "Invalid value `parameter`:" in str(excinfo.value)


class TestChoiceValidatorWithTuple:
    """Tests for ChoiceValidator with tuple-based allowed values."""

    def test_validate_with_valid_choice_in_tuple(self):
        """Test that valid choices in tuple pass validation."""
        ChoiceValidator.validate("jpg", ("jpg", "png", "gif"))
        ChoiceValidator.validate(1, (1, 2, 3))

    def test_validate_with_invalid_choice_in_tuple(self):
        """Test that invalid choices in tuple raise error."""
        with pytest.raises(InvalidChoiceError):
            ChoiceValidator.validate("bmp", ("jpg", "png", "gif"))


class TestChoiceValidatorWithCustomException:
    """Tests for ChoiceValidator with custom exception class."""

    def test_validate_with_custom_exception_class(self):
        """Test that custom exception class is used."""
        with pytest.raises(IntNotInAllowedSetError) as excinfo:
            ChoiceValidator.validate(
                4,
                {1, 2, 3},
                param_name="mode",
                cls_error=IntNotInAllowedSetError,
            )
        assert "Invalid value `mode`:" in str(excinfo.value)

    def test_validate_with_custom_error_still_includes_message(self):
        """Test that custom exception includes error message."""

        class CustomError(Exception):
            """Custom error for testing."""

        with pytest.raises(CustomError) as excinfo:
            ChoiceValidator.validate(
                "invalid",
                ["a", "b"],
                param_name="type",
                cls_error=CustomError,
            )
        assert "Invalid value `type`:" in str(excinfo.value)


class TestChoiceValidatorMixedTypes:
    """Tests for ChoiceValidator with mixed type choices."""

    def test_validate_with_mixed_int_and_string(self):
        """Test that validation works with mixed int and string choices."""
        ChoiceValidator.validate(1, [1, "one", 2, "two"])
        ChoiceValidator.validate("one", [1, "one", 2, "two"])

        with pytest.raises(InvalidChoiceError):
            ChoiceValidator.validate(3, [1, "one", 2, "two"])

    def test_validate_with_mixed_types_including_bool(self):
        """Test that validation works with bool values."""
        ChoiceValidator.validate(True, [True, False])
        ChoiceValidator.validate(False, [True, False])


class TestChoiceValidatorEdgeCases:
    """Tests for edge cases in ChoiceValidator."""

    def test_validate_with_empty_string(self):
        """Test that empty string can be validated."""
        ChoiceValidator.validate("", ["", "a", "b"])

        with pytest.raises(InvalidChoiceError):
            ChoiceValidator.validate("", ["a", "b", "c"])

    def test_validate_with_single_choice(self):
        """Test validation with single allowed choice."""
        ChoiceValidator.validate("only", ["only"])

        with pytest.raises(InvalidChoiceError):
            ChoiceValidator.validate("other", ["only"])

    def test_validate_with_large_choice_set(self):
        """Test validation with large set of choices."""
        large_set = set(range(0, 1000))
        ChoiceValidator.validate(500, large_set)
        ChoiceValidator.validate(0, large_set)
        ChoiceValidator.validate(999, large_set)

        with pytest.raises(InvalidChoiceError):
            ChoiceValidator.validate(1000, large_set)

    def test_validate_with_unicode_strings(self):
        """Test validation with unicode strings."""
        ChoiceValidator.validate("España", ["España", "México", "Chile"])
        ChoiceValidator.validate("日本", ["日本", "中国", "한국"])

        with pytest.raises(InvalidChoiceError):
            ChoiceValidator.validate("France", ["España", "México", "Chile"])

    def test_validate_error_message_formatting_with_complex_objects(self):
        """Test that error message handles complex object representations."""

        class CustomObject:
            """Custom object for testing."""

            def __str__(self):
                return "CustomObj"

        obj1 = CustomObject()
        obj2 = CustomObject()

        # Should not raise during error message formatting
        with pytest.raises(InvalidChoiceError) as excinfo:
            ChoiceValidator.validate("invalid", [obj1, obj2], param_name="object")
        assert "Invalid value `object`:" in str(excinfo.value)


class TestChoiceValidatorDefaultParamName:
    """Tests for default parameter name behavior."""

    def test_validate_default_param_name_in_error(self):
        """Test that default parameter name is used when not provided."""
        with pytest.raises(InvalidChoiceError) as excinfo:
            ChoiceValidator.validate("invalid", ["a", "b"])
        assert "Invalid value `parameter`:" in str(excinfo.value)

    def test_validate_with_explicit_parameter_name(self):
        """Test that explicit parameter name is used."""
        with pytest.raises(InvalidChoiceError) as excinfo:
            ChoiceValidator.validate("invalid", ["a", "b"], param_name="format")
        assert "Invalid value `format`:" in str(excinfo.value)
