"""Unit tests for the ErrorRouter class in the ilovepdf module.

These tests verify correct error routing and exception raising for various
HTTP status codes and API endpoints.
"""

import pytest

from ilovepdf.exceptions import (
    DownloadException,
    ProcessException,
    SignatureException,
    StartException,
    TaskException,
    UploadException,
)
from ilovepdf.ilovepdf_api import ErrorRouter

# pylint: disable=protected-access


class TestErrorRouterUploadErrors:
    """Unit tests for upload error handling in ErrorRouter."""

    def test_handle_upload_response_with_dict_body(self):
        """Test upload error handling with dictionary response body."""
        router = ErrorRouter()
        response_body = {
            "error": {
                "type": "upload_error",
                "message": "File too large",
            }
        }
        with pytest.raises(UploadException) as excinfo:
            router._handle_upload_response(response_body, 400)
        assert "File too large" in str(excinfo.value)

    def test_handle_upload_response_with_string_body(self):
        """Test upload error handling with string response body."""
        router = ErrorRouter()
        response_body = "Upload failed"
        with pytest.raises(UploadException) as excinfo:
            router._handle_upload_response(response_body, 400)
        assert "Upload error" in str(excinfo.value)

    def test_handle_upload_response_without_message(self):
        """Test upload error handling when message is missing."""
        router = ErrorRouter()
        response_body = {"error": {}}
        with pytest.raises(UploadException) as excinfo:
            router._handle_upload_response(response_body, 400)
        assert "Upload error" in str(excinfo.value)

    def test_upload_error_includes_response_code(self):
        """Test that upload exception includes HTTP status code."""
        router = ErrorRouter()
        response_body = {"error": {"message": "Unauthorized"}}
        with pytest.raises(UploadException) as excinfo:
            router._handle_upload_response(response_body, 401)
        assert excinfo.value.response_body == response_body


class TestErrorRouterProcessErrors:
    """Unit tests for process error handling in ErrorRouter."""

    def test_handle_process_response_with_message(self):
        """Test process error handling with error message."""
        router = ErrorRouter()
        response_body = {
            "error": {
                "type": "process_error",
                "message": "Processing failed",
            }
        }
        with pytest.raises(ProcessException) as excinfo:
            router._handle_process_response(response_body, 400)
        assert "Processing failed" in str(excinfo.value)

    def test_handle_process_response_without_message(self):
        """Test process error handling when message is missing."""
        router = ErrorRouter()
        response_body = {"error": {}}
        with pytest.raises(ProcessException) as excinfo:
            router._handle_process_response(response_body, 400)
        assert "Process error" in str(excinfo.value)

    def test_process_error_includes_response_code(self):
        """Test that process exception includes HTTP status code."""
        router = ErrorRouter()
        response_body = {"error": {"message": "Server error"}}
        with pytest.raises(ProcessException) as excinfo:
            router._handle_process_response(response_body, 500)
        assert excinfo.value.errors == response_body


class TestErrorRouterDownloadErrors:
    """Unit tests for download error handling in ErrorRouter."""

    def test_handle_download_response_with_message(self):
        """Test download error handling with error message."""
        router = ErrorRouter()
        response_body = {
            "error": {
                "type": "download_error",
                "message": "File not found",
            }
        }
        with pytest.raises(DownloadException) as excinfo:
            router._handle_download_response(response_body, 404)
        assert "File not found" in str(excinfo.value)

    def test_handle_download_response_without_message(self):
        """Test download error handling when message is missing."""
        router = ErrorRouter()
        response_body = {"error": {}}
        with pytest.raises(DownloadException) as excinfo:
            router._handle_download_response(response_body, 400)
        assert "Download error" in str(excinfo.value)

    def test_download_error_includes_response_code(self):
        """Test that download exception includes HTTP status code."""
        router = ErrorRouter()
        response_body = {"error": {"message": "Access denied"}}
        with pytest.raises(DownloadException) as excinfo:
            router._handle_download_response(response_body, 403)
        assert excinfo.value.response_body == response_body


class TestErrorRouterStartErrors:
    """Unit tests for start error handling in ErrorRouter."""

    def test_handle_start_response_with_type(self):
        """Test start error handling when error type is present."""
        router = ErrorRouter()
        response_body = {
            "error": {
                "type": "start_error",
                "message": "Invalid task parameters",
            }
        }
        with pytest.raises(StartException) as excinfo:
            router._handle_start_response(response_body, 400)
        assert "Invalid task parameters" in str(excinfo.value)

    def test_handle_start_response_without_type(self):
        """Test start error handling when error type is missing."""
        router = ErrorRouter()
        response_body = {"error": {"message": "Bad Request"}}
        with pytest.raises(StartException) as excinfo:
            router._handle_start_response(response_body, 400)
        assert "Bad Request" in str(excinfo.value)

    def test_handle_start_response_without_message(self):
        """Test start error handling when neither type nor message exists."""
        router = ErrorRouter()
        response_body = {"error": {}}
        with pytest.raises(StartException) as excinfo:
            router._handle_start_response(response_body, 400)
        assert "Bad Request" in str(excinfo.value)

    def test_start_error_includes_response_code(self):
        """Test that start exception includes HTTP status code."""
        router = ErrorRouter()
        response_body = {"error": {"type": "validation", "message": "Invalid"}}
        with pytest.raises(StartException) as excinfo:
            router._handle_start_response(response_body, 422)
        assert excinfo.value.response_body == response_body


class TestErrorRouterBadRequestErrors:
    """Unit tests for bad request (400) error handling in ErrorRouter."""

    def test_handle_bad_request_for_task_endpoint(self):
        """Test bad request error handling for task-related endpoints."""
        router = ErrorRouter()
        response_body = {"error": {"type": "invalid_task"}}
        with pytest.raises(TaskException) as excinfo:
            router._handle_bad_request("task/123", response_body, 400)
        assert "Invalid task id" in str(excinfo.value)

    def test_handle_bad_request_for_signature_endpoint_with_type(self):
        """Test bad request error handling for signature endpoint."""
        router = ErrorRouter()
        response_body = {"error": {"type": "invalid_signature"}}
        with pytest.raises(SignatureException) as excinfo:
            router._handle_bad_request("signature", response_body, 400)
        assert "invalid_signature" in str(excinfo.value)

    def test_handle_bad_request_for_signature_endpoint_without_type(self):
        """Test signature error when error type is missing."""
        router = ErrorRouter()
        response_body = {"error": {}}
        with pytest.raises(SignatureException):
            router._handle_bad_request("signature", response_body, 400)

    def test_handle_bad_request_generic_with_error_type(self):
        """Test generic bad request with error type."""
        router = ErrorRouter()
        response_body = {
            "error": {"type": "validation_error", "message": "Invalid data"}
        }
        with pytest.raises(ProcessException) as excinfo:
            router._handle_bad_request("generic", response_body, 400)
        assert "Invalid data" in str(excinfo.value)

    def test_handle_bad_request_generic_without_error_type(self):
        """Test generic bad request without error type."""
        router = ErrorRouter()
        response_body = {"error": {}}
        with pytest.raises(ProcessException) as excinfo:
            router._handle_bad_request("generic", response_body, 400)
        assert "Bad Request" in str(excinfo.value)


class TestErrorRouterGenericErrors:
    """Unit tests for generic error handling in ErrorRouter."""

    def test_handle_generic_error_with_message(self):
        """Test generic error handling with message."""
        router = ErrorRouter()
        response_body = {"error": {"message": "Internal server error"}}
        with pytest.raises(ProcessException) as excinfo:
            router._handle_generic_error(response_body, 500)
        assert "HTTP 500" in str(excinfo.value)
        assert "Internal server error" in str(excinfo.value)

    def test_handle_generic_error_without_message(self):
        """Test generic error handling without message."""
        router = ErrorRouter()
        response_body = {"error": {}}
        with pytest.raises(ProcessException) as excinfo:
            router._handle_generic_error(response_body, 503)
        assert "HTTP 503" in str(excinfo.value)
        assert "Bad Request" in str(excinfo.value)

    def test_handle_generic_error_empty_error_object(self):
        """Test generic error handling with empty error object."""
        router = ErrorRouter()
        response_body = {}
        with pytest.raises(ProcessException) as excinfo:
            router._handle_generic_error(response_body, 502)
        assert "HTTP 502" in str(excinfo.value)


class TestErrorRouterRouting:
    """Unit tests for error routing logic in ErrorRouter."""

    def test_route_to_upload_handler(self):
        """Test that upload endpoint routes to upload handler."""
        router = ErrorRouter()
        response_body = {"error": {"message": "Upload failed"}}
        with pytest.raises(UploadException):
            router.route("upload", response_body, 400)

    def test_route_to_process_handler(self):
        """Test that process endpoint routes to process handler."""
        router = ErrorRouter()
        response_body = {"error": {"message": "Process failed"}}
        with pytest.raises(ProcessException):
            router.route("process", response_body, 400)

    def test_route_to_download_handler(self):
        """Test that download endpoint routes to download handler."""
        router = ErrorRouter()
        response_body = {"error": {"message": "Download failed"}}
        with pytest.raises(DownloadException):
            router.route("download/abc", response_body, 400)

    def test_route_to_start_handler(self):
        """Test that start endpoint routes to start handler."""
        router = ErrorRouter()
        response_body = {"error": {"message": "Start failed"}}
        with pytest.raises(StartException):
            router.route("start/abc", response_body, 400)

    def test_route_handles_too_many_requests(self):
        """Test that 429 status code routes to ProcessException."""
        router = ErrorRouter()
        response_body = {"error": {"message": "Rate limited"}}
        with pytest.raises(ProcessException) as excinfo:
            router.route("unknown", response_body, 429)
        assert "Too Many Requests" in str(excinfo.value)

    def test_route_handles_bad_request(self):
        """Test that 400 status code routes to bad request handler."""
        router = ErrorRouter()
        response_body = {"error": {"message": "Bad request"}}
        with pytest.raises(ProcessException):
            router.route("unknown", response_body, 400)

    def test_route_handles_generic_error(self):
        """Test that unknown status codes route to generic handler."""
        router = ErrorRouter()
        response_body = {"error": {"message": "Server error"}}
        with pytest.raises(ProcessException) as excinfo:
            router.route("unknown", response_body, 500)
        assert "HTTP 500" in str(excinfo.value)


class TestErrorRouterEndpointPrefixMatching:
    """Unit tests for endpoint prefix matching in ErrorRouter."""

    def test_download_prefix_matching(self):
        """Test that download prefix matches various download endpoints."""
        router = ErrorRouter()
        response_body = {"error": {"message": "Download error"}}

        # Test various download endpoint formats
        endpoints = ["download", "download/123", "download_file"]
        for endpoint in endpoints:
            with pytest.raises(DownloadException):
                router.route(endpoint, response_body, 400)

    def test_start_prefix_matching(self):
        """Test that start prefix matches various start endpoints."""
        router = ErrorRouter()
        response_body = {"error": {"type": "error", "message": "Start error"}}

        # Test various start endpoint formats
        endpoints = ["start", "start/123", "start_task"]
        for endpoint in endpoints:
            with pytest.raises(StartException):
                router.route(endpoint, response_body, 400)


class TestErrorRouterExceptionDetails:
    """Unit tests for exception details in ErrorRouter responses."""

    def test_exception_contains_response_body(self):
        """Test that raised exceptions contain the response body."""
        router = ErrorRouter()
        response_body = {
            "error": {
                "type": "test_error",
                "message": "Test message",
            }
        }
        with pytest.raises(ProcessException) as excinfo:
            router._handle_generic_error(response_body, 500)
        assert excinfo.value.errors is not None
        assert "HTTP 500" in str(excinfo.value)

    def test_exception_contains_response_code(self):
        """Test that raised exceptions contain the response code."""
        router = ErrorRouter()
        response_body = {"error": {"message": "Error"}}
        with pytest.raises(ProcessException) as excinfo:
            router._handle_generic_error(response_body, 503)
        assert "HTTP 503" in str(excinfo.value)

    def test_upload_exception_with_multiple_errors(self):
        """Test upload exception with complex error structure."""
        router = ErrorRouter()
        response_body = {
            "error": {
                "type": "upload_failed",
                "message": "Multiple files failed",
                "files": ["file1.jpg", "file2.jpg"],
            }
        }
        with pytest.raises(UploadException) as excinfo:
            router._handle_upload_response(response_body, 400)
        assert excinfo.value.response_body == response_body
