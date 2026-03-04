"""
Unit tests for EditPdfTask: test initialization, element addition, payload, and error
handling.
"""

import pytest

from ilovepdf import EditPdfTask
from ilovepdf.editpdf_task import (
    Element,
)

from .base_test import AbstractUnitTaskTest


class TestEditPdfTask(AbstractUnitTaskTest):
    """
    Unittest for EditPdfTask: validates task initialization, element addition, payload
    structure, and error handling for invalid input.
    """

    _task_class = EditPdfTask
    _task_tool = "editpdf"

    def test_initialization(self, my_task):
        """
        Ensure task initializes with proper empty default payload.
        """
        assert my_task._DEFAULT_PAYLOAD == {"elements": []}

    def test_add_elements(self, my_task):
        """
        Test adding elements to EditPdfTask and verify
        parent linkage and element list management.
        """
        assert my_task.elements == []

        element = my_task.add_element()
        assert element.parent is my_task
        assert element.parent is not None
        assert isinstance(element, Element)
        assert my_task.elements[-1] == element
        assert my_task.elements == [element]

        other_element = Element()
        added_element = my_task.add_element(other_element)
        assert added_element is other_element
        assert my_task.elements[-1] == other_element

        assert my_task.elements == [element, other_element]

    def add_generic_element(self, task, element_type=None):
        """
        Helper for adding a configured Element to the EditPdfTask.
        Args:
            task (EditPdfTask): Target task.
            element_type (str, optional): Type for the element.
        Returns:
            Element: The newly added Element.
        """
        element = Element()
        element.pages = "1-3"
        element.zindex = 1
        element.dimensions = {"w": 100.0, "h": 50.0}
        element.coordinates = {"x": 100.0, "y": 50.0}
        if element_type:
            element.type = element_type

        task.add_element(element)
        return element

    def test_add_element_error(self, my_task):
        """
        Verify that adding a non-Element object raises a TypeError.
        """
        with pytest.raises(TypeError):
            my_task.add_element("invalid_element")

    def test_payload_structure(self, my_task):
        """
        Check payload generation for EditPdfTask including internal element payloads.
        """

        element = self.add_generic_element(my_task, element_type="text")
        element.text = "Sample Text"

        payload = my_task._to_payload()
        assert payload["elements"] == [element._to_payload()]
        # assert "files" not in payload
