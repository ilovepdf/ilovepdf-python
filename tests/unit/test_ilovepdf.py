"""Unit tests for the Ilovepdf class in the ilovepdf module."""

import jwt
import pytest
from pytest_mock import MockerFixture

from ilovepdf.exceptions.auth_exception import AuthException
from ilovepdf.ilovepdf_api import Ilovepdf

VALID_SECRET_KEY = "a" * 32

ERROR_500 = {
    "error": {
        "type": "ServerError",
        "message": "Something on our end went wrong, probably we are not catching "
        "some exception we should catch! We are logging this and we will "
        "fix it.",
        "code": "500",
    }
}


class TestIlovePdfAuth:
    """Unit tests for the IlovePdfAuth class in the ilovepdf module."""

    def test_set_api_keys_stores_credentials(self):
        ilovepdf = Ilovepdf(
            public_key="dummy_public_key", secret_key="dummy_secret_key"
        )
        ilovepdf.set_api_keys("my_public_key", "my_secret_key")
        assert ilovepdf.get_public_key() == "my_public_key"
        assert ilovepdf.get_secret_key() == "my_secret_key"

    def test_get_token_returns_local_jwt(self):
        """Check that get_token returns a self-signed JWT with correct claims."""
        ilovepdf = Ilovepdf(public_key="public_key", secret_key=VALID_SECRET_KEY)
        token = ilovepdf.get_token()

        assert isinstance(token, str)
        payload = jwt.decode(token, VALID_SECRET_KEY, algorithms=["HS256"])
        assert payload["iss"] == ""
        assert payload["aud"] == ""
        assert payload["jti"] == "public_key"

    def test_send_request_auth_endpoint_raises_auth_exception(
        self, mocker: MockerFixture
    ):
        """Check that the /auth endpoint still raises AuthException on 401."""
        mock_request = mocker.patch("requests.request")
        mock_response = mocker.MagicMock()
        mock_response.status_code = 401
        mock_response.json.return_value = ERROR_500
        mock_request.return_value = mock_response

        ilovepdf = Ilovepdf(public_key="bad", secret_key="dummy_secret")
        with pytest.raises(AuthException):
            ilovepdf.send_request(
                "get", "auth", {"json": {"public_key": "bad"}}, start=True
            )

    def test_get_token_does_not_call_auth_endpoint(self, mocker: MockerFixture):
        """Check that token generation is local and does not need the network."""
        mock_request = mocker.patch(
            "requests.request", side_effect=RuntimeError("network should not be used")
        )
        ilovepdf = Ilovepdf(public_key="public_key", secret_key=VALID_SECRET_KEY)
        token = ilovepdf.get_token()

        assert isinstance(token, str)
        mock_request.assert_not_called()

    def test_token_is_cached_and_reused(self, mocker: MockerFixture):
        """Check that the locally generated token is cached and reused."""
        mock_request = mocker.patch(
            "requests.request", side_effect=RuntimeError("network should not be used")
        )

        ilovepdf = Ilovepdf(public_key="public", secret_key=VALID_SECRET_KEY)
        token1 = ilovepdf.get_token()
        token2 = ilovepdf.get_token()
        assert token1 == token2
        mock_request.assert_not_called()

    def test_send_request_refreshes_token_on_signature_auth_error(
        self, mocker: MockerFixture
    ):
        """Check that a 401 'Signature verification failed' is retried once."""
        mock_token = mocker.patch.object(
            Ilovepdf, "get_token", side_effect=["token1", "token2"]
        )
        auth_error_body = {
            "name": "Unauthorized",
            "message": "Signature verification failed",
            "code": 0,
            "status": 401,
        }
        success_body = {"server_filename": "abc123.pdf"}
        responses = [
            mocker.MagicMock(
                status_code=401,
                json=mocker.MagicMock(return_value=auth_error_body),
                headers={"Content-Type": "application/json"},
            ),
            mocker.MagicMock(
                status_code=200,
                json=mocker.MagicMock(return_value=success_body),
                headers={"Content-Type": "application/json"},
            ),
        ]
        mock_request = mocker.patch("requests.request", side_effect=responses)

        ilovepdf = Ilovepdf(public_key="public", secret_key=VALID_SECRET_KEY)
        response = ilovepdf.send_request("post", "upload", {"files": {}, "data": {}})

        assert response.status_code == 200
        assert response.json() == success_body
        assert mock_token.call_count == 2
        assert mock_request.call_count == 2

    def test_send_request_does_not_retry_non_signature_auth_error(
        self, mocker: MockerFixture
    ):
        """Check that unrelated 401 errors are not retried."""
        mock_token = mocker.patch.object(Ilovepdf, "get_token", return_value="token1")
        auth_error_body = {
            "name": "Unauthorized",
            "message": "Invalid credentials",
            "code": 0,
            "status": 401,
        }
        mock_request = mocker.patch(
            "requests.request",
            return_value=mocker.MagicMock(
                status_code=401,
                json=mocker.MagicMock(return_value=auth_error_body),
                headers={"Content-Type": "application/json"},
            ),
        )

        ilovepdf = Ilovepdf(public_key="public", secret_key="secret")
        with pytest.raises(AuthException):
            ilovepdf.send_request("post", "upload", {"files": {}, "data": {}})

        assert mock_token.call_count == 1
        assert mock_request.call_count == 1
