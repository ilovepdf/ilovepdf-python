"""Module for handling file tasks using the ilovepdf API."""

import os
import re
from typing import Generic, Type, TypeVar
from urllib.parse import unquote

from .exceptions import PathException, StartException, UploadException
from .file import File
from .ilovepdf_api import Ilovepdf

MAX_SIZE_MB = 100  # File size limit (100 MB)


T_FILE = TypeVar("T_FILE", bound=File)  # pylint: disable=invalid-name


# T_FILE = TypeVar("T_FILE", bound=File)
# class Task(Ilovepdf, Generic[T_FILE]): # pylint: disable=too-many-instance-attributes,too-many-public-methods


class Task(
    Ilovepdf, Generic[T_FILE]
):  # pylint: disable=too-many-instance-attributes,too-many-public-methods
    """Module for handling file tasks using the ilovepdf API."""

    cls_file: Type[T_FILE] = File  # type: ignore
    _endpoint_execute = "process"

    DEFAULTS_VALUES = {}
    STATUS_VALUES = [
        "",
        "TaskSuccess",
        "TaskDeleted",
        "TaskWaiting",
        "TaskProcessing",
        "TaskSuccessWithWarnings",
        "TaskError",
        "TaskNotFound",
    ]

    def __init__(self, public_key=None, secret_key=None, make_start=False, tool=None):
        super().__init__(public_key, secret_key)
        self.task = None
        self.tool = tool
        self.files: list[T_FILE] = []
        self.packaged_filename = None
        self.outpuname = None
        self.ignore_errors = True
        self.ignore_password = True
        self.try_pdf_repair = True
        self.meta = {}
        self.webhook = None
        self.custom_int = None
        self.custom_string = None
        self.result = None
        self.output_file = None
        self.output_filename = None
        self.output_file_name = None
        self.output_file_type = None
        self.remaining_files = None
        self.remaining_pages = None
        self.remaining_credits = None
        self.status = None
        self.status_message = None
        self._params = dict(self.DEFAULTS_VALUES)

        if make_start:
            self.start()

    def start(self):
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
        self._set_remaining_files(response_body.get("remaining_files"))
        self._set_remaining_pages(response_body.get("remaining_pages"))
        self._set_remaining_credits(response_body.get("remaining_credits"))
        self.set_worker_server("https://" + response_body["server"])
        self.set_task(response_body["task"])

    def next(self, next_tool):
        data = {"v": self.VERSION, "task": self.get_task_id(), "tool": next_tool}
        body = {"params": data}
        try:
            response = self.send_request("post", "task/next", body)
            response_body = response.json()
            if not response_body.get("task"):
                raise StartException("No task assigned on chained start")
        except Exception as exc:
            raise StartException("Error on start chained task") from exc

        # Dynamic import for next task class
        raise NotImplementedError(
            "Dynamic task chaining not implemented. Import and instantiate the next task class directly."
        )

    def set_task(self, task):
        self.task = task
        return self

    def get_task_id(self):
        return self.task

    def set_files(self, files):
        if isinstance(files, list):
            self.files = files
        else:
            self.files = []

    def get_files(self):
        return self.files

    def get_files_array(self):
        return [file.get_file_options() for file in self.files]

    def get_status(self, server=None, task_id=None):
        server = server if server else self.get_worker_server()
        task_id = task_id if task_id else self.get_task_id()
        if server is None or task_id is None:
            raise ValueError("Cannot get status if no file is uploaded")
        return super().get_status(server, task_id)

    def append_file(self, file: T_FILE):
        self.files.append(file)

    def add_file(self, file_path, extra_params=None) -> T_FILE:
        self._validate_task_started()
        file = self.upload_file(self.task, file_path, extra_params)
        self.append_file(file)
        return file

    def add_file_from_url(self, url, bearer_token=None, extra_params=None) -> T_FILE:
        self._validate_task_started()
        file = self.upload_url(self.task, url, bearer_token, extra_params)
        self.files.append(file)
        return self.files[-1]

    def upload_file(self, task, file_path, extra_params=None) -> T_FILE:
        if not os.path.exists(file_path):
            raise ValueError(f"File {file_path} does not exist")
        if os.path.getsize(file_path) > MAX_SIZE_MB * 1024 * 1024:
            raise ValueError(
                f"File {file_path} exceeds the maximum allowed size ({MAX_SIZE_MB} MB)"
            )
        with open(file_path, "rb") as file_obj:
            files = {"file": file_obj}
            data = {"task": task, "v": self.VERSION}
            if extra_params:
                data.update(extra_params)
            body = {"files": files, "data": data}
            response = self.send_request("post", "upload", body)
        return self._get_file_from_upload_response(response, file_path)

    def _get_file_from_upload_response(self, response, file_path) -> T_FILE:
        cls_file = self.cls_file
        try:
            response_body = response.json()
        except Exception as exc:
            raise UploadException("Upload response error") from exc
        filename = os.path.basename(file_path) or cls_file.get_temp_filename()
        file = cls_file(response_body["server_filename"], filename)
        if "pdf_pages" in response_body:
            file.set_pdf_pages(response_body["pdf_pages"])
        if "pdf_page_number" in response_body:
            file.set_pdf_page_number(int(response_body["pdf_page_number"]))
        if "pdf_forms" in response_body:
            file.set_pdf_forms(response_body["pdf_forms"])
        return file

    def upload_url(self, task, url, bearer_token=None, extra_params=None) -> T_FILE:
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

    def delete(self):
        self._validate_task_started()
        response = self.send_request("delete", f"task/{self.get_task_id()}")
        self.result = response.json()
        return self

    def download(self, path=None):
        self._validate_task_started()
        if path is not None and not os.path.isdir(path):
            if not os.path.splitext(path)[1]:
                raise PathException(
                    "Invalid download path. Use method set_outpuname() to set the output file name."
                )
            raise PathException(
                "Invalid download path. Set a valid folder path to download the file."
            )
        self._download_file(self.task)
        if path is None:
            path = "."
        filename = self.output_filename or self.output_file_name
        destination = os.path.join(path or "", filename or "")
        with open(destination, "wb") as file_destination:
            # file_destination.write(self.output_file)
            if self.output_file is not None:
                file_destination.write(self.output_file)
            else:
                raise ValueError("Data to write cannot be None")

    def _download_file(self, task):
        response = self._download_request_data(task)
        self.output_file = response.content
        content_disposition = response.headers.get("Content-Disposition", "")

        filename = None
        match = re.search(r"filename\*=utf-8\'\'([^\s]+)", content_disposition)
        if match:

            filename = unquote(match.group(1).replace('"', ""))
        else:
            match = re.search(r'filename="([^"]+)"', content_disposition)
            if match:
                filename = match.group(1)
        self.output_file_name = filename
        self.output_file_type = (
            os.path.splitext(self.output_file_name)[1][1:]
            if self.output_file_name
            else None
        )

    def _download_request_data(self, task):
        data = {"v": self.VERSION}
        body = {"data": data}
        response = self.send_request("get", f"download/{task}", body)
        return response

    def _get_body(self):
        data = self._to_dict()
        for key in ["timeout_large", "timeout", "time_delay"]:
            data.pop(key, None)
        body = {"data": data, "params": {"v": self.VERSION}}

        return body

    def execute(self):
        self._validate_task_started()
        body = self._get_body()
        endpoint = self._endpoint_execute
        response = self.send_request("post", endpoint, body)
        self.result = response.json()

        # Update status and status_message after processing
        self.status = self.result.get("status")
        self.status_message = self.result.get("status_message")
        return self

    def _to_dict(self):
        props = {}
        attr_names = [
            "task",
            "tool",
            "files",
        ]
        for attr in attr_names:
            if not callable(getattr(self, attr)) and attr in attr_names:
                obj_value = getattr(self, attr)
                value = None
                if attr == "files":
                    # Convert File objects to dicts for JSON serialization
                    value = [
                        (
                            file.get_file_options()
                            if hasattr(file, "get_file_options")
                            else file
                        )
                        for file in (obj_value if isinstance(obj_value, list) else [])
                    ]
                props[attr] = value or obj_value
        props.update(self._params)
        return props

    def set_packaged_filename(self, filename):
        self.packaged_filename = filename
        return self

    def set_output_filename(self, filename):
        self.output_filename = filename
        return self

    def delete_file(self, file):
        self._validate_task_started()
        if file in self.files:
            body = {
                "data": {
                    "task": self.get_task_id(),
                    "server_filename": file.server_filename,
                    "v": self.VERSION,
                }
            }
            self.send_request(
                "delete", f"upload/{self.get_task_id()}/{file.server_filename}", body
            )
            self.files.remove(file)
        return self

    def check_values(self, value, allowed_values):
        if value not in allowed_values:
            if self.tool:
                raise ValueError(
                    f'Invalid {self.tool} value "{value}". Must be one of: {", ".join(allowed_values)}'
                )
            raise ValueError("No tool is set")
        return True

    def set_try_pdf_repair(self, try_pdf_repair):
        self.try_pdf_repair = try_pdf_repair
        return self

    def set_ignore_errors(self, ignore_errors):
        self.ignore_errors = ignore_errors
        return self

    def set_ignore_password(self, ignore_password):
        self.ignore_password = ignore_password
        return self

    def ignore_errors_alias(self, value):
        self.ignore_errors = value
        return self

    def ignore_password_alias(self, value):
        self.ignore_password = value
        return self

    def set_file_encryption(self, encrypt_key=None):
        if len(self.files) > 0:
            raise ValueError("Encrypt mode cannot be set after file upload")
        super().set_file_encryption(encrypt_key)
        return self

    def set_meta(self, key, value):
        self.meta[key] = value
        return self

    def set_custom_int(self, custom_int):
        self.custom_int = custom_int
        return self

    def set_custom_string(self, custom_string):
        self.custom_string = custom_string
        return self

    def list_tasks(self, tool=None, status=None, custom_int=None, page=None):
        self.check_values(status, self.STATUS_VALUES)
        data = {
            "tool": tool,
            "status": status,
            "custom_int": custom_int,
            "page": page,
            "v": self.VERSION,
            "secret_key": self.get_secret_key(),
        }
        body = {"data": data}
        response = self.send_request("post", "task", body, True)
        self.result = response.json()
        return self.result

    def set_webhook(self, webhook):
        self.webhook = webhook
        return self

    def _validate_file_extension(self, file_path):
        if not file_path.lower().endswith(".pdf"):
            raise ValueError("Only PDF files are supported")
        # Optionally: validate file content
        with open(file_path, "rb") as file_reader:
            if not file_reader.read(4) == b"%PDF":
                raise ValueError("File content is not a valid PDF")

    def _validate_task_started(self):
        if self.task is None:
            raise ValueError("Current task does not exist. You must start your task")

    def _set_remaining_credits(self, remaining_credits):
        self.remaining_credits = remaining_credits

    def _set_remaining_files(self, remaining_files):
        self.remaining_files = remaining_files

    def _set_remaining_pages(self, remaining_pages):
        self.remaining_pages = remaining_pages

    @staticmethod
    def get_value_or_default(value, default=None):
        return value if value is not None else default


class ProcessTask(Task):
    """A task class for processing files using the ilovepdf API."""
