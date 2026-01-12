"""Unit tests for the RotateTask class in the ilovepdf module."""

import pytest

from ilovepdf import RotateTask
from ilovepdf.exceptions import InvalidChoiceError
from ilovepdf.rotate_task import ROTATE_ANGLE_OPTIONS, RotateFile

from .base_test import AbstractUnitFileTest, AbstractUnitTaskTest


# pylint: disable=protected-access
class TestRotateFile(AbstractUnitFileTest):
    """Unit tests for the RotateFile class."""

    _task_class = RotateFile

    def test_initialization_sets_default_values(self, my_task):
        """
        Test that the RotateFile class initializes with default values.
        """
        assert ROTATE_ANGLE_OPTIONS == {0, 90, 180, 270}
        assert my_task._DEFAULT_PAYLOAD == {
            "server_filename": None,
            "filename": None,
            "rotate": 0,
        }
        assert my_task.rotate == 0

    @pytest.mark.parametrize("angle", ROTATE_ANGLE_OPTIONS)
    def test_set_rotation_valid_angles(self, my_task, angle):
        """
        Test that the RotateFile class sets the rotation angle correctly for valid
        angles.
        """
        my_task.rotate = angle
        assert my_task.rotate == angle

    @pytest.mark.parametrize("invalid_angle", [-90, 45, 100, 360, None, "90"])
    def test_set_rotation_invalid_angles(self, my_task, invalid_angle):
        """
        Test that the RotateFile class raises an InvalidChoiceError when setting
        an invalid rotation angle.
        """
        with pytest.raises(InvalidChoiceError):
            my_task.rotate = invalid_angle

    @pytest.mark.parametrize("angle", ROTATE_ANGLE_OPTIONS)
    def test_to_payload_includes_rotate_angle(self, my_task, angle):
        """
        Test that _to_payload includes the rotate angle.
        """
        my_task.rotate = angle
        payload = my_task._to_payload()
        assert "rotate" in payload
        assert payload["rotate"] == angle


class TestRotateTask(AbstractUnitTaskTest):
    """Unit tests for the RotateTask class."""

    _task_class = RotateTask
    _task_tool = "rotate"

    def test_init(self):
        """Test RotateTask initialization and inheritance."""
