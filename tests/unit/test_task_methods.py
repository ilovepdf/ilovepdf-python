"""Unit tests for Task class methods in the ilovepdf module.

These tests verify the correct behavior of Task methods including start,
upload_file, get_status, download, and execute with various scenarios
and error conditions.
"""

from unittest.mock import MagicMock

import pytest
from pytest_mock import MockerFixture

from ilovepdf import Task
from ilovepdf.exceptions import StartException
from ilovepdf.file import File

# pylint: disable=protected-access


class DummyTask(Task):
    """Dummy Task class for testing."""

    _tool = "dummytool"

    def __init__(self, public_key, secret_key, make_start=True):
        super().__init__(public_key, secret_key, make_start=False)


class TestTaskStart:
    """Unit tests for Task.start() method."""

    def test_start_success(self, mocker: MockerFixture):
        """Test successful task start with valid response."""
        task = DummyTask("public_key", "secret_key")

        mock_response = MagicMock()
        mock_response.json.return_value = {
            "server": "example.com:8080",
            "task": "task_123",
            "remaining_files": 10,
            "remaining_pages": 100,
            "remaining_credits": 1000,
        }
        mocker.patch.object(task, "send_request", return_value=mock_response)

        task.start()

        assert task.get_task_id() == "task_123"
        assert task.get_worker_server() == "https://example.com:8080"

    def test_start_without_tool_raises_exception(self):
        """Test that start raises StartException when tool is not set."""
        task = DummyTask("public_key", "secret_key")
        task.tool = None

        with pytest.raises(StartException) as excinfo:
            task.start()
        assert "Tool must be set" in str(excinfo.value)

    def test_start_with_invalid_json_response(self, mocker: MockerFixture):
        """Test that start raises StartException with invalid JSON response."""
        task = DummyTask("public_key", "secret_key")

        mock_response = MagicMock()
        mock_response.json.side_effect = Exception("Invalid JSON")
        mocker.patch.object(task, "send_request", return_value=mock_response)

        with pytest.raises(StartException) as excinfo:
            task.start()
        assert "Invalid response" in str(excinfo.value)

    def test_start_without_server_in_response(self, mocker: MockerFixture):
        """Test that start raises StartException when server not in response."""
        task = DummyTask("public_key", "secret_key")

        mock_response = MagicMock()
        mock_response.json.return_value = {
            "task": "task_123",
            # Missing "server" key
        }
        mocker.patch.object(task, "send_request", return_value=mock_response)

        with pytest.raises(StartException) as excinfo:
            task.start()
        assert "no server assigned" in str(excinfo.value)

    def test_start_updates_state_manager(self, mocker: MockerFixture):
        """Test that start updates state manager with response data."""
        task = DummyTask("public_key", "secret_key")

        mock_response = MagicMock()
        mock_response.json.return_value = {
            "server": "example.com",
            "task": "task_456",
            "remaining_files": 5,
            "remaining_pages": 50,
            "remaining_credits": 500,
        }
        mocker.patch.object(task, "send_request", return_value=mock_response)

        task.start()

        assert task._state_manager.remaining_files == 5
        assert task._state_manager.remaining_pages == 50
        assert task._state_manager.remaining_credits == 500

    def test_start_sends_correct_request(self, mocker: MockerFixture):
        """Test that start sends request with correct parameters."""
        task = DummyTask("public_key", "secret_key")

        mock_response = MagicMock()
        mock_response.json.return_value = {
            "server": "example.com",
            "task": "task_789",
        }
        mock_send = mocker.patch.object(
            task, "send_request", return_value=mock_response
        )

        task.start()

        mock_send.assert_called_once()
        call_args = mock_send.call_args
        assert call_args[0][0] == "get"
        assert "start" in call_args[0][1]


class TestTaskUploadFile:
    """Unit tests for Task.upload_file() method."""

    def test_upload_file_success(self, mocker: MockerFixture, tmp_path):
        """Test successful file upload."""
        task = DummyTask("public_key", "secret_key")
        task.set_task("task_123")

        # Create a temporary file
        test_file = tmp_path / "test.jpg"
        test_file.write_bytes(b"fake image data")

        mock_response = MagicMock()
        mocker.patch.object(task, "send_request", return_value=mock_response)
        mock_process = mocker.patch.object(
            task._file_manager,
            "process_upload_response",
            return_value=File(filename="test.jpg", server_filename="server_test.jpg"),
        )

        result = task.upload_file("task_123", str(test_file))

        assert result.filename == "test.jpg"
        mock_process.assert_called_once()

    def test_upload_file_with_nonexistent_file(self):
        """Test upload_file raises error for nonexistent file."""
        task = DummyTask("public_key", "secret_key")

        with pytest.raises(FileNotFoundError) as excinfo:
            task.upload_file("task_123", "/nonexistent/file.jpg")
        assert "does not exist" in str(excinfo.value)

    def test_upload_file_with_extra_params(self, mocker: MockerFixture, tmp_path):
        """Test upload_file includes extra parameters in request."""
        task = DummyTask("public_key", "secret_key")
        task.set_task("task_123")

        # Create a temporary file
        test_file = tmp_path / "test.jpg"
        test_file.write_bytes(b"fake image data")

        mock_response = MagicMock()
        mock_send = mocker.patch.object(
            task, "send_request", return_value=mock_response
        )
        mocker.patch.object(
            task._file_manager,
            "process_upload_response",
            return_value=File(filename="test.jpg", server_filename="server_test.jpg"),
        )

        extra_params = {"custom_param": "value"}
        task.upload_file("task_123", str(test_file), extra_params)

        mock_send.assert_called_once()
        call_args = mock_send.call_args
        body = call_args[1]["body"] if "body" in call_args[1] else call_args[0][2]
        assert "custom_param" in body["data"]

    def test_upload_file_sends_correct_endpoint(self, mocker: MockerFixture, tmp_path):
        """Test that upload_file sends request to correct endpoint."""
        task = DummyTask("public_key", "secret_key")
        task.set_task("task_123")

        # Create a temporary file
        test_file = tmp_path / "test.jpg"
        test_file.write_bytes(b"fake image data")

        mock_response = MagicMock()
        mock_send = mocker.patch.object(
            task, "send_request", return_value=mock_response
        )
        mocker.patch.object(
            task._file_manager,
            "process_upload_response",
            return_value=File(filename="test.jpg", server_filename="server_test.jpg"),
        )

        task.upload_file("task_123", str(test_file))

        mock_send.assert_called_once()
        call_args = mock_send.call_args
        assert call_args[0][0] == "post"
        assert call_args[0][1] == "upload"


class TestTaskGetStatus:
    """Unit tests for Task.get_status() method."""

    def test_get_status_success(self, mocker: MockerFixture):
        """Test successful status retrieval."""
        task = DummyTask("public_key", "secret_key")
        task.set_worker_server("https://example.com")
        task.set_task("task_123")

        mock_response = MagicMock()
        status_data = {"status": "processing"}
        mock_response.json.return_value = status_data
        mocker.patch.object(task, "send_request", return_value=mock_response)

        result = task.get_status()

        assert result == status_data

    def test_get_status_with_custom_server(self, mocker: MockerFixture):
        """Test get_status with custom server parameter."""
        task = DummyTask("public_key", "secret_key")
        task.set_task("task_123")

        mock_response = MagicMock()
        mock_response.json.return_value = {"status": "done"}
        mock_send = mocker.patch.object(
            task, "send_request", return_value=mock_response
        )

        task.get_status(server="https://custom.com")

        mock_send.assert_called_once()

    def test_get_status_with_custom_task_id(self, mocker: MockerFixture):
        """Test get_status with custom task_id parameter."""
        task = DummyTask("public_key", "secret_key")
        task.set_worker_server("https://example.com")

        mock_response = MagicMock()
        mock_response.json.return_value = {"status": "done"}
        mock_send = mocker.patch.object(
            task, "send_request", return_value=mock_response
        )

        task.get_status(task_id="task_999")

        mock_send.assert_called_once()

    def test_get_status_without_server_raises_error(self):
        """Test get_status raises error when server not set."""
        task = DummyTask("public_key", "secret_key")
        task.set_task("task_123")

        with pytest.raises(ValueError):
            task.get_status()

    def test_get_status_without_task_raises_error(self):
        """Test get_status raises error when task_id not set."""
        task = DummyTask("public_key", "secret_key")
        task.set_worker_server("https://example.com")

        with pytest.raises(ValueError):
            task.get_status()


class TestTaskDownload:
    """Unit tests for Task.download() method."""

    def test_download_success(self, mocker: MockerFixture, tmp_path):
        """Test successful download."""
        task = DummyTask("public_key", "secret_key")
        task.set_task("task_123")
        task.set_worker_server("https://example.com")

        mock_response = MagicMock()
        mock_response.content = b"fake file content"
        mock_response.headers = {
            "content-disposition": 'attachment; filename="test.jpg"'
        }
        mock_send = mocker.patch.object(
            task, "send_request", return_value=mock_response
        )
        mock_save = mocker.patch.object(task._download_manager, "save_file")

        task.download(str(tmp_path))

        mock_send.assert_called_once()
        mock_save.assert_called_once()

    def test_download_validates_path(self, mocker: MockerFixture, tmp_path):
        """Test that download validates the output path."""
        task = DummyTask("public_key", "secret_key")
        task.set_task("task_123")
        task.set_worker_server("https://example.com")

        mock_response = MagicMock()
        mock_response.content = b"fake file content"
        mock_response.headers = {
            "content-disposition": 'attachment; filename="test.jpg"'
        }
        mocker.patch.object(task, "send_request", return_value=mock_response)
        mock_validate = mocker.patch.object(
            task._download_manager, "validate_download_path"
        )

        task.download(str(tmp_path))

        mock_validate.assert_called_once()

    def test_download_without_task_raises_error(self, tmp_path):
        """Test download raises error when task not started."""
        task = DummyTask("public_key", "secret_key")

        with pytest.raises(ValueError):
            task.download(str(tmp_path))


class TestTaskExecute:
    """Unit tests for Task.execute() method."""

    def test_execute_success(self, mocker: MockerFixture):
        """Test successful task execution."""
        task = DummyTask("public_key", "secret_key")
        task.set_task("task_123")
        task.set_worker_server("https://example.com")

        mock_response = MagicMock()
        mock_response.json.return_value = {"status": "success"}
        mock_send = mocker.patch.object(
            task, "send_request", return_value=mock_response
        )

        result = task.execute()

        assert result is task
        mock_send.assert_called_once()

    def test_execute_sends_to_correct_endpoint(self, mocker: MockerFixture):
        """Test that execute sends request to correct endpoint."""
        task = DummyTask("public_key", "secret_key")
        task.set_task("task_123")
        task.set_worker_server("https://example.com")

        mock_response = MagicMock()
        mock_response.json.return_value = {"status": "success"}
        mock_send = mocker.patch.object(
            task, "send_request", return_value=mock_response
        )

        task.execute()

        mock_send.assert_called_once()
        call_args = mock_send.call_args
        assert call_args[0][0] == "post"
        assert "process" in call_args[0][1]

    def test_execute_without_task_raises_error(self):
        """Test execute raises error when task not started."""
        task = DummyTask("public_key", "secret_key")

        with pytest.raises(ValueError):
            task.execute()

    def test_execute_returns_self(self, mocker: MockerFixture):
        """Test that execute returns self for method chaining."""
        task = DummyTask("public_key", "secret_key")
        task.set_task("task_123")
        task.set_worker_server("https://example.com")

        mock_response = MagicMock()
        mock_response.json.return_value = {"status": "success"}
        mocker.patch.object(task, "send_request", return_value=mock_response)

        result = task.execute()

        assert result is task


class TestTaskSetTask:
    """Unit tests for Task.set_task() method."""

    def test_set_task_updates_task_id(self):
        """Test that set_task updates the task ID."""
        task = DummyTask("public_key", "secret_key")

        task.set_task("task_456")

        assert task.get_task_id() == "task_456"
        assert task._payload["task"] == "task_456"

    def test_set_task_updates_state_manager(self):
        """Test that set_task updates state manager."""
        task = DummyTask("public_key", "secret_key")

        task.set_task("task_789")

        assert task._state_manager.get_task_id() == "task_789"


class TestTaskSetWorkerServer:
    """Unit tests for Task.set_worker_server() method."""

    def test_set_worker_server_updates_server(self):
        """Test that set_worker_server updates the server."""
        task = DummyTask("public_key", "secret_key")

        task.set_worker_server("https://new.server.com")

        assert task.get_worker_server() == "https://new.server.com"

    def test_set_worker_server_stores_value(self):
        """Test that set_worker_server stores the server URL."""
        task = DummyTask("public_key", "secret_key")

        task.set_worker_server("https://another.server.com")

        assert task.get_worker_server() == "https://another.server.com"
