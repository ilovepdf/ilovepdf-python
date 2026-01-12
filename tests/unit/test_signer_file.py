"""Unit tests for the SignerFile class in ilovepdf.sign."""

import pytest

from ilovepdf.exceptions import MissingPayloadFieldError
from ilovepdf.sign import Element, SignerFile

from .base_test import AbstractUnitTaskElementTest
from .samples_utils import FileSamples


# pylint: disable=protected-access
class TestSignerFile(AbstractUnitTaskElementTest):
    """Unit tests for the SignerFile class."""

    _task_class = SignerFile

    def test_set_defaults(self, my_task):
        """Test that default values are set correctly."""
        SignerFile._DEFAULT_PAYLOAD = {
            "server_filename": None,
            "elements": [],
        }
        assert my_task.server_filename is None
        assert my_task.elements == []
        assert my_task._file is None

    def test_init_with_file(self):
        """Checks that the object is initialized correctly with a file."""
        file = FileSamples.file1
        signer_file = self._task_class(file)
        assert signer_file._file is file
        assert signer_file.file is file

        signer_file.add_element()

        payload = signer_file._to_payload()
        assert payload["elements"] == [Element()._to_payload()]

    def test_set_server_filename(self, my_task):
        """Test setting the server_filename property."""
        my_task.server_filename = "server_filename"
        assert my_task.server_filename == "server_filename"

    def test_set_server_filename_invalid(self, my_task):
        """
        Test invalid values for server_filename raise errors.
        Covers:
        - Empty string, None, non-string (int) and list.
        """
        with pytest.raises(
            ValueError, match="server_filename: value must not be an empty"
        ):
            my_task.server_filename = ""
        with pytest.raises(TypeError, match="value must be a string"):
            my_task.server_filename = None
        with pytest.raises(TypeError, match="value must be a string"):
            my_task.server_filename = 1234
        with pytest.raises(TypeError):
            my_task.server_filename = []

    def test_add_elements(self, my_task):
        """Test adding elements to the SignerFile."""
        assert my_task.elements == []

        element = my_task.add_element()
        assert isinstance(element, Element)
        assert my_task.elements[-1] == element
        assert my_task.elements == [element]

        other_element = Element()
        added_element = my_task.add_element(other_element)
        assert added_element is other_element
        assert my_task.elements[-1] == other_element

        assert my_task.elements == [element, other_element]

    def test_add_element_max_elements(self, my_task):
        """Test that adding more than the maximum allowed elements raises an error."""
        max_elements = 1000
        for _ in range(max_elements):
            my_task.add_element()
        assert len(my_task.elements) == max_elements

        with pytest.raises(ValueError, match="Maximum number of elements reached"):
            my_task.add_element()

    def test_add_element_error(self, my_task):
        """Test that adding an invalid element raises an error."""
        with pytest.raises(TypeError):
            my_task.add_element("invalid_element")

    def test_missing_required_fields_raises(self, my_task):
        """Test that MissingPayloadFieldError is raised when required fields are
        missing."""
        with pytest.raises(MissingPayloadFieldError) as excinfo:
            my_task._to_payload()
        missing = excinfo.value.missing_fields
        assert missing == ["server_filename", "elements"]
