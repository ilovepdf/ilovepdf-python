"""Unit tests for the ExtractTask class in the ilovepdf module."""

import pytest

from ilovepdf import ExtractTask


class TestExtractTask:
    """Unit tests for the ExtractTask class in the ilovepdf module."""

    @pytest.fixture
    def extract_task(self):
        """Fixture that creates an ExtractTask instance for testing."""
        task = ExtractTask("public_key", "secret_key", make_start=False)
        return task

    def test_initialization_sets_default_values(self, extract_task):
        """
        Ensure ExtractTask is initialized with default values.
        """
        assert extract_task.detailed is False
        assert extract_task.tool == "extract"

    def test_setters_assign_values_correctly(self, extract_task):
        """
        Ensure setters assign values correctly.
        """
        extract_task.detailed = True
        assert extract_task.detailed is True

        extract_task.detailed = False
        assert extract_task.detailed is False

    def test_to_dict_includes_all_params(self, extract_task):
        """
        Ensure _to_dict includes all parameters.
        """
        extract_task.detailed = True
        params = extract_task._to_dict()  # pylint: disable=protected-access
        assert params["detailed"] is True
