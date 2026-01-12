"""Unit tests for the PdfOcrTask class in the ilovepdf module."""

from unittest.mock import patch

import pytest

from ilovepdf import PdfOcrTask
from ilovepdf.pdfocr_task import OcrFile


class TestPdfOcrTask:
    """Unit tests for the PdfOcrTask class in the ilovepdf module."""

    @pytest.fixture
    def ocr_task(self):
        """Fixture that creates a PdfOcrTask instance for testing."""
        task = PdfOcrTask("public_key", "secret_key", make_start=False)
        task.task = "dummy_task_id"
        return task

    def test_initialization_sets_default_values(self, ocr_task):
        """Ensure PdfOcrTask is initialized with default values."""
        assert ocr_task.tool == "pdfocr", "Tool should be 'pdfocr'"

    def test_add_file_returns_ocrfile(self, ocr_task, tmp_path):
        pdf_path = tmp_path / "sample.pdf"
        pdf_path.write_bytes(b"%PDF-1.4\n%EOF\n")
        with patch.object(
            ocr_task, "upload_file", return_value=OcrFile("server.pdf", "sample.pdf")
        ):
            file = ocr_task.add_file(str(pdf_path))
            assert isinstance(file, OcrFile)
            assert file.ocr_languages == "eng"

    def test_set_languages_accepts_valid_codes(self, ocr_task, tmp_path):
        pdf_path = tmp_path / "sample.pdf"
        pdf_path.write_bytes(b"%PDF-1.4\n%EOF\n")
        with patch.object(
            ocr_task, "upload_file", return_value=OcrFile("server.pdf", "sample.pdf")
        ):
            file = ocr_task.add_file(str(pdf_path))
            file.set_languages(["eng", "spa"])
            assert file.get_languages() == "eng,spa"
            file.set_languages("fra")
            assert file.get_languages() == "fra"

    def test_set_languages_rejects_invalid_codes(self, ocr_task, tmp_path):
        pdf_path = tmp_path / "sample.pdf"
        pdf_path.write_bytes(b"%PDF-1.4\n%EOF\n")
        with patch.object(
            ocr_task, "upload_file", return_value=OcrFile("server.pdf", "sample.pdf")
        ):
            file = ocr_task.add_file(str(pdf_path))
            with pytest.raises(ValueError, match="Invalid language code"):
                file.set_languages(["eng", "xxx"])

    def test_set_languages_empty(self, ocr_task, tmp_path):
        pdf_path = tmp_path / "sample.pdf"
        pdf_path.write_bytes(b"%PDF-1.4\n%EOF\n")
        with patch.object(
            ocr_task, "upload_file", return_value=OcrFile("server.pdf", "sample.pdf")
        ):
            file = ocr_task.add_file(str(pdf_path))
            with pytest.raises(ValueError, match="Languages cannot be empty"):
                file.set_languages([])

    def test_get_file_options_includes_ocr_languages(self, ocr_task, tmp_path):
        pdf_path = tmp_path / "sample.pdf"
        pdf_path.write_bytes(b"%PDF-1.4\n%EOF\n")
        with patch.object(
            ocr_task, "upload_file", return_value=OcrFile("server.pdf", "sample.pdf")
        ):
            file = ocr_task.add_file(str(pdf_path))
            file.set_languages("spa")
            options = file.get_file_options()
            assert "ocr_languages" in options
            assert options["ocr_languages"] == "spa"

    def test_set_languages_string_and_list_equivalence(self, ocr_task, tmp_path):
        pdf_path = tmp_path / "sample.pdf"
        pdf_path.write_bytes(b"%PDF-1.4\n%EOF\n")
        with patch.object(
            ocr_task, "upload_file", return_value=OcrFile("server.pdf", "sample.pdf")
        ):
            file = ocr_task.add_file(str(pdf_path))
            file.set_languages(["eng", "spa"])
            langs_list = file.get_languages()
            file.set_languages("eng,spa")
            langs_str = file.get_languages()
            assert langs_list == langs_str
