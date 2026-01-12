"""Unit tests for the SignTask class in the ilovepdf module."""

from unittest.mock import MagicMock

import pytest

from ilovepdf import SignTask


class DummySigner:  # pylint: disable=too-few-public-methods
    """Dummy signer class for testing."""

    def __init__(self, name="Test User", email="test@example.com"):
        self.name = name
        self.email = email
        self.elements = []

    def add_elements(self, file, element):
        self.elements.append((file, element))
        return self


class TestSignTask:
    """Unit tests for the SignTask class."""

    @pytest.fixture
    def sign_task(self):
        """Fixture that creates a SignTask instance for testing."""
        task = SignTask(
            public_key="dummy_public", secret_key="dummy_secret", make_start=False
        )
        return task

    def test_initialization_sets_default_values(self, sign_task):
        """
        Ensure SignTask is initialized with default values.
        """
        assert sign_task.tool == "sign"
        assert sign_task.lock_order is None
        assert sign_task.expiration_days is None
        assert sign_task.language is None
        assert sign_task.subject_signer is None
        assert sign_task.message_signer is None
        assert sign_task.signers == []
        assert sign_task.uuid_visible is None
        assert sign_task.reminders is None
        assert sign_task.verify_enabled is None
        assert sign_task.brand_name is None
        assert sign_task.brand_logo is None
        # pylint: disable=protected-access
        assert sign_task._endpoint_execute == "signature"
        # pylint: enable=protected-access

    def test_add_receiver_adds_signer(self, sign_task):
        signer = DummySigner()
        sign_task.add_receiver(signer)
        assert len(sign_task.signers) == 1
        assert sign_task.signers[0] == signer

    def test_setters_and_getters(self, sign_task):
        # Test verify_enabled
        sign_task.set_verify_signature_verification(True)
        assert sign_task.get_verify_signature_verification() is True

        # Test message_signer
        sign_task.set_message("Please sign this document")
        assert sign_task.get_message() == "Please sign this document"

        # Test subject_signer
        sign_task.set_subject("Signature Request")
        assert sign_task.get_subject() == "Signature Request"

        # Test reminders
        sign_task.set_reminders(3)
        assert sign_task.get_reminders() == 3

        # Test lock_order
        sign_task.set_lock_order(2)
        assert sign_task.get_lock_order() == 2

    def test_chaining_setters_returns_self(self, sign_task):
        # Ensure setters return self for chaining
        result = (
            sign_task.set_message("msg")
            .set_subject("subj")
            .set_reminders(5)
            .set_lock_order(1)
        )
        assert result is sign_task
        assert sign_task.get_message() == "msg"
        assert sign_task.get_subject() == "subj"
        assert sign_task.get_reminders() == 5
        assert sign_task.get_lock_order() == 1

    def test_execute_result_structure(self, sign_task):
        # Simulate the response structure returned by the integration test
        fake_response = {
            "about_to_expire_reminder": False,
            "completed_on": None,
            "created": "2021-10-18 14:03:43",
            "disable_notifications": None,
            "email": "email@email.com",
            "expires": "2022-02-15 15:00:00",
            "language": "en",
            "lock_order": False,
            "mode": "multiple",
            "name": "Guillem",
            "notes": None,
            "signer_reminder_days_cycle": 2,
            "signer_reminders": True,
            "subject_cc": None,
            "subject_signer": None,
            "timezone": None,
            "token_requester": "15928374asdf",
            "uuid": "18B06FDC-8643-447C-BAFB-9D3F8CA421B6",
            "uuid_visible": True,
            "verify_enabled": True,
            "expired": False,
            "expiring": False,
            "signers": [
                {
                    "uuid": "FCE3CAB9-2320-44C1-B18B-0F23BE2CF2FD",
                    "name": "name",
                    "email": "emailsigner@email.com",
                    "phone": None,
                    "type": "signer",
                    "token_requester": "1234asdf",
                    "status": "waiting",
                    "access_code": False,
                    "phone_access_code": False,
                    "force_signature_type": "all",
                    "notes": None,
                }
            ],
            "files": [{"filename": "sample.pdf", "pages": 2, "filesize": 22698}],
            "certified": True,
            "status": "draft",
        }

        # Mock the execute method to return an object with a .result attribute
        mock_execute = MagicMock()
        mock_execute.result = fake_response
        sign_task.execute = MagicMock(return_value=mock_execute)

        result = sign_task.execute().result

        # Validate the structure
        assert isinstance(result, dict)
        assert "status" in result
        assert "signers" in result and isinstance(result["signers"], list)
        assert "files" in result and isinstance(result["files"], list)
        assert "uuid" in result
        assert "created" in result
        assert "email" in result
        assert "name" in result
        signer = result["signers"][0]
        assert "uuid" in signer
        assert "name" in signer
        assert "email" in signer
        assert "status" in signer
        file_info = result["files"][0]
        assert "filename" in file_info
        assert "pages" in file_info
        assert "filesize" in file_info
