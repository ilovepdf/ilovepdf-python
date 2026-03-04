"""Helper functions and abstract base classes for the ilovepdf-python library.

Provides base classes and utilities for serializing and validating payloads
for API requests.
"""

from collections.abc import Sequence
from typing import Any

from ilovepdf.exceptions import MissingPayloadFieldError

Payload = dict[str, Any]


class AbstractTaskElement:
    """Base class for task elements that can be serialized to an API payload.

    This class provides mechanisms for defining default payloads, serializing
    attributes, and validating required fields for API requests.

    Attributes:
        REQUIRED_FIELDS (list[str]): List of required field names that must be present
            and non-empty in the payload. Subclasses should override this attribute
            to specify their own required fields.

    Example:
        class ExampleElement(AbstractTaskElement):
            _DEFAULT_PAYLOAD = {
                "attr1": "default_value_1",
                "attr2": "default_value_2",
            }
            REQUIRED_FIELDS = ["attr1", "attr2"]

            @property
            def attr1(self) -> str:
                return self._get_attr("attr1")

            @attr1.setter
            def attr1(self, value: str):
                self._set_attr("attr1", value)

            # Usage:
            element = ExampleElement()
            element.attr1 = "custom_value"
            payload = element._to_payload()
    """

    _DEFAULT_PAYLOAD: Payload = {}
    _LIST_ATTRS: Sequence[str] = ("files", "elements")
    REQUIRED_FIELDS: list[str] = []

    def __init__(self) -> None:
        self._payload: Payload = self._get_default_payload()

        for key in self._LIST_ATTRS:
            if key in self._payload:
                self._payload[key] = list(self._payload[key])

    def _get_attr(self, key: str) -> Any:
        """
        Gets the value of an attribute from the payload.

        Only allows keys defined in _DEFAULT_PAYLOAD.

        Args:
            key (str): The attribute key.

        Returns:
            Any: The value of the attribute.

        Raises:
            KeyError: If the key is not defined in _DEFAULT_PAYLOAD.
        """
        if key not in self._get_default_payload():
            raise KeyError(
                f"Invalid attribute key: '{key}'. "
                f"Allowed keys: {list(self._get_default_payload().keys())}"
            )
        return self._payload[key]

    def _set_attr(self, key: str, value: Any) -> None:
        """Sets the value of an attribute in the payload.

        Only allows keys defined in _DEFAULT_PAYLOAD.

        If value is None, restores the default value from _DEFAULT_PAYLOAD.

        Args:
            key (str): The attribute key.
            value (Any): The value to set.

        Raises:
            KeyError: If the key is not defined in _DEFAULT_PAYLOAD.
        """
        if key not in self._get_default_payload():
            raise KeyError(
                f"Invalid attribute key: '{key}'. "
                f"Allowed keys: {list(self._get_default_payload().keys())}"
            )
        if value is None:
            self._payload[key] = self._get_default_payload()[key]
        else:
            self._payload[key] = value

    @classmethod
    def _get_default_payload(cls):
        """Get the default payload by merging all _DEFAULT_PAYLOAD from class hierarchy.

        Returns:
            Payload: Merged dictionary of all _DEFAULT_PAYLOAD from parent classes.
        """
        result = {}
        for base_cls in reversed(cls.__mro__):
            if (
                hasattr(base_cls, "_DEFAULT_PAYLOAD")
                and "_DEFAULT_PAYLOAD" in base_cls.__dict__
            ):
                result = result | base_cls.__dict__["_DEFAULT_PAYLOAD"]
        return result

    @classmethod
    def _get_required_fields(cls):
        """Get required fields by merging all REQUIRED_FIELDS from class hierarchy.

        Returns:
            list[str]: Merged list of all REQUIRED_FIELDS from parent classes,
                with duplicates removed while preserving order.
        """
        result = []
        for base_cls in reversed(cls.__mro__):
            if (
                hasattr(base_cls, "REQUIRED_FIELDS")
                and "REQUIRED_FIELDS" in base_cls.__dict__
            ):
                result = result + base_cls.__dict__["REQUIRED_FIELDS"]
        # Remove duplicates while preserving order
        return list(dict.fromkeys(result))

    def _to_payload(self) -> Payload:
        """Returns a dict ready for the API.

        Recursively serializes items that expose `_to_payload()`.
        Runs `_validate_payload()` before returning.

        Returns:
            Payload: The serialized payload dictionary.

        Example:
            element = ExampleElement()
            payload = element._to_payload()
        """
        payload = self._serialize_lists(self._payload.copy())
        self._validate_payload(payload)
        return payload

    def _validate_payload(self, payload: Payload) -> None:
        """Validates the payload.

        Args:
            payload (Payload): The payload to validate.

        Raises:
            ValueError: If the payload is empty or required fields are missing.
        """
        if not payload:
            raise ValueError("Payload cannot be empty.")

        # Validate required fields if defined
        missing_fields = [
            field
            for field in self._get_required_fields()
            if field not in payload or payload[field] in (None, "", [], {})
        ]
        if missing_fields:
            raise MissingPayloadFieldError(missing_fields)

    @classmethod
    def _serialize_lists(cls, data: Payload) -> Payload:
        """Serializes list attributes in the payload by calling _to_payload.

        Args:
            data (Payload): The payload dictionary.

        Returns:
            Payload: The payload with serialized lists.
        """
        for key in cls._LIST_ATTRS:
            if key not in data:
                continue
            items = data[key]
            if not isinstance(items, Sequence) or isinstance(items, str | bytes):
                continue
            serialized = []
            for item in items:
                to_pl = getattr(item, "_to_payload", None)
                serialized.append(to_pl() if callable(to_pl) else item)
            data[key] = serialized
        return data
