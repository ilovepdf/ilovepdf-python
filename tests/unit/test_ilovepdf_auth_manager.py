"""Unit tests for the IlovepdfAuthManager class in the ilovepdf module."""

from typing import Optional
from unittest.mock import MagicMock, patch

import pytest

from ilovepdf.exceptions.auth_exception import AuthException
from ilovepdf.ilovepdf_api import Ilovepdf


class IlovepdfAuthManager:
    """
    Class that manages authentication and credential handling for iLovePDF,
    using the Ilovepdf class internally.
    """

    def __init__(
        self, public_key: Optional[str] = None, secret_key: Optional[str] = None
    ):
        # Always provide a non-empty secret_key for testing purposes if not given
        if secret_key is None:
            secret_key = "dummy_secret"
        self._ilovepdf = Ilovepdf(public_key=public_key, secret_key=secret_key)

    def set_credentials(
        self,
        public_key: Optional[str] = None,
        secret_key: Optional[str] = None,
    ):
        self._ilovepdf.set_api_keys(public_key, secret_key)

    def get_token(self):
        return self._ilovepdf.get_token()

    def token_actual(self):
        return self._ilovepdf.auth.token

    def get_public_key(self):
        return self._ilovepdf.get_public_key()

    def get_secret_key(self):
        return self._ilovepdf.get_secret_key()


class TestIlovepdfAuthManager:
    """
    Test the IlovepdfAuthManager class.
    """

    def test_configure_credentials(self):
        manager = IlovepdfAuthManager(secret_key="dummy_secret")
        manager.set_credentials("pub_key", "sec_key")
        assert manager.get_public_key() == "pub_key"
        assert manager.get_secret_key() == "sec_key"

    @patch("requests.request")
    def test_get_token(self, mock_request):
        mock_response = MagicMock()
        mock_response.json.return_value = {"token": "token_cache"}
        mock_response.status_code = 200
        mock_request.return_value = mock_response

        manager = IlovepdfAuthManager(public_key="pub_key", secret_key="dummy_secret")
        token = manager.get_token()
        assert token == "token_cache"
        assert manager.token_actual() == "token_cache"

    @patch("requests.request")
    def test_token_is_reusable(self, mock_request):
        mock_response = MagicMock()
        mock_response.json.return_value = {"token": "token_cache"}
        mock_response.status_code = 200
        mock_request.return_value = mock_response

        manager = IlovepdfAuthManager(public_key="pub_key", secret_key="dummy_secret")
        token1 = manager.get_token()
        token2 = manager.get_token()
        assert token1 == token2 == "token_cache"
        mock_request.assert_called_once()

    @patch("requests.request")
    def test_invalid_credentials_raise_exception(self, mock_request):
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.json.return_value = {
            "error": {
                "type": "AuthError",
                "message": "Invalid credentials",
                "code": "401",
            }
        }
        mock_request.return_value = mock_response

        manager = IlovepdfAuthManager(public_key="bad", secret_key="bad")
        with pytest.raises(AuthException):
            manager.get_token()

    @patch("requests.request")
    def test_connection_error_raises_exception(self, mock_request):
        mock_request.side_effect = Exception("Connection error")
        manager = IlovepdfAuthManager(public_key="public", secret_key="secret")
        with pytest.raises(Exception) as excinfo:
            manager.get_token()
        assert "Connection error" in str(excinfo.value)
