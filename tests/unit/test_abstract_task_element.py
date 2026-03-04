"""Unit tests for required fields and attribute validation in
AbstractTaskElement.

Tests:
- REQUIRED_FIELDS and MissingPayloadFieldError handling
- Restoring default values when setting None
- KeyError for invalid attribute keys
"""

import pytest

from ilovepdf.abstract_task_element import AbstractTaskElement
from ilovepdf.exceptions.payload_field_errors import MissingPayloadFieldError

from .base_test import AbstractUnitTaskElementTest


class DummyElement(AbstractTaskElement):
    """Dummy element for testing required fields and attribute logic."""

    _DEFAULT_PAYLOAD = {
        "name": "John",
        "address": "123 Main St",
        "optional": "something",
    }
    REQUIRED_FIELDS = ["name", "address"]


class TestAbstractTaskElement(AbstractUnitTaskElementTest):
    """
    Test suite for verifying required fields and attribute validation logic
    in AbstractTaskElement.

    This class contains unit tests to ensure:
    - All required fields are present in the payload, and appropriate exceptions are
        raised when missing.
    - Setting an attribute to None restores its default value.
    - KeyError is raised when accessing or setting invalid attribute keys.
    """

    _task_class = DummyElement

    def test_to_payload_with_all_required_fields(self, my_task):
        """Payload includes all required fields; no exception is raised."""
        payload = my_task._to_payload()
        assert payload["name"] == "John"
        assert payload["address"] == "123 Main St"

    @pytest.mark.parametrize(
        "missing_field, value",
        [
            ("name", ""),
            ("address", ""),
            ("name", None),
            ("address", None),
        ],
    )
    def test_to_payload_missing_single_required_field(
        self, my_task, missing_field, value
    ):
        """
        Raises MissingPayloadFieldError if a required field is empty or None.
        Covers edge cases: empty string and None produce MissingPayloadFieldError.
        """
        my_task._payload[missing_field] = value
        with pytest.raises(MissingPayloadFieldError) as excinfo:
            my_task._to_payload()
        assert missing_field in excinfo.value.missing_fields

    def test_to_payload_missing_multiple_required_fields(self, my_task):
        """Only fields that remain empty are reported as missing."""
        my_task._set_attr("name", "")
        my_task._set_attr("address", None)  # Restores default, not missing
        with pytest.raises(MissingPayloadFieldError) as excinfo:
            my_task._to_payload()
        missing = excinfo.value.missing_fields
        assert "name" in missing
        assert "address" not in missing

    def test_to_payload_required_field_empty_list_and_dict(self, my_task):
        """Empty list or dict in required field triggers MissingPayloadFieldError."""
        my_task._set_attr("name", [])
        my_task._set_attr("address", {})
        with pytest.raises(MissingPayloadFieldError) as excinfo:
            my_task._to_payload()
        missing = excinfo.value.missing_fields
        assert "name" in missing
        assert "address" in missing

    def test_set_attr_none_restores_default(self):
        """Setting an attribute to None restores its default value in the payload."""

        class DummyElementWithDefault(AbstractTaskElement):
            """Dummy element with default values for testing None assignment."""

            _DEFAULT_PAYLOAD = {"attr1": 1000, "attr2": None}
            REQUIRED_FIELDS = ["attr1"]

            @property
            def attr1(self):
                """get attr1"""
                return self._get_attr("attr1")

            @attr1.setter
            def attr1(self, value):
                """set attr1"""
                self._set_attr("attr1", value)

        element = DummyElementWithDefault()
        element.attr1 = None  # Should restore default 1000
        payload = element._to_payload()
        assert payload["attr1"] == 1000

    def test_set_attr_invalid_key_raises_keyerror(self):
        """_set_attr raises KeyError for an invalid attribute key."""

        class DummyElement(AbstractTaskElement):
            """class DummyElement"""

            _DEFAULT_PAYLOAD = {"foo": 1}
            REQUIRED_FIELDS = []

        elem = DummyElement()
        with pytest.raises(KeyError) as excinfo:
            elem._set_attr("bar", 123)
        assert "Invalid attribute key: 'bar'" in str(excinfo.value)

    def test_get_attr_invalid_key_raises_keyerror(self):
        """_get_attr raises KeyError for an invalid attribute key."""

        class DummyElement(AbstractTaskElement):
            """class DummyElement"""

            _DEFAULT_PAYLOAD = {"foo": 1}

        elem = DummyElement()
        with pytest.raises(KeyError) as excinfo:
            elem._get_attr("bar")
        assert "Invalid attribute key: 'bar'" in str(excinfo.value)

    def test_missing_required_fields_raises(self, my_task):
        """Test that MissingPayloadFieldError is raised when required fields are
        missing."""
        my_task._payload["name"] = None
        my_task._payload["address"] = None

        self.assert_missing_required_fields_raise(my_task, ["name", "address"])

    def test_get_default_payload(self, my_task):
        """Verify _get_default_payload returns the element's default payload."""
        assert my_task._get_default_payload() == {
            "name": "John",
            "address": "123 Main St",
            "optional": "something",
        }


class TestInheritanceDefaultPayloadAndRequiredFields:
    """Verify merging of default payloads and required fields across inheritance."""

    def test_default_payload_merge_hierarchy(self):
        """Should merge _DEFAULT_PAYLOAD from all levels in hierarchy."""

        class Base(AbstractTaskElement):
            """Base class."""

            _DEFAULT_PAYLOAD = {"a": 1}

        class Child(Base):
            """Child class."""

            _DEFAULT_PAYLOAD = {"b": 2}

        class GrandChild(Child):
            """Grandchild class."""

            _DEFAULT_PAYLOAD = {"c": 3}

        assert Base._get_default_payload() == {"a": 1}
        assert Child._get_default_payload() == {"a": 1, "b": 2}
        assert GrandChild._get_default_payload() == {"a": 1, "b": 2, "c": 3}

    def test_default_payload_override(self):
        """Child should override parent's payload values."""

        class Base(AbstractTaskElement):
            """Base class."""

            _DEFAULT_PAYLOAD = {"x": "old", "y": 2}

        class Child(Base):
            """Child class."""

            _DEFAULT_PAYLOAD = {"x": "new", "z": 3}

        assert Child._get_default_payload() == {"x": "new", "y": 2, "z": 3}

    def test_required_fields_merge_hierarchy(self):
        """Should merge REQUIRED_FIELDS from all levels without duplicates."""

        class Base(AbstractTaskElement):
            """Base required fields."""

            REQUIRED_FIELDS = ["a", "b"]

        class Child(Base):
            """Child required fields, with duplicates."""

            REQUIRED_FIELDS = ["b", "c"]  # b is duplicate

        class GrandChild(Child):
            """GrandChild required fields, with duplicates."""

            REQUIRED_FIELDS = ["c", "d"]  # c is duplicate

        assert Base._get_required_fields() == ["a", "b"]
        assert Child._get_required_fields() == ["a", "b", "c"]
        assert GrandChild._get_required_fields() == ["a", "b", "c", "d"]

    def test_combined_payload_and_fields(self):
        """Both methods should work together in complex hierarchy."""

        class Base(AbstractTaskElement):
            """Base class with default payload and required fields."""

            _DEFAULT_PAYLOAD = {"a": 1}
            REQUIRED_FIELDS = ["a"]

        class Child(Base):
            """Child class with its own default payload and required fields."""

            _DEFAULT_PAYLOAD = {"b": 2}
            REQUIRED_FIELDS = ["b"]

        assert Child._get_default_payload() == {"a": 1, "b": 2}
        assert Child._get_required_fields() == ["a", "b"]
        # Works as instance method too
        assert Child()._get_default_payload() == {"a": 1, "b": 2}
