"""Unit tests for the Signer class in the ilovepdf.sign module."""

import pytest

from ilovepdf.exceptions import InvalidChoiceError, MissingPayloadFieldError
from ilovepdf.file import File
from ilovepdf.sign import Signer, SignerFile

from .base_test import AbstractUnitTaskElementTest


# pylint: disable=protected-access
class TestSigner(AbstractUnitTaskElementTest):
    """Unit tests for the Signer class."""

    _task_class = Signer

    def test_set_defaults(self, my_task):
        """Test default values of Signer."""
        assert my_task.type == "signer"
        assert Signer._DEFAULT_PAYLOAD == {
            "name": None,
            "email": None,
            "phone": None,
            "files": [],
            "type": "signer",
            "access_code": None,
            "force_signature_type": None,
        }
        assert Signer.REQUIRED_FIELDS == ["name", "email", "files"]

    def test_initialization_sets_name_and_email(self):
        """
        Test that the Signer is initialized with the correct name and email.
        """
        signer = Signer(name="Test User", email="test.user@example.com")
        assert signer.name == "Test User"
        assert signer.email == "test.user@example.com"

    @pytest.mark.parametrize("type_signer", ["signer", "validator", "viewer"])
    def test_set_type(self, my_task, type_signer):
        """Test setting valid types."""
        my_task.type = type_signer
        assert my_task.type == type_signer

    def test_set_type_invalid(self, my_task):
        """Test setting an invalid type raises error."""
        with pytest.raises(InvalidChoiceError):
            my_task.type = "invalid_type"

    def test_set_access_code(self, my_task):
        """Test setting access code."""
        my_task.access_code = "123456"
        assert my_task.access_code == "123456"

    def test_set_force_signature_type(self, my_task):
        """Test setting force_signature_type."""
        my_task.force_signature_type = "some_type"
        assert my_task.force_signature_type == "some_type"

    def test_add_signer_file_error(self, my_task):
        """Test error when adding invalid signer file."""
        with pytest.raises(TypeError):
            my_task.add_signer_file("invalid_file")

    def test_add_signer_file(self, my_task):
        """Test adding elements to the SignerFile."""
        assert my_task.files == []

        signer_file = SignerFile()

        element = my_task.add_signer_file(signer_file)
        assert isinstance(element, SignerFile)
        assert element is signer_file
        assert my_task.files[-1] == element
        assert my_task.files == [element]

        other_element = SignerFile()
        added_element = my_task.add_signer_file(other_element)
        assert isinstance(added_element, SignerFile)
        assert added_element is other_element
        assert my_task.files[-1] == other_element

        assert my_task.files == [element, other_element]

    def test_add_file(self, my_task):
        """Test adding files to the SignerFile."""
        assert my_task.files == []

        file = File("server_filename", "filename")
        sign_file = my_task.add_file(file)
        assert isinstance(sign_file, SignerFile)
        assert my_task.files[-1] == sign_file
        assert my_task.files == [sign_file]

    def test_missing_required_fields_raises(self, my_task):
        """Test that MissingPayloadFieldError is raised when required fields are
        missing."""
        my_task._payload.update({"name": None, "email": None, "files": None})

        with pytest.raises(MissingPayloadFieldError) as excinfo:
            my_task._to_payload()
        missing = excinfo.value.missing_fields
        assert missing == ["name", "email", "files"]
