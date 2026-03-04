"""Unit tests for the PdfToJpgTask class in the ilovepdf module.

These tests verify correct behavior and parameter validation for PDF to JPG
conversion tasks using PdfToJpgTask.
"""

import pytest

from ilovepdf import PdfToJpgTask
from ilovepdf.exceptions import InvalidChoiceError
from tests.unit.base_test import AbstractUnitTaskTest


class TestPdfToJpgTask(AbstractUnitTaskTest):
    """
    Unit tests for PdfToJpgTask.

    Covers initialization, valid and invalid pdfjpg_mode settings,
    and parameter validation.
    """

    _task_class = PdfToJpgTask
    _task_tool = "pdfjpg"

    def test_initialization_sets_default_values(self, my_task):
        """
        Validates that PdfToJpgTask is initialized with expected default values.

        Args:
            my_task (PdfToJpgTask): The task instance under test.

        Asserts:
            - The extension list is ['pdf'].
            - The default payload contains pdfjpg_mode set to 'pages'.
        """
        assert my_task.get_extension_list() == ["pdf"]
        assert my_task._DEFAULT_PAYLOAD == {
            "pdfjpg_mode": "pages",
        }

    @pytest.mark.parametrize(
        "mode",
        [
            "pages",
            "extract",
        ],
    )
    def test_pdfjpg_mode_setter_accepts_valid_values(self, my_task, mode):
        """
        Validates that pdfjpg_mode setter accepts valid values and updates payload.

        Args:
            my_task (PdfToJpgTask): The task instance under test.
            mode (str): The valid mode to set.

        Asserts:
            - pdfjpg_mode property matches the set value.
            - The payload reflects the updated mode.
        """
        my_task.pdfjpg_mode = mode
        assert my_task.pdfjpg_mode == mode
        assert my_task._payload["pdfjpg_mode"] == mode

    @pytest.mark.parametrize(
        "invalid_mode",
        [
            "invalid",
            "",
            None,
            123,
            "PAGEs",
        ],
    )
    def test_pdfjpg_mode_setter_rejects_invalid_values(self, my_task, invalid_mode):
        """
        Validates that pdfjpg_mode setter raises InvalidChoiceError for invalid values.

        Args:
            my_task (PdfToJpgTask): The task instance under test.
            invalid_mode: The invalid mode to test.

        Asserts:
            - Setting an invalid mode raises InvalidChoiceError.
        """
        with pytest.raises(InvalidChoiceError):
            my_task.pdfjpg_mode = invalid_mode
