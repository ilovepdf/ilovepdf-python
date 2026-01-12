"""Test the authentication API."""

import pytest
import requests

from ilovepdf.exceptions import AuthException
from ilovepdf.ilovepdf_api import Ilovepdf

from .base_task_integration_test import BaseTaskIntegrationTest


class AuthTest(Ilovepdf):
    """Class for testing authentication."""

    def start(self):
        """Start the authentication test."""


# pylint: disable=bad-option-value
# pylint: disable=broad-exception-raised
class TestAuthAPI(BaseTaskIntegrationTest):
    """Test the authentication API."""

    task_class = AuthTest

    def test_configure_credentials(self):
        """Check that credentials are configured correctly."""
        assert self.task.get_token() == self.task.auth.token

    def test_get_token_and_reuse(self):
        """
        Check that a token is obtained and reused in the session using the real API.
        """
        instance = self.task
        token1 = instance.get_token()
        assert isinstance(token1, str)
        assert instance.auth.token == token1
        token2 = instance.get_token()
        assert token1 == token2

    def test_invalid_credentials_raise_auth_exception(self):
        """
        Check that invalid credentials raise an authentication error from the real API.
        """
        invalid_instance = self.task_class(public_key="invalid", secret_key="invalid")
        with pytest.raises(AuthException) as auth_error:
            invalid_instance.get_token()
        exc = auth_error.value
        assert any(
            s in str(exc.args) for s in ["ServerError", "Auth error", "Invalid"]
        ), "Expected authentication error message not found."

    def test_connection_error(self):
        """Simulate a connection error and check exception handling."""

        def fake_request(*args, **kwargs):
            raise Exception("Simulated connection error")

        # Patch requests.request temporarily
        original_request = requests.request
        requests.request = fake_request
        try:
            instance = self.task_class(
                public_key=self.public_key, secret_key=self.secret_key
            )
            with pytest.raises(Exception) as connection_error:
                instance.get_token()
            assert "Simulated connection error" in str(connection_error.value)
        finally:
            requests.request = original_request
