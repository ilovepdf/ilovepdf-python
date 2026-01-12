"""Unit tests for the UploadFiles class in the ilovepdf module."""

from unittest.mock import MagicMock, patch

import pytest

from ilovepdf.exceptions.upload_exception import UploadException
from ilovepdf.file import File
from ilovepdf.task import Task


# Task = ProcessTask
class TestUploadPDF:
    """Unit tests for the UploadPDF class in the ilovepdf module."""

    @patch.object(Task, "send_request")
    def test_start_creates_task_and_sets_ids(self, mock_send_request):
        # Simulate API response when starting a task
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "server": "worker.ilovepdf.com",
            "task": "task_123",
            "remaining_files": 10,
            "remaining_pages": 100,
            "remaining_credits": 50,
        }
        mock_send_request.return_value = mock_response

        task = Task(public_key="public", secret_key="secret")
        task.tool = "compress"
        task.start()
        assert task.get_task_id() == "task_123"
        assert task.get_worker_server() == "https://worker.ilovepdf.com"
        assert task.remaining_files == 10
        assert task.remaining_pages == 100
        assert task.remaining_credits == 50

    @patch.object(Task, "send_request")
    def test_add_file_success(self, mock_send_request, tmp_path):
        # Create a temporary PDF file
        pdf_file = tmp_path / "test.pdf"
        pdf_file.write_bytes(b"%PDF-1.4 test content")

        # Simulate API response when uploading the file
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "server_filename": "file_abc123",
            "pdf_pages": ["100x200", "200x300"],
            "pdf_page_number": 2,
        }
        mock_send_request.return_value = mock_response

        task = Task(public_key="public", secret_key="secret")
        task.task = "task_123"  # Simulate already started task

        uploaded_file = task.add_file(str(pdf_file))
        assert isinstance(uploaded_file, File)
        assert uploaded_file.server_filename == "file_abc123"
        assert uploaded_file.pdf_pages == ["100x200", "200x300"]
        assert uploaded_file.pdf_page_number == 2

    @patch.object(Task, "send_request")
    def test_add_file_nonexistent_path_raises(self, _mock_send_request):
        task = Task(public_key="public", secret_key="secret")
        task.task = "task_123"
        with pytest.raises(ValueError):
            task.add_file("nonexistent.pdf")

    @patch.object(Task, "send_request")
    def test_upload_file_api_error_raises(self, mock_send_request, tmp_path):
        pdf_file = tmp_path / "test.pdf"
        pdf_file.write_bytes(b"%PDF-1.4 test content")

        # Simulate API error response when uploading the file
        mock_response = MagicMock()
        mock_response.json.side_effect = Exception("Upload response error")
        mock_send_request.return_value = mock_response

        task = Task(public_key="public", secret_key="secret")
        task.task = "task_123"
        with pytest.raises(UploadException):
            task.add_file(str(pdf_file))

    @patch.object(Task, "send_request")
    def test_add_file_large_file(self, mock_send_request, tmp_path):
        # Simulate a large file (10MB, should be accepted)
        large_pdf = tmp_path / "large.pdf"
        large_pdf.write_bytes(b"%PDF-1.4" + b"A" * (10 * 1024 * 1024))  # 10MB

        mock_response = MagicMock()
        mock_response.json.return_value = {
            "server_filename": "file_large",
            "pdf_pages": ["100x200"],
            "pdf_page_number": 1,
        }
        mock_send_request.return_value = mock_response

        task = Task(public_key="public", secret_key="secret")
        task.task = "task_123"
        uploaded_file = task.add_file(str(large_pdf))
        assert isinstance(uploaded_file, File)
        assert uploaded_file.server_filename == "file_large"

    def test_add_file_too_large_raises(self, tmp_path):
        # Simulate a too large file (200MB, should be rejected)
        huge_pdf = tmp_path / "huge.pdf"
        huge_pdf.write_bytes(b"%PDF-1.4" + b"A" * (200 * 1024 * 1024))  # 200MB
        task = Task(public_key="public", secret_key="secret")
        task.task = "task_123"
        with pytest.raises(ValueError, match="exceeds the maximum allowed size"):
            task.add_file(str(huge_pdf))

    @patch.object(Task, "send_request")
    def test_add_multiple_files(self, mock_send_request, tmp_path):
        # Create two temporary PDF files
        pdf1 = tmp_path / "file1.pdf"
        pdf2 = tmp_path / "file2.pdf"
        pdf1.write_bytes(b"%PDF-1.4 file1")
        pdf2.write_bytes(b"%PDF-1.4 file2")

        # Simulate different API responses for each file
        def side_effect(*args):
            response = MagicMock()
            if "file1.pdf" in args[2]["files"]["file"].name:
                response.json.return_value = {
                    "server_filename": "file1_id",
                    "pdf_pages": ["100x200"],
                    "pdf_page_number": 1,
                }
            else:
                response.json.return_value = {
                    "server_filename": "file2_id",
                    "pdf_pages": ["200x300"],
                    "pdf_page_number": 2,
                }
            return response

        mock_send_request.side_effect = side_effect

        task = Task(public_key="public", secret_key="secret")
        task.task = "task_123"
        file_obj1 = task.add_file(str(pdf1))
        file_obj2 = task.add_file(str(pdf2))
        assert file_obj1.server_filename == "file1_id"
        assert file_obj2.server_filename == "file2_id"
        assert len(task.files) == 2

    @patch.object(Task, "send_request")
    def test_add_file_returns_file_id_for_operations(self, mock_send_request, tmp_path):
        # Create a temporary PDF file
        pdf_file = tmp_path / "test.pdf"
        pdf_file.write_bytes(b"%PDF-1.4 test content")

        mock_response = MagicMock()
        mock_response.json.return_value = {
            "server_filename": "file_abc123",
            "pdf_pages": ["100x200"],
            "pdf_page_number": 1,
        }
        mock_send_request.return_value = mock_response

        task = Task(public_key="public", secret_key="secret")
        task.task = "task_123"
        uploaded_file = task.add_file(str(pdf_file))
        # Check that the identifier is available for further operations
        assert hasattr(uploaded_file, "server_filename")
        assert uploaded_file.server_filename == "file_abc123"
