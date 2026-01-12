"""Unit tests for the PdfToPdfATask class in ilovepdf.pdftopdfa_task."""

import pytest

from ilovepdf import PdfToPdfATask


class TestPdfToPdfATask:
    """Unit tests for the PdfToPdfATask class in ilovepdf.pdftopdfa_task."""

    @pytest.fixture
    def pdfa_task(self):
        """Fixture that creates a PdfToPdfATask instance for testing."""
        task = PdfToPdfATask("public_key", "secret_key", make_start=False)
        return task

    def test_initialization_sets_default_values(self, pdfa_task):
        """
        Ensure PdfToPdfATask is initialized with default values.
        """
        assert pdfa_task.conformance == "pdfa-2b"
        assert pdfa_task.allow_downgrade is True
        assert pdfa_task.tool == "pdfa"

    def test_setters_assign_values_correctly(self, pdfa_task):
        """
        Ensure setters assign values correctly and validation works.
        """
        pdfa_task.conformance = "pdfa-1b"
        assert pdfa_task.conformance == "pdfa-1b"

        pdfa_task.allow_downgrade = False
        assert pdfa_task.allow_downgrade is False

    def test_invalid_conformance_raises(self, pdfa_task):
        """
        Ensure invalid conformance values raise ValueError.
        """
        with pytest.raises(ValueError):
            pdfa_task.conformance = "invalid-conformance"

    def test_to_dict_includes_all_params(self, pdfa_task):
        """
        Ensure _to_dict includes all parameters.
        """
        pdfa_task.conformance = "pdfa-3a"
        pdfa_task.allow_downgrade = False
        params = pdfa_task._to_dict()  # pylint: disable=protected-access
        assert params["conformance"] == "pdfa-3a"
        assert params["allow_downgrade"] is False
