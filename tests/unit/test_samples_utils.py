"""Unit tests for sample objects defined in samples_utils.py.

These tests ensure that all reusable samples are valid and compatible with
the current constructors and expected behaviors.
"""

import pytest

from tests.unit.samples_utils import sample_classes


# pylint: disable=protected-access
@pytest.mark.parametrize("sample_class", sample_classes)
def test_sample_classes_are_valid(sample_class):
    """Test that all sample classes can be converted to payloads."""
    for sample_object in sample_class.all_samples:
        payload = sample_object._to_payload()
        assert isinstance(payload, dict)
