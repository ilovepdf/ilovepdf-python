"""Unit tests for the File class in the ilovepdf module."""

import unittest
from unittest.mock import Mock

from ilovepdf import File


class TestFile(unittest.TestCase):
    """Unit tests for the File class in the ilovepdf module."""

    def setUp(self):
        self.file = File("server_filename", "filename")

    def test_initialization(self):
        self.assertEqual(self.file.server_filename, "server_filename")
        self.assertEqual(self.file.filename, "filename")

        with self.assertRaises(ValueError):
            File("", "filename")
        with self.assertRaises(ValueError):
            File("server_filename", "")

    def test_set_rotation(self):
        self.file.set_rotation(90)
        self.assertEqual(self.file.rotate, 90)

        with self.assertRaises(ValueError):
            self.file.set_rotation(45)

    def test_set_password(self):
        self.file.set_password("password")
        self.assertEqual(self.file.password, "password")

    def test_get_file_options(self):
        options = self.file.get_file_options()
        self.assertEqual(options["server_filename"], "server_filename")
        self.assertEqual(options["filename"], "filename")

    def test_get_sanitized_pdf_pages(self):
        self.file.pdf_pages = ["100x200", "300x400"]
        sanitized = self.file.get_sanitized_pdf_pages()
        self.assertEqual(
            sanitized,
            [{"width": "100", "height": "200"}, {"width": "300", "height": "400"}],
        )

    def test_each_pdf_form_element(self):
        self.file.pdf_forms = [
            {"page": 1, "type": "text", "value": "test"},
            {"page": 2, "type": "signature"},
        ]
        self.file.pdf_pages = ["100x200", "300x400"]

        mock_callback = Mock()
        self.file.each_pdf_form_element(mock_callback)

        self.assertEqual(mock_callback.call_count, 2)
        mock_callback.assert_any_call(
            self.file.pdf_forms[0], {"width": "100", "height": "200"}
        )
        mock_callback.assert_any_call(
            self.file.pdf_forms[1], {"width": "300", "height": "400"}
        )


if __name__ == "__main__":
    unittest.main()
