"""Unit tests for IntValidator.

Covers all validation methods of IntValidator, including edge cases and error
handling.
"""

import pytest

from ilovepdf.exceptions import (
    IntNotInAllowedSetError,
    IntOutOfRangeError,
    NotAnIntError,
)
from ilovepdf.validators import IntValidator

# pylint: disable=protected-access


class TestIntValidatorType:
    """Tests for IntValidator.validate_type()."""

    def test_validate_type_with_valid_int(self):
        """Test that valid integers pass validation."""
        IntValidator.validate_type(0)
        IntValidator.validate_type(1)
        IntValidator.validate_type(-1)
        IntValidator.validate_type(999999)

    def test_validate_type_with_bool_raises_error(self):
        """Test that boolean values raise NotAnIntError."""
        with pytest.raises(NotAnIntError) as excinfo:
            IntValidator.validate_type(True)
        assert "Invalid parameter: value must be an integer." in str(excinfo.value)

    def test_validate_type_with_string_raises_error(self):
        """Test that string values raise NotAnIntError."""
        with pytest.raises(NotAnIntError) as excinfo:
            IntValidator.validate_type("5")
        assert "Invalid parameter: value must be an integer." in str(excinfo.value)

    def test_validate_type_with_float_raises_error(self):
        """Test that float values raise NotAnIntError."""
        with pytest.raises(NotAnIntError) as excinfo:
            IntValidator.validate_type(5.0)
        assert "Invalid parameter: value must be an integer." in str(excinfo.value)

    def test_validate_type_with_none_raises_error(self):
        """Test that None raises NotAnIntError."""
        with pytest.raises(NotAnIntError) as excinfo:
            IntValidator.validate_type(None)
        assert "Invalid parameter: value must be an integer." in str(excinfo.value)

    def test_validate_type_custom_param_name(self):
        """Test that custom parameter name appears in error message."""
        with pytest.raises(NotAnIntError) as excinfo:
            IntValidator.validate_type("invalid", param_name="width")
        assert "Invalid width: value must be an integer." in str(excinfo.value)


class TestIntValidatorPositive:
    """Tests for IntValidator.validate_positive()."""

    def test_validate_positive_with_valid_positive_int(self):
        """Test that positive integers pass validation."""
        IntValidator.validate_positive(1)
        IntValidator.validate_positive(100)
        IntValidator.validate_positive(999999)

    def test_validate_positive_with_zero_raises_error(self):
        """Test that zero raises IntOutOfRangeError."""
        with pytest.raises(IntOutOfRangeError) as excinfo:
            IntValidator.validate_positive(0)
        assert "Invalid parameter: value must be a positive integer" in str(
            excinfo.value
        )

    def test_validate_positive_with_negative_raises_error(self):
        """Test that negative integers raise IntOutOfRangeError."""
        with pytest.raises(IntOutOfRangeError) as excinfo:
            IntValidator.validate_positive(-1)
        assert "Invalid parameter: value must be a positive integer" in str(
            excinfo.value
        )

    def test_validate_positive_with_non_int_raises_error(self):
        """Test that non-integers raise NotAnIntError."""
        with pytest.raises(NotAnIntError) as excinfo:
            IntValidator.validate_positive("5", param_name="width")
        assert "Invalid width: value must be an integer." in str(excinfo.value)

    def test_validate_positive_custom_param_name(self):
        """Test that custom parameter name appears in error message."""
        with pytest.raises(IntOutOfRangeError) as excinfo:
            IntValidator.validate_positive(0, param_name="height")
        assert "Invalid height: value must be a positive integer" in str(excinfo.value)


class TestIntValidatorRange:
    """Tests for IntValidator.validate_range()."""

    def test_validate_range_with_value_in_range(self):
        """Test that values within range pass validation."""
        IntValidator.validate_range(5, 1, 10)
        IntValidator.validate_range(1, 1, 10)  # at minimum
        IntValidator.validate_range(10, 1, 10)  # at maximum
        IntValidator.validate_range(0, -10, 10)  # negative range

    def test_validate_range_with_value_below_minimum(self):
        """Test that values below minimum raise IntOutOfRangeError."""
        with pytest.raises(IntOutOfRangeError) as excinfo:
            IntValidator.validate_range(0, 1, 10)
        assert "parameter must be between 1 and 10." in str(excinfo.value)

    def test_validate_range_with_value_above_maximum(self):
        """Test that values above maximum raise IntOutOfRangeError."""
        with pytest.raises(IntOutOfRangeError) as excinfo:
            IntValidator.validate_range(11, 1, 10)
        assert "parameter must be between 1 and 10." in str(excinfo.value)

    def test_validate_range_with_non_int_raises_error(self):
        """Test that non-integers raise NotAnIntError."""
        with pytest.raises(NotAnIntError) as excinfo:
            IntValidator.validate_range("5", 1, 10, param_name="quality")
        assert "Invalid quality: value must be an integer." in str(excinfo.value)

    def test_validate_range_custom_param_name(self):
        """Test that custom parameter name appears in error message."""
        with pytest.raises(IntOutOfRangeError) as excinfo:
            IntValidator.validate_range(15, 1, 10, param_name="quality")
        assert "quality must be between 1 and 10." in str(excinfo.value)

    def test_validate_range_negative_values(self):
        """Test that negative ranges work correctly."""
        IntValidator.validate_range(-5, -10, 0)
        IntValidator.validate_range(-10, -10, -5)

    def test_validate_range_large_values(self):
        """Test that large ranges work correctly."""
        IntValidator.validate_range(50000, 1, 100000)


class TestIntValidatorOptions:
    """Tests for IntValidator.validate_options()."""

    def test_validate_options_with_valid_option(self):
        """Test that values in options set pass validation."""
        IntValidator.validate_options(1, {1, 2, 3})
        IntValidator.validate_options(2, {1, 2, 3})
        IntValidator.validate_options(3, {1, 2, 3})

    def test_validate_options_with_invalid_option(self):
        """Test that values not in options raise IntNotInAllowedSetError."""
        with pytest.raises(IntNotInAllowedSetError) as excinfo:
            IntValidator.validate_options(4, {1, 2, 3})
        assert "Invalid value `parameter`: value must be one of 1, 2, 3." in str(
            excinfo.value
        )

    def test_validate_options_with_non_int_raises_error(self):
        """Test that non-integers raise NotAnIntError."""
        with pytest.raises(NotAnIntError) as excinfo:
            IntValidator.validate_options("1", {1, 2, 3}, param_name="mode")
        assert "Invalid mode: value must be an integer." in str(excinfo.value)

    def test_validate_options_custom_param_name(self):
        """Test that custom parameter name appears in error message."""
        with pytest.raises(IntNotInAllowedSetError) as excinfo:
            IntValidator.validate_options(0, {1, 2, 3}, param_name="rotation")
        assert "Invalid value `rotation`: value must be one of 1, 2, 3." in str(
            excinfo.value
        )

    def test_validate_options_single_option(self):
        """Test validation with single option."""
        IntValidator.validate_options(5, {5})

    def test_validate_options_large_set(self):
        """Test validation with large option set."""
        options = set(range(0, 360, 15))  # 0, 15, 30, ..., 345
        IntValidator.validate_options(90, options)
        IntValidator.validate_options(0, options)
        IntValidator.validate_options(345, options)

    def test_validate_options_with_zero(self):
        """Test that zero in options is handled correctly."""
        IntValidator.validate_options(0, {0, 1, 2})

    def test_validate_options_with_negative(self):
        """Test that negative values in options are handled correctly."""
        IntValidator.validate_options(-1, {-1, 0, 1})
