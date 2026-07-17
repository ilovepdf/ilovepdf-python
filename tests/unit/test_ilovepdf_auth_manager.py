"""Unit tests for the IlovepdfAuthManager class in the ilovepdf module."""

import jwt
import pytest
from pytest_mock import MockerFixture

from ilovepdf.exceptions.auth_exception import AuthException
from ilovepdf.ilovepdf_api import Ilovepdf

VALID_SECRET_KEY = "dummy_secret_key_that_is_long_enough_for_hs256"
INVALID_SECRET_KEY = "bad_secret_key_that_is_long_enough_for_hs256"


class IlovepdfAuthManager:
    """
    Class that manages authentication and credential handling for iLovePDF,
    using the Ilovepdf class internally.
    """

    def __init__(self, public_key: str | None = None, secret_key: str | None = None):
        # Always provide a non-empty secret_key for testing purposes if not given
        public_key = public_key or "dummy_key"
        secret_key = secret_key or VALID_SECRET_KEY
        self._ilovepdf = Ilovepdf(public_key=public_key, secret_key=secret_key)

    def set_credentials(
        self,
        public_key: str | None = None,
        secret_key: str | None = None,
    ):
        self._ilovepdf.set_api_keys(public_key, secret_key)  # type: ignore

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

    def test_get_token(self, mocker: MockerFixture):
        """Check that get_token returns a self-signed JWT."""
        mock_request = mocker.patch(
            "requests.request", side_effect=RuntimeError("network should not be used")
        )

        manager = IlovepdfAuthManager(public_key="pub_key")
        token = manager.get_token()

        assert isinstance(token, str)
        payload = jwt.decode(token, VALID_SECRET_KEY, algorithms=["HS256"])
        assert payload["jti"] == "pub_key"
        assert manager.token_actual() == token
        mock_request.assert_not_called()

    def test_token_is_reusable(self, mocker: MockerFixture):
        """Check that the locally generated token is cached and reused."""
        mock_request = mocker.patch(
            "requests.request", side_effect=RuntimeError("network should not be used")
        )

        manager = IlovepdfAuthManager(public_key="pub_key")
        token1 = manager.get_token()
        token2 = manager.get_token()
        assert token1 == token2
        mock_request.assert_not_called()

    def test_invalid_credentials_raise_exception(self, mocker: MockerFixture):
        """Check that invalid credentials fail on a real API call."""
        mock_request = mocker.patch("requests.request")
        mock_response = mocker.MagicMock()
        mock_response.status_code = 401
        mock_response.json.return_value = {
            "error": {
                "type": "AuthError",
                "message": "Invalid credentials",
                "code": "401",
            }
        }
        mock_request.return_value = mock_response

        manager = IlovepdfAuthManager(public_key="bad", secret_key=INVALID_SECRET_KEY)
        with pytest.raises(AuthException):
            manager._ilovepdf.send_request("get", "start/compress", start=True)

    def test_connection_error_does_not_break_token_generation(
        self, mocker: MockerFixture
    ):
        """Check that token generation works even when the network is down."""
        mock_request = mocker.patch(
            "requests.request", side_effect=Exception("Connection error")
        )
        manager = IlovepdfAuthManager(public_key="public")
        token = manager.get_token()
        assert isinstance(token, str)
        mock_request.assert_not_called()
