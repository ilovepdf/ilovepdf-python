"""Unit tests for the BoolValidator class in the ilovepdf.validators module.

These tests verify correct behavior and parameter validation for boolean values
using BoolValidator.
"""

import pytest

from ilovepdf.exceptions import InvalidChoiceError
from ilovepdf.validators.bool_validator import BoolValidator


# pylint: disable=protected-access
class TestBoolValidator:
    """
    Unit tests for BoolValidator.

    Covers validation of boolean values and rejection of invalid types.
    """

    def test_validate_true(self):
        """Should pass for True."""
        BoolValidator.validate(True)

    def test_validate_false(self):
        """Should pass for False."""
        BoolValidator.validate(False)

    @pytest.mark.parametrize(
        "value", ["true", "false", 1, 0, None, "yes", "no", [], {}, 3.14]
    )
    def test_validate_invalid(self, value):
        """
        Should raise InvalidChoiceError for non-bool values.
        """
        with pytest.raises(InvalidChoiceError):
            BoolValidator.validate(value, param_name="test_param")
