"""Unit tests for PdfToPdfATask using the ilovepdf PDF/A API."""

import pytest

from ilovepdf import PdfToPdfATask
from ilovepdf.exceptions import InvalidChoiceError
from ilovepdf.pdftopdfa_task import PDFA_CONFORMANCE_OPTIONS

from .base_test import AbstractUnitTaskTest


# pylint: disable=protected-access
class TestPdfToPdfATask(AbstractUnitTaskTest):
    """Unit tests for PdfToPdfATask covering defaults and validation."""

    _task_class = PdfToPdfATask
    _task_tool = "pdfa"

    def test_initialization_sets_default_values(self, my_task):
        """Ensures PdfToPdfATask starts with expected defaults."""
        assert my_task._DEFAULT_PAYLOAD == {
            "conformance": "pdfa-2b",
            "allow_downgrade": True,
        }
        assert PDFA_CONFORMANCE_OPTIONS == {
            "pdfa-1b",
            "pdfa-1a",
            "pdfa-2b",
            "pdfa-2u",
            "pdfa-2a",
            "pdfa-3b",
            "pdfa-3u",
            "pdfa-3a",
        }
        assert my_task.conformance == "pdfa-2b"
        assert my_task.allow_downgrade is True

    def test_setters_assign_values_correctly(self, my_task):
        """Confirms setters update and persist supported values."""
        for conformance in PDFA_CONFORMANCE_OPTIONS:
            my_task.conformance = conformance
            assert my_task.conformance == conformance

        my_task.allow_downgrade = False
        assert my_task.allow_downgrade is False

    def test_invalid_conformance_raises(self, my_task):
        """Validates unsupported conformance values raise InvalidChoiceError."""
        with pytest.raises(InvalidChoiceError):
            my_task.conformance = "invalid-conformance"

    def test_invalid_allow_downgrade_raises(self, my_task):
        """Validates unsupported allow_downgrade values raise ValueError."""
        with pytest.raises(InvalidChoiceError):
            my_task.allow_downgrade = "invalid-allow-downgrade"

    def test_to_payload_includes_all_params(self, my_task):
        """Ensures the serialized payload contains updated parameters."""
        my_task.conformance = "pdfa-3a"
        my_task.allow_downgrade = False
        params = my_task._to_payload()
        assert params["conformance"] == "pdfa-3a"
        assert params["allow_downgrade"] is False
