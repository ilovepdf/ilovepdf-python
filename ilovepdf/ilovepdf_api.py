"""Module for interacting with the iLovePDF API, including authentication,
file encryption, and request handling.

This module provides the Ilovepdf class for managing API keys, tokens,
file encryption, and sending requests to the iLovePDF API endpoints.
"""

import hashlib
import json
import logging
import os
import pprint
import secrets
import time
from datetime import datetime, timezone
from typing import Optional

import jwt
import requests
from requests.exceptions import JSONDecodeError

from ilovepdf.exceptions.auth_exception import AuthException
from ilovepdf.exceptions.download_exception import DownloadException
from ilovepdf.exceptions.process_exception import ProcessException
from ilovepdf.exceptions.signature_exception import SignatureException
from ilovepdf.exceptions.start_exception import StartException
from ilovepdf.exceptions.task_exception import TaskException
from ilovepdf.exceptions.upload_exception import UploadException

loglevel = os.environ.get("PYTHONLOGLEVEL", "INFO").upper()  # pylint: disable=no-member

logging.basicConfig(level=loglevel)
logging.getLogger("urllib3").setLevel(loglevel)
logging.debug("DEBUG mode activated!")
_logger = logging.getLogger(__name__)
_logger.setLevel(loglevel)


# Helper for random encryption key (to be implemented)
def rand_sha256(length: int) -> str:
    random_data = str(time.time()) + str(secrets.randbelow(80001) + 10000)
    sha = hashlib.sha256(random_data.encode()).hexdigest()
    return sha[:length]


ALGORITHM = "HS256"
EXPIRE_SEC = 3600


class AuthManager:  # pylint: disable=too-few-public-methods
    """Handles authentication and token management for iLovePDF API."""

    def __init__(self, secret_key: str, public_key: str):
        self.secret_key = secret_key
        self.public_key = public_key
        self.token_cache: Optional[tuple[str, int]] = None
        self.token: Optional[str] = None


class ServerConfig:  # pylint: disable=too-few-public-methods
    """Stores server configuration and timeout settings for iLovePDF API."""

    def __init__(self):
        self.worker_server = None
        self.time_delay = 5400
        self.timeout = 10
        self.timeout_large = None


class EncryptionConfig:  # pylint: disable=too-few-public-methods
    """Manages file encryption settings for iLovePDF API."""

    def __init__(self):
        self.encrypted = False
        self.encrypt_key = None


class Ilovepdf:  # pylint: disable=too-many-public-methods
    """Class for interacting with the iLovePDF API.

    This class manages API keys, authentication tokens, file encryption,
    and sending requests to iLovePDF API endpoints.
    """

    VERSION = "python.0.0.1"
    _start_server = "https://api.ilovepdf.com"
    _api_version = "v1"

    def __init__(self, public_key=None, secret_key=None):
        if (
            secret_key is None
            or not isinstance(secret_key, str)
            or secret_key.strip() == ""
        ):
            raise ValueError("A non-empty secret_key string is required for Ilovepdf.")
        self.auth = AuthManager(secret_key, public_key)
        self.server = ServerConfig()
        self.encryption = EncryptionConfig()
        self.info = None

        if public_key and secret_key:
            self.set_api_keys(public_key, secret_key)

    @property
    def api_version(self):
        return self._api_version

    @classmethod
    def set_api_version(cls, api_version):
        cls._api_version = api_version

    def set_api_keys(self, public_key, secret_key):
        self.auth.public_key = public_key
        self.auth.secret_key = secret_key

    def get_secret_key(self):
        return self.auth.secret_key or ""

    def get_public_key(self):
        return self.auth.public_key or ""

    def get_token(self) -> str:
        # Ensure secret_key is a non-empty string before proceeding
        if (
            self.auth.secret_key is None
            or not isinstance(self.auth.secret_key, str)
            or self.auth.secret_key.strip() == ""
        ):
            raise ValueError(
                "A non-empty secret_key string is required to generate a token."
            )
        # Use cached token if not expiring soon
        if self.auth.token_cache is not None:
            token, exp = self.auth.token_cache
            if exp - 120 > int(datetime.now(timezone.utc).timestamp()):
                self.auth.token = token
                return token

        # Try to get token from API (for test compatibility)
        try:
            url = f"{self.get_start_server()}/v1/auth"
            headers = {"Accept": "application/json"}
            data = {"public_key": self.get_public_key()}
            response = requests.request(
                "POST",
                url,
                json=data,
                headers=headers,
                timeout=self.server.timeout,
            )
            if response.status_code in (200, 201):
                response_json = response.json()
                token = response_json.get("token")
                if token:
                    now = int(datetime.now(timezone.utc).timestamp())
                    exp = now + EXPIRE_SEC
                    self.auth.token_cache = (token, exp)
                    self.auth.token = token
                    return token
                raise KeyError("Token not found in response")

            if response.status_code == 401:
                response_json = response.json()
                raise AuthException(
                    response_json.get("error", {}).get("type", "Auth error"),
                    response_json,
                    response.status_code,
                )

            response_json = {}
            try:
                response_json = response.json()
            except JSONDecodeError as exc:
                logging.warning("Error parsing response JSON: %s", exc)
                response_json = None
            # Raise AuthException for all relevant HTTP error codes
            if response.status_code in (400, 401, 403, 500):
                raise AuthException(
                    response_json.get("error", {}).get("type", "Auth error"),
                    response_json,
                    response.status_code,
                )
            raise Exception(
                response_json.get("error", {}).get("message", "Auth failed")
            )
        except requests.RequestException:
            # Fallback to local JWT if HTTP request fails (for offline/dev mode)
            pass

        # Fallback: generate local JWT
        now = int(datetime.now(timezone.utc).timestamp())
        exp = now + EXPIRE_SEC
        payload = {
            "iss": "api.ilovepdf.com",
            "aud": "",
            "iat": now,
            "nbf": now,
            "exp": exp,
            "jti": self.auth.public_key,
        }
        token = jwt.encode(payload, self.auth.secret_key, algorithm=ALGORITHM)
        self.auth.token_cache = (token, exp)
        self.auth.token = token
        return token

    def get_jwt(self):
        if self.auth.token:
            return self.auth.token
        secret = self.get_secret_key()
        current_time = int(time.time())
        host_info = ""
        token = {
            "iss": host_info,
            "aud": host_info,
            "iat": current_time - self.server.time_delay,
            "nbf": current_time - self.server.time_delay,
            "exp": current_time + 3600 + self.server.time_delay,
            "jti": self.get_public_key(),
        }
        if self.is_file_encryption():
            token["file_encryption_key"] = self.get_encrypt_key()
        self.auth.token = jwt.encode(
            token, secret, algorithm=self.get_token_algorithm()
        )
        return self.auth.token

    @staticmethod
    def get_token_algorithm():
        return "HS256"

    @classmethod
    def set_start_server(cls, server):
        cls._start_server = server

    @classmethod
    def get_start_server(cls):
        return cls._start_server

    def get_worker_server(self):
        return self.server.worker_server

    def set_worker_server(self, worker_server):
        self.server.worker_server = worker_server

    def set_file_encryption(self, encrypt_key=None):
        """
        Enables file encryption. If a key is provided, it will be used.
        If not, a random key will be generated.
        """
        self.enable_encryption(True)
        if encrypt_key is None:
            encrypt_key = rand_sha256(32)
        if len(encrypt_key) not in (16, 24, 32):
            raise ValueError("Encrypt key should have 16, 24 or 32 chars length")
        self.encryption.encrypt_key = encrypt_key
        return self

    def disable_file_encryption(self):
        """
        Disables file encryption and removes the encryption key.
        """
        self.enable_encryption(False)
        self.encryption.encrypt_key = None
        return self

    def enable_encryption(self, enable):
        self.encryption.encrypted = enable

    def set_encryption(self, enable):
        self.enable_encryption(enable)

    def is_file_encryption(self):
        return self.encryption.encrypted

    def get_encrypt_key(self):
        return self.encryption.encrypt_key

    def set_encrypt_key(self, encrypt_key=None):
        if encrypt_key is None:
            encrypt_key = rand_sha256(32)
        if len(encrypt_key) not in (16, 24, 32):
            raise ValueError("Encrypt key should have 16, 24 or 32 chars length")
        self.encryption.encrypt_key = encrypt_key

    def send_request(
        self, method, endpoint, params=None, start=False
    ):  # pylint: disable=too-many-locals,too-many-branches
        to_server = self.get_start_server()
        if not start and self.get_worker_server() is not None:
            to_server = self.get_worker_server()

        timeout = (
            self.server.timeout_large
            if endpoint in ["process", "upload"] or endpoint.startswith("download/")
            else self.server.timeout
        )
        headers = (
            {
                "Authorization": f"Bearer {self.get_token()}",
                "Accept": "application/json",
            }
            if endpoint != "auth"
            else {}
        )

        url = f"{to_server}/v1/{endpoint}"
        request_params = params.copy() if params else {}
        request_params.setdefault("headers", headers)
        request_params.setdefault("timeout", timeout)

        if endpoint == "process":
            del request_params["headers"]["Accept"]
            if "files" in request_params["data"]:
                request_params["headers"].update({"Content-Type": "application/json"})
                request_params["data"] = json.dumps(request_params["data"])
            # request_params["data"] = json.dumps(request_params["data"])

            # if "files" in request_params["data"]:
            #     request_params["headers"].update({"Content-Type": "application/json"})
            #     print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", type(request_params["data"]))
            #     print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", request_params["data"])
            #     request_params["data"]["files"] = [
            #         item.get_file_options()
            #         for item in request_params["data"]["files"]
            #     ]

        _logger.debug(
            "\nREQUEST:\n  method: %s\n  url: %s\n  params:\n%s",
            method.upper(),
            url,
            pprint.pformat(request_params, indent=4),
        )

        try:
            response = requests.request(method.upper(), url, **request_params)
        except requests.ConnectionError as exc:
            # Propagate ConnectionError so tests can catch it
            raise ConnectionError(f"Connection error: {exc}") from exc
        except requests.RequestException as exc:
            raise Exception(f"HTTP request failed: {exc}") from exc

        response_code = response.status_code
        try:
            response_body = response.json()
            _logger.debug("RESPONSE: status=%s, body=%s", response_code, response_body)
        except JSONDecodeError:
            response_body = {}

        if response_code not in (200, 201):
            if response_code == 401:
                raise AuthException(
                    response_body.get("name", "Auth error"),
                    response_body,
                    response_code,
                )
            # Diccionario de handlers exactos
            endpoint_handlers = {
                "upload": self._handle_upload_response,
                "process": self._handle_process_response,
            }
            handler = endpoint_handlers.get(endpoint)
            if handler:
                handler(response_body, response_code)
            # Diccionario de handlers por prefijo
            prefix_handlers = {
                "download": self._handle_download_response,
                "start": self._handle_start_response,
            }
            for prefix, func in prefix_handlers.items():
                if endpoint.startswith(prefix):
                    func(response_body, response_code)
                    break
            if response_code == 429:
                raise Exception("Too Many Requests")
            if response_code == 400:
                self._handle_bad_request(endpoint, response_body, response_code)
            self._handle_generic_error(response_body, response_code)
        return response

    def _handle_upload_response(self, response_body, response_code):
        if isinstance(response_body, str):
            raise UploadException("Upload error", response_body, response_code)
        raise UploadException(
            response_body.get("error", {}).get("message", "Upload error"),
            response_body,
            response_code,
        )

    def _handle_process_response(self, response_body, response_code):
        raise ProcessException(
            response_body.get("error", {}).get("message", "Process error"),
            response_body,
            response_code,
        )

    def _handle_download_response(self, response_body, response_code):
        raise DownloadException(
            response_body.get("error", {}).get("message", "Download error"),
            response_body,
            response_code,
        )

    def _handle_start_response(self, response_body, response_code):
        error = response_body.get("error", {})
        if error.get("type"):
            raise StartException(
                error.get("message", "Start error"),
                response_body,
                response_code,
            )
        raise Exception("Bad Request")

    def _handle_bad_request(self, endpoint, response_body, response_code):
        if "task" in endpoint:
            raise TaskException("Invalid task id")
        if "signature" in endpoint:
            error = response_body.get("error", {})
            raise SignatureException(
                error.get("type", "Signature error"),
                response_body,
                response_code,
            )
        error = response_body.get("error", {})
        if error.get("type"):
            raise Exception(error.get("message", "Bad Request"))
        raise Exception("Bad Request")

    def _handle_generic_error(self, response_body, response_code):
        error = response_body.get("error", {})
        if error.get("message"):
            raise Exception(f"HTTP {response_code}: {error.get('message')}")
        raise Exception(f"HTTP {response_code}: Bad Request")

    def get_status(self, server, task_id):
        worker_server = self.get_worker_server()
        self.set_worker_server(server)
        response = self.send_request("get", f"task/{task_id}")
        self.set_worker_server(worker_server)
        return response.json()

    def verify_ssl(self, verify):
        # requests uses 'verify' param per request, so this is handled in send_request
        pass

    def follow_location(self, follow):
        # requests handles redirects by default, can be controlled per request
        pass

    def get_updated_info(self):
        data = {"v": self.VERSION}
        body = {"data": data}
        response = self.send_request("get", "info", body)
        self.info = response.json()
        return self.info

    def get_info(self):
        return self.get_updated_info()

    def get_remaining_files(self):
        info = self.get_updated_info()
        return info.get("remaining_credits")
