"""Module for handling file tasks using the iLovePDF API."""

import os
import re
from collections.abc import Callable
from typing import Any, Generic, TypeVar, cast
from urllib.parse import unquote

from .abstract_task_element import AbstractTaskElement
from .exceptions import (
    FileExtensionNotAllowed,
    FileTooLargeError,
    PathException,
    StartException,
    UploadException,
)
from .file import File
from .ilovepdf_api import Ilovepdf

FILE_EXTENSIONS = ["pdf"]

MAX_SIZE_MB = 100  # File size limit (100 MB)


T_FILE = TypeVar("T_FILE", bound=File)


T = TypeVar("T")


class FileManager:
    """Manages file operations including validation and upload processing.

    This class encapsulates file extension validation, size checking, and
    processing of upload responses from the API.
    """

    def __init__(
        self, cls_file: type[File] = File, file_extensions: list[str] | None = None
    ):
        """Initialize FileManager.

        Args:
            cls_file (type[File]): The File class to use for file objects.
        """
        self.cls_file = cls_file
        self.file_extensions = file_extensions or FILE_EXTENSIONS

    def validate_extension(
        self,
        file_path: str,
        extension_list: list[str] | None = None,
    ) -> None:
        """Validate that the file extension is allowed.

        Args:
            file_path (str): Path to the file.
            extension_list (list[str] | None): List of allowed extensions.

        Raises:
            FileExtensionNotAllowed: If the file extension is not allowed.
        """
        if extension_list is None:
            extension_list = self.file_extensions

        extension_list_format = self.get_extension_format(extension_list)
        if not any(file_path.lower().endswith(ext) for ext in extension_list_format):
            msg = "File extension not allowed. Supported extensions: "
            msg += " ".join(extension_list_format)
            raise FileExtensionNotAllowed(msg)

    def validate_file_exists(self, file_path: str) -> None:
        """Validate that a file exists and is within size limits.

        Args:
            file_path (str): Path to the file.

        Raises:
            ValueError: If file does not exist or exceeds size limit.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File {file_path} does not exist")

        file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
        if file_size_mb > MAX_SIZE_MB:
            raise FileTooLargeError(
                f"File {file_path} exceeds the maximum allowed size ({MAX_SIZE_MB} MB)"
            )

    def get_extension_list(self) -> list[str]:
        """Get the list of allowed file extensions.

        Returns:
            List[str]: List of allowed extensions.
        """
        return self.file_extensions

    def get_extension_format(
        self,
        extension_list: list[str] | None = None,
    ) -> tuple:
        """Get extensions in dot format (e.g., '.pdf').

        Args:
            extension_list (list[str] | None): List of extensions to format.

        Returns:
            tuple: Tuple of formatted extensions.
        """
        ext_list = extension_list or self.file_extensions
        return tuple(f".{ext}" for ext in ext_list)

    def process_upload_response(self, response: Any, file_path: str) -> File:
        """Process the API response after uploading a file.

        Args:
            response: The API response object.
            file_path (str): Path to the uploaded file.

        Returns:
            File: The File object created from the response.

        Raises:
            UploadException: If the response is invalid.
        """
        try:
            response_body = response.json()
        except Exception as exc:
            raise UploadException("Upload response error") from exc

        filename = os.path.basename(file_path) or self.cls_file.get_temp_filename()
        file = self.cls_file(response_body["server_filename"], filename)
        return file


class DownloadManager:
    """Manages file download operations including path validation and
    response processing.

    This class handles download path validation, file content storage,
    and metadata extraction from download responses.
    """

    def __init__(self):
        """Initialize DownloadManager."""
        self.output_file: bytes | None = None
        self.output_filename: str | None = None
        self.output_file_name: str | None = None
        self.output_file_type: str | None = None

    def validate_download_path(self, path: str | None) -> None:
        """Validate the download destination path.

        Args:
            path (str | None): The destination path.

        Raises:
            PathException: If the path is invalid.
        """
        if path is None:
            return

        if not os.path.isdir(path):
            if os.path.splitext(path)[1]:
                raise PathException(
                    "Invalid download path. Use method set_output_filename() "
                    "to set the output file name."
                )
            raise PathException(
                "Invalid download path. Set a valid folder path to download the file."
            )

    def save_file(self, path: str | None, filename: str | None) -> None:
        """Save downloaded file to disk.

        Args:
            path (str | None): Destination folder path.
            filename (str | None): Filename to use.

        Raises:
            ValueError: If output file data is None.
        """
        if self.output_file is None:
            raise ValueError("Data to write cannot be None")

        destination = os.path.join(path or ".", filename or "")
        with open(destination, "wb") as file_dest:
            file_dest.write(self.output_file)

    def process_download_response(self, response: Any) -> None:
        """Process download response and extract metadata.

        Args:
            response: The API response object.
        """
        self.output_file = response.content
        content_disposition = response.headers.get("Content-Disposition", "")

        filename = None

        # Try UTF-8 encoded filename first
        match = re.search(r"filename\*=utf-8\'\'([^\s]+)", content_disposition)
        if match:
            filename = unquote(match.group(1).replace('"', ""))
        else:
            # Try regular filename
            match = re.search(r'filename="([^"]+)"', content_disposition)
            if match:
                filename = match.group(1)

        self.output_file_name = filename or "output_unknown_filename.unknown"
        self.output_file_type = (
            os.path.splitext(self.output_file_name)[1][1:]
            if self.output_file_name
            else None
        )


class PayloadBuilder:
    """Builds and validates request payloads for tasks.

    This class encapsulates payload construction and validation logic
    for API requests.
    """

    def __init__(self, to_payload_func: Callable[[], dict[str, Any]]) -> None:
        """Initialize PayloadBuilder.

        Args:
            to_payload_func (Callable[[], dict[str, Any]]): Function that returns the
                payload dictionary.
        """
        self._to_payload = to_payload_func

    def build_body(self, version: str) -> dict[str, Any]:
        """Build the request body for API operations.

        Args:
            version (str): The library version.

        Returns:
            dict[str, Any]: The request body dictionary.

        Raises:
            ValueError: If body is invalid.
        """
        data = self._to_payload()

        # Remove server config keys
        for key in ["timeout_large", "timeout", "time_delay"]:
            data.pop(key, None)

        body = {"data": data, "params": {"v": version}}
        self.validate_body(body)
        return body

    @staticmethod
    def validate_body(body: dict[str, Any] | None) -> bool:
        """Validate the request body.

        Args:
            body (dict[str, Any] | None): The request body dictionary.

        Returns:
            bool: True if valid.

        Raises:
            ValueError: If the body is invalid.
        """
        if not body:
            raise ValueError("Invalid body")
        return True


class TaskStateManager:
    """Manages task state including validation and state updates.

    This class encapsulates task state management, including task ID
    tracking, status updates, and validation.
    """

    def __init__(self):
        """Initialize TaskStateManager."""
        self.task: str | None = None
        self.status: str | None = None
        self.status_message: str | None = None
        self.remaining_credits: int | None = None
        self.remaining_files: int | None = None
        self.remaining_pages: int | None = None

    def validate_task_started(self) -> None:
        """Validate that the task has been started.

        Raises:
            ValueError: If the task is not started.
        """
        if not self.task:
            raise ValueError("Current task does not exist. You must start your task")

    def set_task(self, task: str) -> None:
        """Set the task ID.

        Args:
            task (str): The task ID.
        """
        self.task = task

    def get_task_id(self) -> str | None:
        """Get the task ID.

        Returns:
            str | None: The task ID.
        """
        return self.task

    def set_remaining_credits(self, remaining_credits: int | None) -> None:
        """Set the remaining credits.

        Args:
            remaining_credits (int | None): Number of remaining credits.
        """
        self.remaining_credits = remaining_credits

    def set_remaining_files(self, remaining_files: int | None) -> None:
        """Set the remaining files.

        Args:
            remaining_files (int | None): Number of remaining files.
        """
        self.remaining_files = remaining_files

    def set_remaining_pages(self, remaining_pages: int | None) -> None:
        """Set the remaining pages.

        Args:
            remaining_pages (int | None): Number of remaining pages.
        """
        self.remaining_pages = remaining_pages

    def update_status(self, result: dict[str, Any]) -> None:
        """Update task status from result.

        Args:
            result (dict[str, Any]): The result dictionary from API.
        """
        self.status = result.get("status")
        self.status_message = result.get("status_message")


class Task(Ilovepdf, Generic[T_FILE], AbstractTaskElement):
    """
    Class for handling file tasks using the iLovePDF API.

    This class provides core functionality for managing file-based tasks such
    as uploading, downloading, and processing files. It supports validation,
    error handling, and integration with the iLovePDF API.


    Args:
        public_key (str, optional): API public key. If not provided,
            uses ILOVEPDF_PUBLIC_KEY env variable.
        secret_key (str, optional): API secret key. If not provided,
            uses ILOVEPDF_SECRET_KEY env variable.
        make_start (bool): Whether to start the task immediately.
            Default is False.

    Example:
        class AnyTask(Task):
            _tool = "anytool"

            _DEFAULT_PAYLOAD = {
                "attr1": "value1",
                "attr2": "value2",
            }

        @property
        def attr1(self) -> str:
            return self._get_attr("attr1")

        @attr1.setter
        def attr1(self, value: str):
            self._set_attr("attr1", value)

        # Instantiate the task
        any_tool = AnyTask(public_key, secret_key)
    """

    cls_file: type[T_FILE] = File  # type: ignore
    _file_extension: list = FILE_EXTENSIONS
    _endpoint_execute = "process"
    _tool: str
    _task_status = "TaskSuccess"

    _DEFAULT_PAYLOAD = {
        "tool": None,
        "task": None,
        "files": [],
    }

    def __init__(
        self,
        public_key: str | None = None,
        secret_key: str | None = None,
        make_start: bool = True,
    ) -> None:
        """
        Initialize a Task instance.

        Args:
            public_key (str | None): API public key.
            secret_key (str | None): API secret key.
            make_start (bool): Whether to start the task immediately.
        """
        super().__init__(public_key, secret_key)
        self.result: dict[str, Any] | None = None
        self._file_manager = FileManager(self.cls_file, self._file_extension)
        self._download_manager = DownloadManager()
        self._payload_builder = PayloadBuilder(self._to_payload)
        self._state_manager = TaskStateManager()

        self.tool = self._tool

        if make_start:
            self.start()

    @property
    def tool(self) -> str | None:
        """Get the tool name.

        Returns:
            str | None: The current tool name. Default is None.
        """
        return self._payload["tool"]

    @tool.setter
    def tool(self, value: str | None) -> None:
        """Set the tool name.

        Args:
            value (str | None): The tool name.
        """
        self._payload["tool"] = value

    @property
    def files(self):
        """Get the files of the task."""
        return self._get_attr("files")

    def start(self) -> None:
        """
        Start the task by requesting a server assignment from the API.

        Raises:
            StartException: If the tool is not set or the API response is
                invalid.
        """
        if self.tool is None:
            raise StartException("Tool must be set")

        data = {"v": self.VERSION}
        body = {"params": data}
        response = self.send_request("get", f"start/{self.tool}", body)

        try:
            response_body = response.json()
        except Exception as exc:
            raise StartException("Invalid response") from exc

        if not response_body.get("server"):
            raise StartException("no server assigned on start")

        # Update state
        self._state_manager.set_remaining_files(response_body.get("remaining_files"))
        self._state_manager.set_remaining_pages(response_body.get("remaining_pages"))
        self._state_manager.set_remaining_credits(
            response_body.get("remaining_credits")
        )

        # Set server and task
        self.set_worker_server("https://" + response_body["server"])
        self.set_task(response_body["task"])

    def set_task(self, task: str) -> None:
        """Set the current task ID.

        Args:
            task (str): The task ID.
        """
        self._state_manager.set_task(task)
        self._payload["task"] = task

    def get_task_id(self) -> str | None:
        """Get the current task ID.

        Returns:
            str | None: The task ID, or None if not set.
        """
        return self._state_manager.get_task_id()

    def append_file(self, file: T_FILE) -> T_FILE:
        """Append a file to the task's file list.

        Args:
            file (T_FILE): The File object to append.

        Returns:
            T_FILE: The appended File object.
        """
        self.files.append(file)
        return file

    def _validate_and_upload_file(
        self, file_path: str, extension_list: list[str] | None = None, **kwargs: Any
    ) -> T_FILE:
        """Validate and upload a file with optional extension filtering.

        This helper method encapsulates the common pattern of validating
        file extension, checking task state, uploading the file, and ensuring
        the correct File instance type.

        Args:
            file_path (str): Path to the file to upload.
            extension_list (Optional[List[str]]): List of allowed file extensions.
                If None, uses the task's default allowed extensions.
            **kwargs (Any): Additional parameters for file upload.

        Returns:
            T_FILE: The uploaded File object.

        Raises:
            ValueError: If the file extension is not valid.
            ProcessingError: If the task has not been started yet.
        """
        self._file_manager.validate_extension(file_path, extension_list=extension_list)
        self._state_manager.validate_task_started()
        file = self.upload_file(self.get_task_id(), file_path, kwargs)
        if not isinstance(file, self.cls_file):
            file = self.cls_file(file.server_filename, file.filename)
        return file

    def add_file(self, file_path: str, **kwargs: Any) -> T_FILE:
        """Add a file to the task by uploading it.

        Args:
            file_path (str): Path to the file to add.
            **kwargs: Additional parameters for file upload.

        Returns:
            T_FILE: The uploaded File object.

        Raises:
            ValueError: If the file extension is not supported or the task
                is not started.
        """
        file = self._validate_and_upload_file(file_path, **kwargs)
        self.append_file(file)
        return file

    def add_file_from_url(self, url, bearer_token=None, extra_params=None) -> T_FILE:
        """Add a file to the task by uploading it from a URL.

        Args:
            url (str): URL to the file to add.
            bearer_token (str | None): Bearer token for authentication.
            extra_params (Dict[str, Any] | None): Additional parameters
                for file upload.

        Returns:
            T_FILE: The uploaded File object.

        Raises:
            ValueError: If the task is not started.
        """
        self._validate_task_started()
        file = self.upload_url(self.task, url, bearer_token, extra_params)
        self.files.append(file)
        return self.files[-1]

    def upload_file(
        self,
        task: str | None,
        file_path: str,
        extra_params: dict[str, Any] | None = None,
    ) -> T_FILE:
        """Upload a file to the API for the current task.

        Args:
            task (str | None): The task ID.
            file_path (str): Path to the file to upload.
            extra_params (Dict[str, Any] | None): Additional parameters
                for upload.

        Returns:
            T_FILE: The uploaded File object.

        Raises:
            ValueError: If the file does not exist or exceeds size limit.
        """
        self._file_manager.validate_file_exists(file_path)

        with open(file_path, "rb") as file_obj:
            files = {"file": file_obj}
            data: dict[str, Any] = {"task": task, "v": self.VERSION}
            if extra_params:
                data.update(extra_params)
            body = {"files": files, "data": data}
            response = self.send_request("post", "upload", body)

        return cast(
            T_FILE, self._file_manager.process_upload_response(response, file_path)
        )

    def get_status(
        self,
        server: str | None = None,
        task_id: str | None = None,
    ) -> dict[str, Any]:
        """Get the status of the current task from the API.

        Args:
            server (str | None): The server URL. If not provided,
                uses the current worker server.
            task_id (str | None): The task ID. If not provided,
                uses the current task ID.

        Returns:
            Dict[str, Any]: Status response from the API.

        Raises:
            ValueError: If server or task_id is not set.
        """
        server = server or self.get_worker_server()
        task_id = task_id or self.get_task_id()

        if server is None or task_id is None:
            raise ValueError("Cannot get status if no file is uploaded")

        return super().get_status(server, task_id)

    def _get_file_from_upload_response(self, response, file_path) -> T_FILE:
        """Get a File object from an upload response.

        Args:
            response (Response): Response object from upload request.
            file_path (str): Path to the file.

        Returns:
            T_FILE: The uploaded File object.
        """
        cls_file = self.cls_file
        try:
            response_body = response.json()
        except Exception as exc:
            raise UploadException("Upload response error") from exc
        filename = os.path.basename(file_path) or cls_file.get_temp_filename()
        file = cls_file(response_body["server_filename"], filename)
        if "pdf_pages" in response_body:
            file.pdf_pages = response_body["pdf_pages"]
        if "pdf_page_number" in response_body:
            file.pdf_page_number = int(response_body["pdf_page_number"])
        if "pdf_forms" in response_body:
            file.pdf_forms = response_body["pdf_forms"]
        return file

    def upload_url(self, task, url, bearer_token=None, extra_params=None) -> T_FILE:
        """Upload a file from a URL.

        Args:
            task (str): Task ID.
            url (str): URL of the file.
            bearer_token (str, optional): Bearer token for authentication.
                Defaults to None.
            extra_params (dict, optional): Extra parameters for the request.
                Defaults to None.

        Returns:
            T_FILE: The uploaded File object.
        """
        body = self._get_body_for_upload_url_file(task, url, bearer_token, extra_params)
        response = self.send_request("post", "upload", body)
        return self._get_file_from_upload_response(response, url)

    def _get_body_for_upload_url_file(
        self, task, url, bearer_token=None, extra_params=None
    ):
        data = {"cloud_file": url, "task": task, "v": self.VERSION}
        if bearer_token:
            data["cloud_token"] = bearer_token
        if extra_params:
            data.update(extra_params)
        return {"data": data}

    def delete(self) -> "Task":
        """Delete the current task from the API.

        Returns:
            Task: Self for chaining.

        Raises:
            ValueError: If the task is not started.
        """
        self._state_manager.validate_task_started()
        response = self.send_request("delete", f"task/{self.get_task_id()}")
        self.result = response.json()
        return self

    def download(self, path: str | None = None) -> None:
        """Download the processed file from the API.

        Args:
            path (str | None): Destination folder path.

        Raises:
            PathException: If the path is invalid.
            ValueError: If the file data is None.
        """
        self._state_manager.validate_task_started()
        self._download_manager.validate_download_path(path)

        # Download file data
        response = self._download_request_data(self.get_task_id())
        self._download_manager.process_download_response(response)

        # Save to disk
        dest_path = path or "."
        filename = (
            self._download_manager.output_filename
            or self._download_manager.output_file_name
        )
        self._download_manager.save_file(dest_path, filename)

    def _download_request_data(self, task: str | None) -> Any:
        """Build and send the download request for the given task.

        Args:
            task (str | None): The task ID.

        Returns:
            Any: The API response object.
        """
        data = {"v": self.VERSION}
        body = {"data": data}
        response = self.send_request("get", f"download/{task}", body)
        return response

    def execute(self) -> "Task":
        """Execute the current task by sending it to the API.

        Returns:
            Task: Self for chaining.

        Raises:
            ValueError: If the task is not started.
        """
        self._state_manager.validate_task_started()
        body = self._payload_builder.build_body(self.VERSION)
        endpoint = self._endpoint_execute
        response = self.send_request("post", endpoint, body)
        self.result = response.json()

        # Update status after execution
        if self.result is not None:
            self._state_manager.update_status(self.result)
        return self

    def set_output_filename(self, filename: str) -> "Task":
        """Set the output filename for the downloaded file.

        Args:
            filename (str): The output filename.

        Returns:
            Task: Self for chaining.
        """
        self._download_manager.output_filename = filename
        return self

    @property
    def output_file(self) -> bytes | None:
        """Get the downloaded file content.

        Returns:
            bytes | None: The file content, or None if not downloaded.
        """
        return self._download_manager.output_file

    @property
    def output_filename(self) -> str | None:
        """Get the output filename set by user.

        Returns:
            str | None: The output filename.
        """
        return self._download_manager.output_filename

    @property
    def output_file_name(self) -> str | None:
        """Get the output file name from response.

        Returns:
            str | None: The file name extracted from response.
        """
        return self._download_manager.output_file_name

    @property
    def output_file_type(self) -> str | None:
        """Get the output file type.

        Returns:
            str | None: The file extension.
        """
        return self._download_manager.output_file_type

    @property
    def task(self) -> str | None:
        """Get the task ID.

        Returns:
            str | None: The task ID. Default is None.
        """
        return self._state_manager.task

    @task.setter
    def task(self, value: str | None) -> None:
        """Set the task ID.

        Args:
            value (str | None): The task ID.
        """
        self._state_manager.task = value

    @property
    def status(self) -> str | None:
        """Get the task status.

        Returns:
            str | None: The task status. Default is None.
        """
        return self._state_manager.status

    @property
    def status_message(self) -> str | None:
        """Get the task status message.

        Returns:
            str | None: The status message. Default is None.
        """
        return self._state_manager.status_message

    @property
    def remaining_files(self) -> int | None:
        """Get remaining files count.

        Returns:
            int | None: Number of remaining files. Default is None.
        """
        return self._state_manager.remaining_files

    @property
    def remaining_pages(self) -> int | None:
        """Get remaining pages count.

        Returns:
            int | None: Number of remaining pages. Default is None.
        """
        return self._state_manager.remaining_pages

    @property
    def remaining_credits(self) -> int | None:
        """Get remaining credits count.

        Returns:
            int | None: Number of remaining credits. Default is None.
        """
        return self._state_manager.remaining_credits

    def _validate_file_extension(
        self, file_path: str, extension_list: list[str] | None = None
    ) -> None:
        """Validate file extension.

        Args:
            file_path (str): Path to the file.
            extension_list (list[str | None]): List of allowed extensions.

        Raises:
            ValueError: If the file extension is not allowed.
        """
        self._file_manager.validate_extension(file_path, extension_list)

    def _validate_task_started(self) -> None:
        """Validate that task has been started.

        Raises:
            ValueError: If the task is not started.
        """
        self._state_manager.validate_task_started()

    def get_extension_list(self) -> list[str]:
        """Get the list of allowed file extensions.

        Returns:
            List[str]: List of allowed extensions.
        """
        return self._file_manager.get_extension_list()

    def get_extension_list_format(
        self, extension_list: list[str] | None = None
    ) -> tuple:
        """Get extensions in dot format.

        Args:
            extension_list (List[str] | None): List of extensions to format.

        Returns:
            tuple: Tuple of formatted extensions.
        """
        return self._file_manager.get_extension_format(extension_list)

    def _set_remaining_credits(self, remaining_credits: int) -> None:
        """Set remaining credits.

        Args:
            remaining_credits (int): Number of remaining credits.
        """
        self._state_manager.set_remaining_credits(remaining_credits)

    def _set_remaining_files(self, remaining_files: int) -> None:
        """Set remaining files.

        Args:
            remaining_files (int): Number of remaining files.
        """
        self._state_manager.set_remaining_files(remaining_files)

    def _set_remaining_pages(self, remaining_pages: int) -> None:
        """Set remaining pages.

        Args:
            remaining_pages (int): Number of remaining pages.
        """
        self._state_manager.set_remaining_pages(remaining_pages)

    def validate_body(self, body: dict[str, Any]) -> bool:
        """Validate request body.

        Args:
            body (Dict[str, Any]): The request body dictionary.

        Returns:
            bool: True if valid.

        Raises:
            ValueError: If the body is invalid.
        """
        return self._payload_builder.validate_body(body)

    def build_body(self) -> dict[str, Any]:
        """Build request body.

        Returns:
            Dict[str, Any]: The request body dictionary.
        """
        return self._payload_builder.build_body(self.VERSION)
