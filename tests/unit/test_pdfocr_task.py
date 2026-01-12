"""Unit tests for the PdfOcrTask class in the ilovepdf module.

These tests verify correct behavior for OCR language configuration and
task instantiation for PDF OCR processing.
"""

import pytest

from ilovepdf import PdfOcrTask
from ilovepdf.exceptions import InvalidChoiceError
from ilovepdf.pdfocr_task import OcrFile

from .base_test import AbstractUnitFileTest, AbstractUnitTaskTest


# pylint: disable=protected-access
class TestOcrFile(AbstractUnitFileTest):
    """Unit tests for OcrFile language configuration behavior."""

    _task_class = OcrFile

    def test_initialization_sets_default_values(self, my_task):
        """Checks default OCR language is set to 'eng'."""
        assert my_task._DEFAULT_PAYLOAD == {
            "server_filename": None,
            "filename": None,
            "ocr_languages": "eng",
        }
        assert my_task.ocr_languages == "eng"

    def test_set_languages_accepts_valid_codes(self, my_task):
        """Ensures the OCR language setter handles valid string and list values."""
        my_task.ocr_languages = ["eng"]
        assert my_task.ocr_languages == "eng"

        my_task.ocr_languages = ["eng", "spa"]
        assert my_task.ocr_languages == "eng,spa"

        my_task.ocr_languages = "eng,spa"
        assert my_task.ocr_languages == "eng,spa"

        my_task.ocr_languages = "fra"
        assert my_task.ocr_languages == "fra"

    def test_set_languages_rejects_invalid_codes(self, my_task):
        """Validates that unsupported language codes raise InvalidChoiceError."""
        with pytest.raises(InvalidChoiceError):
            my_task.ocr_languages = "morse"

        with pytest.raises(InvalidChoiceError):
            my_task.ocr_languages = "morse,eng"

        with pytest.raises(InvalidChoiceError):
            my_task.ocr_languages = ["morse"]

        with pytest.raises(InvalidChoiceError):
            my_task.ocr_languages = ["eng", "morse"]


class TestPdfOcrTask(AbstractUnitTaskTest):
    """Unit tests for PdfOcrTask interactions with OCR-specific files."""

    _task_class = PdfOcrTask
    _task_tool = "pdfocr"

    def test_dummy(self):
        """Dummy test to ensure the PdfOcrTask class is defined."""
