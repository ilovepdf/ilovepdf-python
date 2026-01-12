"""Unit tests for the CompressTask class in the ilovepdf module.

These tests verify the correct behavior and parameter validation for image compression
tasks using CompressTask.
"""

import pytest

from ilovepdf import CompressTask
from ilovepdf.compress_task import COMPRESSION_LEVEL_OPTIONS
from ilovepdf.exceptions import InvalidChoiceError

from .base_test import AbstractUnitTaskTest


# pylint: disable=protected-access
class TestCompressTask(AbstractUnitTaskTest):
    """
    Unit tests for CompressTask.

    Covers initialization, valid and invalid compression level settings,
    and parameter validation.
    """

    _task_class = CompressTask
    _task_tool = "compress"

    def test_initialization(self, my_task):
        """
        Test that CompressTask is initialized correctly.

        Verifies that the default compression level is "recommended".
        """
        assert COMPRESSION_LEVEL_OPTIONS == {"low", "recommended", "extreme"}
        assert my_task.compression_level == "recommended"

    def test_set_compression_level_valid(self, my_task):
        """
        Test setting a valid compression level.

        Verifies that the compression level can be set to "low", "recommended", or
        "extreme".
        """
        for level in COMPRESSION_LEVEL_OPTIONS:
            my_task.compression_level = level
            assert my_task.compression_level == level

    def test_set_compression_level_invalid(self, my_task):
        """
        Test setting an invalid compression level.

        Verifies that setting an invalid compression level raises an exception.
        """

        with pytest.raises(InvalidChoiceError) as excinfo:
            my_task.compression_level = "invalid_level"
        assert "compression_level" in str(excinfo.value)
