"""Test the authentication API."""

import unittest

import requests

from ilovepdf.exceptions import AuthException
from ilovepdf.ilovepdf_api import Ilovepdf
from ilovepdf.task import Task

from .utils.base_ilovepdf_task_test import BaseIlovePdfTaskTest


class TestActivityAuthAPI(BaseIlovePdfTaskTest):
    """Test the authentication API."""

    task_class = Task
    sample_file_path = None

    def test_configure_credentials(self):
        """Check that credentials are configured correctly."""
        instance = Ilovepdf(public_key=self.public_key, secret_key=self.secret_key)
        self.assertEqual(instance.auth.public_key, self.public_key)
        self.assertEqual(instance.auth.secret_key, self.secret_key)

    def test_get_token_and_reuse(self):
        """Check that a token is obtained and reused in the session using the real API."""
        instance = Ilovepdf(public_key=self.public_key, secret_key=self.secret_key)
        token1 = instance.get_token()
        self.assertIsInstance(token1, str)
        self.assertEqual(instance.auth.token, token1)
        token2 = instance.get_token()
        self.assertEqual(token1, token2)

    def test_invalid_credentials_raise_auth_exception(self):
        """Check that invalid credentials raise an authentication error from the real API."""
        invalid_instance = Ilovepdf(public_key="invalid", secret_key="invalid")
        with self.assertRaises(AuthException) as auth_error:
            invalid_instance.get_token()
        exc = auth_error.exception
        self.assertTrue(
            any(s in str(exc.args) for s in ["ServerError", "Auth error", "Invalid"]),
            "Expected authentication error message not found.",
        )

    def test_connection_error(self):
        """Simulate a connection error and check exception handling."""

        def fake_request(*args, **kwargs):
            raise Exception("Simulated connection error")

        # Patch requests.request temporarily
        original_request = requests.request
        requests.request = fake_request
        try:
            instance = Ilovepdf(public_key=self.public_key, secret_key=self.secret_key)
            with self.assertRaises(Exception) as connection_error:
                instance.get_token()
            self.assertIn("Simulated connection error", str(connection_error.exception))
        finally:
            requests.request = original_request


if __name__ == "__main__":
    unittest.main()
