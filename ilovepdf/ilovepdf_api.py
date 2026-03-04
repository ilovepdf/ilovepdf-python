"""Module for interacting with the iLovePDF API, including authentication,
file encryption, and request handling.

This module provides the Ilovepdf class for managing API keys, tokens,
file encryption, and sending requests to the iLovePDF API endpoints.
"""

import json
import logging
import os
import pprint
import time
from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

import jwt
import requests
from dotenv import find_dotenv, load_dotenv
from requests.exceptions import JSONDecodeError

from ilovepdf.exceptions import (
    AuthException,
    DownloadException,
    ProcessException,
    SignatureException,
    StartException,
    TaskException,
    UploadException,
)

load_dotenv(find_dotenv())

# Constants
JWT_ALGORITHM = "HS256"
TOKEN_EXPIRE_SECONDS = 3600
TOKEN_CACHE_BUFFER_SECONDS = 120
DEFAULT_TIME_DELAY_SECONDS = 5400
DEFAULT_TIMEOUT_SECONDS = int(os.getenv("DEFAULT_TIMEOUT_SECONDS", "60"))
API_VERSION = "v1"
START_SERVER_URL = os.getenv("START_SERVER_URL", "https://api.ilovepdf.com")
API_HOST = os.getenv("API_HOST", "api.ilovepdf.com")
LIBRARY_VERSION = "python.0.0.1"

# HTTP Status Codes
HTTP_OK = 200
HTTP_CREATED = 201
HTTP_BAD_REQUEST = 400
HTTP_UNAUTHORIZED = 401
HTTP_FORBIDDEN = 403
HTTP_TOO_MANY_REQUESTS = 429
HTTP_INTERNAL_SERVER_ERROR = 500

# Endpoints requiring large timeout
LARGE_TIMEOUT_ENDPOINTS = ["process", "upload"]


def _setup_logging(loglevel, logfile=None) -> logging.Logger:
    """Configure and return logger for this module.

    Returns:
        logging.Logger: Configured logger instance.
    """

    params: dict[str, Any] = {
        "level": loglevel,
        "format": "%(asctime)s %(levelname)s %(name)s: %(message)s",
    }

    if logfile:
        params.update({"filemode": "a", "filename": logfile, "force": True})

    logging.basicConfig(**params)
    logging.getLogger("urllib3").setLevel(loglevel)
    logger = logging.getLogger(__name__)
    logger.setLevel(loglevel)
    if loglevel == "DEBUG":
        logger.debug("DEBUG mode activated!")
    return logger


env_loglevel = os.getenv("PYTHONLOGLEVEL", "INFO").upper()
env_logfile = os.getenv("PYTHONLOGFILE")
_logger = _setup_logging(env_loglevel, env_logfile)


@dataclass
class AuthManager:
    """Handles authentication and token management for iLovePDF API.

    Attributes:
        secret_key (str): API secret key for authentication.
        public_key (str): API public key for authentication.
        token_cache (tuple[str, int] | None): Cached token and expiration.
        token (str | None): Current JWT token.
    """

    secret_key: str
    public_key: str
    token_cache: tuple[str, int] | None = None
    token: str | None = None


@dataclass
class ServerConfig:
    """Stores server configuration and timeout settings for iLovePDF API.

    Attributes:
        worker_server (str | None): Worker server URL for task processing.
        time_delay (int): Time delay in seconds. Default is 5400.
        timeout (int): Request timeout in seconds. Default is 10.
        timeout_large (int | None): Timeout for large operations.
    """

    worker_server: str | None = None
    time_delay: int = DEFAULT_TIME_DELAY_SECONDS
    timeout: int = DEFAULT_TIMEOUT_SECONDS
    timeout_large: int | None = None


@dataclass
class EncryptionConfig:
    """Manages file encryption settings for iLovePDF API.

    Attributes:
        encrypted (bool): Whether file encryption is enabled.
        encrypt_key (str | None): Encryption key for file operations.
    """

    encrypted: bool = False
    encrypt_key: str | None = None


class RequestBuilder:
    """Builds and prepares HTTP requests for the iLovePDF API.

    This class encapsulates the logic for constructing URLs, headers,
    timeouts, and parameters for API requests.
    """

    def __init__(
        self,
        server_config: ServerConfig,
        auth_manager: AuthManager,
        get_token_callback: Callable[[], str],
        start_server: str,
    ) -> None:
        """Initialize RequestBuilder.

        Args:
            server_config (ServerConfig): Server configuration.
            auth_manager (AuthManager): Authentication manager.
            get_token_callback (Callable): Callback to get authentication
                token.
            start_server (str): Start server URL.
        """
        self.server_config = server_config
        self.auth_manager = auth_manager
        self.get_token = get_token_callback
        self.start_server = start_server

    def build_url(self, endpoint: str, start: bool) -> str:
        """Build the full URL for the API request.

        Args:
            endpoint (str): API endpoint path.
            start (bool): Whether to use start server or worker server.

        Returns:
            str: Complete URL for the request.
        """
        server = self.start_server
        if not start and self.server_config.worker_server is not None:
            server = self.server_config.worker_server
        return f"{server}/{API_VERSION}/{endpoint}"

    def build_timeout(self, endpoint: str) -> int:
        """Determine the appropriate timeout for the request.

        Args:
            endpoint (str): API endpoint path.

        Returns:
            int: Timeout in seconds.
        """
        is_large_endpoint = endpoint in LARGE_TIMEOUT_ENDPOINTS or (
            endpoint.startswith("download/")
        )

        if is_large_endpoint and self.server_config.timeout_large:
            return self.server_config.timeout_large
        return self.server_config.timeout

    def build_headers(self, endpoint: str) -> dict[str, str]:
        """Build headers for the API request.

        Args:
            endpoint (str): API endpoint path.

        Returns:
            dict[str, str]: Request headers.
        """
        if endpoint == "auth":
            return {}

        return {
            "Authorization": f"Bearer {self.get_token()}",
            "Accept": "application/json",
        }

    def prepare_params(
        self,
        params: dict[str, Any] | None,
        headers: dict[str, str],
        endpoint: str,
    ) -> dict[str, Any]:
        """Prepare and normalize request parameters.

        Args:
            params (dict[str, Any] | None): Original parameters.
            headers (dict[str, str]): Request headers.
            endpoint (str): API endpoint path.

        Returns:
            dict[str, Any]: Prepared request parameters.
        """
        params = dict(params or {})
        params.setdefault("headers", headers)

        # Only add data dict if not a start endpoint
        # (GET requests don't need empty data)
        if not endpoint.startswith("start/"):
            params.setdefault("data", {})

        # Special handling for process endpoint
        if endpoint == "process":
            if "Accept" in params["headers"]:
                del params["headers"]["Accept"]
            if "files" in params["data"]:
                params["headers"]["Content-Type"] = "application/json"
                params["data"] = json.dumps(params["data"])
        if endpoint == "signature":
            params["headers"]["Accept"] = "application/json"
            if "data" in params:
                params["json"] = params["data"]
                del params["data"]
        return params


class ResponseHandler:
    """Handles parsing and validation of API responses.

    This class encapsulates the logic for processing API responses,
    including JSON parsing and error detection.
    """

    @staticmethod
    def parse_json(response: requests.Response) -> dict[str, Any]:
        """Parse JSON from response body.

        Args:
            response (requests.Response): The HTTP response.

        Returns:
            dict[str, Any]: Parsed JSON or error dict if parsing fails.
        """
        try:
            return response.json()
        except JSONDecodeError:
            return {
                "error": "Failed to parse JSON response",
                "raw_response": response.text or "Empty response",
            }

    @staticmethod
    def is_success(response: requests.Response) -> bool:
        """Check if response indicates success.

        Args:
            response (requests.Response): The HTTP response.

        Returns:
            bool: True if status code indicates success.
        """
        return response.status_code in (HTTP_OK, HTTP_CREATED)


class ErrorRouter:
    """Routes errors to appropriate exception handlers.

    This class encapsulates error handling logic, routing different
    error types to their respective handlers based on endpoint and
    status code.
    """

    def __init__(self) -> None:
        """Initialize ErrorRouter."""
        self.endpoint_handlers: dict[str, Callable[[Any, int], None]] = {
            "upload": self._handle_upload_response,
            "process": self._handle_process_response,
        }

    def route(
        self, endpoint: str, response_body: dict[str, Any], response_code: int
    ) -> None:
        """Route error handling based on endpoint and status code.

        Args:
            endpoint (str): API endpoint path.
            response_body (dict[str, Any]): Response body.
            response_code (int): HTTP status code.

        Raises:
            UploadException: For upload errors.
            ProcessException: For process errors.
            DownloadException: For download errors.
            StartException: For start errors.
            TaskException: For task-related errors.
            SignatureException: For signature-related errors.
        """
        # Exact endpoint handlers
        if endpoint in self.endpoint_handlers:
            self.endpoint_handlers[endpoint](response_body, response_code)
            return

        # Prefix-based handlers
        if endpoint.startswith("download"):
            self._handle_download_response(response_body, response_code)
            return

        if endpoint.startswith("start"):
            self._handle_start_response(response_body, response_code)
            return

        # Status code handlers
        if response_code == HTTP_TOO_MANY_REQUESTS:
            raise ProcessException("Too Many Requests")

        if response_code == HTTP_BAD_REQUEST:
            self._handle_bad_request(endpoint, response_body, response_code)
            return

        # Generic error handler
        self._handle_generic_error(response_body, response_code)

    @staticmethod
    def _handle_upload_response(
        response_body: dict[str, Any] | str, response_code: int
    ) -> None:
        """Handle upload error responses.

        Args:
            response_body (dict[str, Any] | str): Response body.
            response_code (int): HTTP status code.

        Raises:
            UploadException: Always raises with error details.
        """
        if isinstance(response_body, str):
            raise UploadException("Upload error", response_body, response_code)
        raise UploadException(
            response_body.get("error", {}).get("message", "Upload error"),
            response_body,
            response_code,
        )

    @staticmethod
    def _handle_process_response(
        response_body: dict[str, Any], response_code: int
    ) -> None:
        """Handle process error responses.

        Args:
            response_body (dict[str, Any]): Response body.
            response_code (int): HTTP status code.

        Raises:
            ProcessException: Always raises with error details.
        """
        raise ProcessException(
            response_body.get("error", {}).get("message", "Process error"),
            response_body,
            response_code,
        )

    @staticmethod
    def _handle_download_response(
        response_body: dict[str, Any], response_code: int
    ) -> None:
        """Handle download error responses.

        Args:
            response_body (dict[str, Any]): Response body.
            response_code (int): HTTP status code.

        Raises:
            DownloadException: Always raises with error details.
        """
        raise DownloadException(
            response_body.get("error", {}).get("message", "Download error"),
            response_body,
            response_code,
        )

    @staticmethod
    def _handle_start_response(
        response_body: dict[str, Any], response_code: int
    ) -> None:
        """Handle start error responses.

        Args:
            response_body (dict[str, Any]): Response body.
            response_code (int): HTTP status code.

        Raises:
            StartException: Always raises with error details.
        """
        error = response_body.get("error", {})
        if error.get("type"):
            raise StartException(
                error.get("message", "Start error"),
                response_body,
                response_code,
            )
        raise StartException("Bad Request", response_body, response_code)

    @staticmethod
    def _handle_bad_request(
        endpoint: str, response_body: dict[str, Any], response_code: int
    ) -> None:
        """Handle bad request (400) error responses.

        Args:
            endpoint (str): API endpoint path.
            response_body (dict[str, Any]): Response body.
            response_code (int): HTTP status code.

        Raises:
            TaskException: For task-related errors.
            SignatureException: For signature-related errors.
            ProcessException: For other bad request errors.
        """

        _logger.debug(
            "\nBad request error:\n%s",
            pprint.pformat(response_body, indent=4),
        )

        if "task" in endpoint:
            raise TaskException("Invalid task id", response_body, response_code)

        if "signature" in endpoint:
            error = response_body.get("error", {})
            raise SignatureException(
                error.get("type", "Signature error"),
                response_body,
                response_code,
            )

        error = response_body.get("error", {})
        if error.get("type"):
            raise ProcessException(error.get("message", "Bad Request"))
        raise ProcessException("Bad Request")

    @staticmethod
    def _handle_generic_error(
        response_body: dict[str, Any], response_code: int
    ) -> None:
        """Handle generic error responses.

        Args:
            response_body (dict[str, Any]): Response body.
            response_code (int): HTTP status code.

        Raises:
            ProcessException: Always raises with error details.
        """
        error = response_body.get("error", {})
        if error.get("message"):
            msg = f"HTTP {response_code}: {error.get('message')}"
            raise ProcessException(msg, response_body, response_code)
        raise ProcessException(
            f"HTTP {response_code}: Bad Request", response_body, response_code
        )


class Ilovepdf:
    """
    Class for interacting with the iLovePDF API.

    This class manages API keys, authentication tokens, file encryption,
    and sending requests to iLovePDF API endpoints.

    Args:
        public_key (str, optional): API public key. If not provided,
            uses ILOVEPDF_PUBLIC_KEY env variable.
        secret_key (str, optional): API secret key. If not provided,
            uses ILOVEPDF_SECRET_KEY env variable.

    Raises:
        ValueError: If public_key or secret_key are empty or invalid.

    Example:
        ilovepdf = Ilovepdf(
            public_key="your_public_key",
            secret_key="your_secret_key"
        )
    """

    VERSION = LIBRARY_VERSION
    _start_server = START_SERVER_URL
    _api_version = API_VERSION

    def __init__(
        self, public_key: str | None = None, secret_key: str | None = None
    ) -> None:
        super().__init__()
        if public_key is None:
            public_key = os.getenv("ILOVEPDF_PUBLIC_KEY")
        if secret_key is None:
            secret_key = os.getenv("ILOVEPDF_SECRET_KEY")

        self._validate_api_key(public_key, "public_key")
        self._validate_api_key(secret_key, "secret_key")

        # Type checker: validated keys are guaranteed to be str at this point
        self.auth = AuthManager(
            secret_key=secret_key,  # type: ignore
            public_key=public_key,  # type: ignore
        )
        self.server = ServerConfig()
        self.encryption = EncryptionConfig()
        self.info = None

        # Initialize request and error handling components
        self._request_builder = RequestBuilder(
            self.server, self.auth, self.get_token, self.get_start_server()
        )
        self._response_handler = ResponseHandler()
        self._error_router = ErrorRouter()

    @staticmethod
    def _validate_api_key(key: str | None, key_name: str) -> None:
        """Validate that an API key is a non-empty string.

        Args:
            key (str | None): The API key to validate.
            key_name (str): Name of the key for error messages.

        Raises:
            ValueError: If the key is None, not a string, or empty.
        """
        if not key or not isinstance(key, str) or key.strip() == "":
            raise ValueError(
                f"A non-empty {key_name} string is required for IlovePDF "
                f"(argument or ILOVEPDF_{key_name.upper()} env variable)."
            )

    @property
    def api_version(self) -> str:
        """Get the API version.

        Returns:
            str: The current API version. Default is "v1".
        """
        return self._api_version

    @classmethod
    def set_api_version(cls, api_version: str) -> None:
        """Set the API version.

        Args:
            api_version (str): The API version to use.
        """
        cls._api_version = api_version

    def set_api_keys(self, public_key: str, secret_key: str) -> None:
        """Set the API keys.

        Args:
            public_key (str): The API public key.
            secret_key (str): The API secret key.
        """
        self.auth.public_key = public_key
        self.auth.secret_key = secret_key

    def get_secret_key(self) -> str:
        """Get the secret key.

        Returns:
            str: The API secret key. Default is empty string.
        """
        return self.auth.secret_key or ""

    def get_public_key(self) -> str:
        """Get the public key.

        Returns:
            str: The API public key. Default is empty string.
        """
        return self.auth.public_key or ""

    def get_token(self) -> str:
        """Get the JWT token for API authentication.

        Retrieves a cached token if still valid, otherwise requests a new
        token from the API. Falls back to local JWT generation if API fails.

        Returns:
            str: Valid JWT authentication token.

        Raises:
            ValueError: If secret_key is not a non-empty string.
            AuthException: If authentication with the API fails.
        """
        self._validate_api_key(self.auth.secret_key, "secret_key")

        # Check cached token
        if self._is_token_cache_valid():
            # Type checker: cache is guaranteed to be non-None here
            token, _ = self.auth.token_cache  # type: ignore
            self.auth.token = token
            return token

        # Try to get token from API
        try:
            token = self._request_token_from_api()
            self._cache_token(token)
            return token
        except requests.RequestException as exc:
            _logger.warning(
                "Failed to get token from API (%s), "
                "falling back to local JWT generation.",
                exc,
            )

        # Fallback: generate local JWT
        token = self._generate_local_jwt()
        self._cache_token(token)
        return token

    def _is_token_cache_valid(self) -> bool:
        """Check if the cached token is still valid.

        Returns:
            bool: True if cached token exists and hasn't expired.
        """
        if self.auth.token_cache is None:
            return False
        _, exp = self.auth.token_cache
        current_time = int(datetime.now(timezone.utc).timestamp())
        return exp - TOKEN_CACHE_BUFFER_SECONDS > current_time

    def _request_token_from_api(self) -> str:
        """Request a new token from the iLovePDF API.

        Returns:
            str: JWT token from the API.

        Raises:
            AuthException: If authentication fails or response is invalid.
        """
        url = f"{self.get_start_server()}/{API_VERSION}/auth"
        headers = {"Accept": "application/json"}
        data = {"public_key": self.get_public_key()}

        response = requests.request(
            "POST",
            url,
            json=data,
            headers=headers,
            timeout=self.server.timeout,
        )

        if response.status_code in (HTTP_OK, HTTP_CREATED):
            response_json = response.json()
            token = response_json.get("token")
            if token:
                return token
            raise KeyError("Token not found in response")

        # Handle error responses
        response_json = self._response_handler.parse_json(response)

        if response.status_code == HTTP_UNAUTHORIZED:
            raise AuthException(
                response_json.get("error", {}).get("type", "Auth error"),
                response_json,
                response.status_code,
            )

        if response.status_code in (
            HTTP_BAD_REQUEST,
            HTTP_FORBIDDEN,
            HTTP_INTERNAL_SERVER_ERROR,
        ):
            raise AuthException(
                response_json.get("error", {}).get("type", "Auth error"),
                response_json,
                response.status_code,
            )

        raise AuthException(
            response_json.get("error", {}).get("message", "Auth failed")
        )

    def _generate_local_jwt(self) -> str:
        """Generate a JWT token locally.

        Returns:
            str: Locally generated JWT token.
        """
        now = int(datetime.now(timezone.utc).timestamp())
        delay = self.server.time_delay
        exp = now + TOKEN_EXPIRE_SECONDS + delay

        payload = {
            "iss": API_HOST,
            "aud": API_HOST,
            "iat": now - delay,
            "nbf": now - delay,
            "exp": exp,
            "jti": self.auth.public_key,
        }

        if self.is_file_encryption():
            payload["file_encryption_key"] = self.get_encrypt_key()  # type: ignore

        token = jwt.encode(payload, self.auth.secret_key, algorithm=JWT_ALGORITHM)
        return token

    def _cache_token(self, token: str) -> None:
        """Cache a token with its expiration time.

        Args:
            token (str): The JWT token to cache.
        """
        now = int(datetime.now(timezone.utc).timestamp())
        exp = now + TOKEN_EXPIRE_SECONDS + self.server.time_delay
        self.auth.token_cache = (token, exp)
        self.auth.token = token

    def get_jwt(self) -> str:
        """Get the JWT token.

        Returns:
            str: JWT authentication token.
        """
        if self.auth.token:
            return self.auth.token

        current_time = int(time.time())
        token_dict: dict[str, int | str | None] = {
            "iss": API_HOST,
            "aud": API_HOST,
            "iat": current_time - self.server.time_delay,
            "nbf": current_time - self.server.time_delay,
            "exp": current_time + TOKEN_EXPIRE_SECONDS + self.server.time_delay,
            "jti": self.get_public_key(),
        }

        if self.is_file_encryption():
            token_dict["file_encryption_key"] = self.get_encrypt_key()

        self.auth.token = jwt.encode(
            token_dict,
            self.get_secret_key(),
            algorithm=self.get_token_algorithm(),
        )
        return self.auth.token

    @staticmethod
    def get_token_algorithm() -> str:
        """Get the JWT token algorithm.

        Returns:
            str: The algorithm used for JWT encoding. Default is "HS256".
        """
        return JWT_ALGORITHM

    @classmethod
    def set_start_server(cls, server: str) -> None:
        """Set the start server URL.

        Args:
            server (str): The base URL for the API server.
        """
        cls._start_server = server

    @classmethod
    def get_start_server(cls) -> str:
        """Get the start server URL.

        Returns:
            str: The base URL for the API server.
        """
        return cls._start_server

    def get_worker_server(self) -> str | None:
        """Get the worker server URL.

        Returns:
            str | None: Worker server URL if set, otherwise None.
        """
        return self.server.worker_server

    def set_worker_server(self, worker_server: str | None) -> None:
        """Set the worker server URL.

        Args:
            worker_server (str | None): The worker server URL for task
                processing, or None to clear it.
        """
        self.server.worker_server = worker_server

    def is_file_encryption(self) -> bool:
        """Check if file encryption is enabled.

        Returns:
            bool: True if file encryption is enabled, False otherwise.
        """
        return self.encryption.encrypted

    def get_encrypt_key(self) -> str | None:
        """Get the encryption key.

        Returns:
            str | None: The encryption key if set, otherwise None.
        """
        return self.encryption.encrypt_key

    def send_request(
        self,
        method: str,
        endpoint: str,
        params: dict[str, Any] | None = None,
        start: bool = False,
    ) -> requests.Response:
        """Send a request to the iLovePDF API.

        Args:
            method (str): HTTP method (GET, POST, etc.).
            endpoint (str): API endpoint path.
            params (dict[str, Any] | None): Request parameters.
            start (bool): Whether this is a start server request.

        Returns:
            requests.Response: The HTTP response object.

        Raises:
            ConnectionError: If connection to server fails.
            AuthException: If authentication fails (401).
            UploadException: If upload operation fails.
            ProcessException: If processing operation fails.
            DownloadException: If download operation fails.
            StartException: If start operation fails.
        """
        # Update request builder with current start server
        self._request_builder.start_server = self.get_start_server()

        url = self._request_builder.build_url(endpoint, start)
        timeout = self._request_builder.build_timeout(endpoint)
        headers = self._request_builder.build_headers(endpoint)
        params = self._request_builder.prepare_params(params, headers, endpoint)

        _logger.debug(
            "\nREQUEST:\n  method: %s\n  url: %s\n  params:\n%s",
            method.upper(),
            url,
            pprint.pformat(params, indent=4),
        )

        response = self._execute_request(method, url, timeout, params)
        return self._handle_response(response, endpoint)

    def _execute_request(
        self, method: str, url: str, timeout: int, params: dict[str, Any]
    ) -> requests.Response:
        """Execute the HTTP request.

        Args:
            method (str): HTTP method.
            url (str): Complete URL.
            timeout (int): Request timeout.
            params (dict[str, Any]): Request parameters.

        Returns:
            requests.Response: The HTTP response.

        Raises:
            ConnectionError: If connection fails.
            ProcessException: If request fails for other reasons.
        """
        try:
            return requests.request(method.upper(), url, timeout=timeout, **params)
        except requests.ConnectionError as exc:
            raise ConnectionError(f"Connection error: {exc}") from exc
        except requests.RequestException as exc:
            raise ProcessException(f"HTTP request failed: {exc}") from exc

    def _handle_response(
        self, response: requests.Response, endpoint: str
    ) -> requests.Response:
        """Handle and validate the API response.

        Args:
            response (requests.Response): The HTTP response.
            endpoint (str): API endpoint path.

        Returns:
            requests.Response: The validated response.

        Raises:
            AuthException: If authentication fails.
            UploadException: If upload fails.
            ProcessException: If processing fails.
            DownloadException: If download fails.
            StartException: If start operation fails.
        """
        response_code: int = response.status_code or 0

        _logger.debug(
            "RESPONSE: status=%s, content_type=%s",
            response_code,
            response.headers.get("Content-Type", "unknown"),
        )

        if self._response_handler.is_success(response):
            return response

        # Only parse JSON for error responses
        response_body = self._response_handler.parse_json(response)

        # Handle error responses
        if response_code == HTTP_UNAUTHORIZED:
            raise AuthException(
                response_body.get("name", "Auth error"),
                response_body,
                response_code,
            )

        # Route to specific error handlers
        self._error_router.route(endpoint, response_body, response_code)

        return response

    def get_status(self, server: str, task_id: str) -> dict[str, Any]:
        """Get the status of a task.

        Args:
            server (str): The worker server URL.
            task_id (str): The task identifier.

        Returns:
            dict[str, Any]: Task status information.
        """
        original_worker_server = self.get_worker_server()
        self.set_worker_server(server)
        response = self.send_request("get", f"task/{task_id}")
        self.set_worker_server(original_worker_server)
        return response.json()

    def get_updated_info(self) -> dict[str, Any]:
        """Get updated information about the account.

        Returns:
            dict[str, Any]: Account information including remaining credits.
        """
        data = {"v": self.VERSION}
        body = {"data": data}
        response = self.send_request("get", "info", body)
        self.info = response.json()
        return self.info

    def get_info(self) -> dict[str, Any]:
        """Get information about the account.

        Returns:
            dict[str, Any]: Account information.
        """
        return self.get_updated_info()

    def get_remaining_files(self) -> int:
        """Get the remaining number of files that can be processed.

        Returns:
            int: Number of remaining files.
        """
        if self.info is None:
            self.get_updated_info()
        return self.info.get("remaining_files", 0) if self.info else 0
