"""Unit tests for the ProtectTask class in the ilovepdf module.

This module contains unit tests for the ProtectTask class, which is part of the
ilovepdf module.
The tests cover initialization, password setting, dictionary representation,
and file addition validation.
"""

import pytest

from ilovepdf import ProtectTask

from .base_test import AbstractUnitTaskTest


# pylint: disable=protected-access
class TestProtectTask(AbstractUnitTaskTest):
    """Unit tests for the ProtectTask class."""

    _task_class = ProtectTask
    _task_tool = "protect"

    def test_default_values(self, my_task):
        """Ensure default values are set correctly."""
        assert my_task._DEFAULT_PAYLOAD == {
            "password": None,
        }

    def test_password_is_not_accessible(self, my_task):
        """
        Ensure that the password is not accessible via the property.
        """
        with pytest.raises(NotImplementedError):
            _ = my_task.password

    def test_set_password(self, my_task):
        """Test setting a valid password."""
        my_task.password = "secret"
        assert my_task._payload["password"] == "secret"

    def test_missing_required_fields_raises(self, my_task):
        """ "Test that MissingPayloadFieldError is raised when required fields
        are missing."""
        self.assert_missing_required_fields_raise(my_task, ["password"])

    def test_set_password_raises_on_empty_or_non_string(self, my_task):
        """
        Ensure set_password raises ValueError if password is empty or not a
        string.
        """
        with pytest.raises(ValueError):
            my_task.password = ""
        with pytest.raises(TypeError):
            my_task.password = None
        with pytest.raises(TypeError):
            my_task.password = 12345
