"""Unit tests for ValidatePdfATask using the ilovepdf PDF/A validation API.

These tests verify property defaults, setters, validation, and result extraction.
"""

import pytest

from ilovepdf.exceptions import InvalidChoiceError
from ilovepdf.validate_pdfa_task import (
    PDFA_CONFORMANCE_OPTIONS,
    ValidatePdfATask,
)

from .base_test import AbstractUnitTaskTest


class TestValidatePdfATask(AbstractUnitTaskTest):
    """
    Unit tests for ValidatePdfATask.

    Covers initialization, valid and invalid property settings, parameter validation,
    and result extraction.
    """

    _task_class = ValidatePdfATask
    _task_tool = "validatepdfa"

    def test_initialization_sets_default_values(self, my_task):
        """Ensures ValidatePdfATask starts with expected defaults."""
        assert my_task._DEFAULT_PAYLOAD == {
            "conformance": "pdfa-2b",
            "allow_downgrade": True,
        }
        assert my_task.conformance == "pdfa-2b"
        assert my_task.allow_downgrade is True
        assert my_task.validation_result is None

    def test_setters_assign_values_correctly(self, my_task):
        """Confirms setters update and persist supported values."""
        for conformance in PDFA_CONFORMANCE_OPTIONS:
            my_task.conformance = conformance
            assert my_task.conformance == conformance

        my_task.allow_downgrade = False
        assert my_task.allow_downgrade is False
        my_task.allow_downgrade = True
        assert my_task.allow_downgrade is True

    def test_invalid_conformance_raises(self, my_task):
        """Validates unsupported conformance values raise InvalidChoiceError."""
        with pytest.raises(InvalidChoiceError):
            my_task.conformance = "invalid-conformance"

    def test_invalid_allow_downgrade_raises(self, my_task):
        """Validates non-boolean allow_downgrade values raise TypeError."""
        with pytest.raises(InvalidChoiceError):
            my_task.allow_downgrade = "not-a-bool"

    def test_validation_result_extraction_conformant(self, my_task):
        """Validates extraction of a conformant PDF/A result from a typical
        API response."""
        my_task.result = {
            "download_filename": "document.pdf",
            "filesize": 0,
            "output_extensions": '["pdf"]',
            "output_filenumber": 1,
            "output_filesize": 0,
            "status": "TaskSuccess",
            "timer": "0.100",
            "validations": [
                {
                    "server_filename": "abc123.pdf",
                    "status": "Conformant",
                }
            ],
        }
        my_task._extract_validation_result()
        result = my_task.validation_result
        assert result is not None
        assert result["status"] == "Conformant"
        assert result["server_filename"] == "abc123.pdf"

    def test_validation_result_extraction_non_conformant(self, my_task):
        """Validates extraction when the file is not PDF/A compliant."""
        my_task.result = {
            "download_filename": "document.pdf",
            "filesize": 0,
            "output_extensions": '["pdf"]',
            "output_filenumber": 1,
            "output_filesize": 0,
            "status": "TaskSuccess",
            "timer": "0.144",
            "validations": [
                {
                    "server_filename": "def456.pdf",
                    "status": "NonConformant",
                    "reason": [
                        "0, 3, 0x8341052B, The required XMP property "
                        "'pdfaid:part' is missing., 1",
                        "10, 0, 0x83410612, The document does not conform "
                        "to the requested standard., 1",
                    ],
                }
            ],
        }
        my_task._extract_validation_result()
        result = my_task.validation_result
        assert result is not None
        assert result["status"] == "NonConformant"
        assert isinstance(result["reason"], list)
        assert len(result["reason"]) == 2

    def test_validation_result_extraction_empty_validations(self, my_task):
        """Handles case where API response has empty validations list."""
        my_task.result = {
            "status": "TaskSuccess",
            "validations": [],
        }
        my_task._extract_validation_result()
        assert my_task.validation_result is None

    def test_validation_result_extraction_missing_validations_key(self, my_task):
        """Handles case where API response has no validations key."""
        my_task.result = {
            "status": "TaskSuccess",
        }
        my_task._extract_validation_result()
        assert my_task.validation_result is None

    def test_validation_result_extraction_no_result(self, my_task):
        """Handles case where no result is set."""
        my_task.result = None
        my_task._extract_validation_result()
        assert my_task.validation_result is None

    def test_validation_result_extraction_multiple_files(self, my_task):
        """Validates that only the first validation entry is extracted."""
        my_task.result = {
            "status": "TaskSuccess",
            "validations": [
                {
                    "server_filename": "first.pdf",
                    "status": "Conformant",
                },
                {
                    "server_filename": "second.pdf",
                    "status": "NonConformant",
                    "reason": ["Some reason"],
                },
            ],
        }
        my_task._extract_validation_result()
        result = my_task.validation_result
        assert result is not None
        assert result["server_filename"] == "first.pdf"
        assert result["status"] == "Conformant"
