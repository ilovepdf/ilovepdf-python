"""Abstract base class for unit tests of ILovePDF task classes.

Classes:
    AbstractUnitTaskElementTest: Base class for unit tests of ILovePDF task element
        classes.
    AbstractUnitFileTest: Base class for unit tests of ILovePDF file task element
        classes.
    AbstractUnitTaskTest: Base class for unit tests of ILovePDF task classes.

Provides a reusable fixture and structure for testing ILovePDF tasks.
"""

from abc import ABC

import pytest

from ilovepdf import File, Task
from ilovepdf.abstract_task_element import AbstractTaskElement
from ilovepdf.exceptions import MissingPayloadFieldError
from ilovepdf.file import BaseFile


class AbstractUnitTaskElementTest(ABC):
    """
    Base class for unit tests of ILovePDF task element classes.

    Subclasses must set `_task_class` to a concrete subclass of AbstractTaskElement.

    Attributes:
        _task_class (Type): Concrete task element class to test.
        _check_payload_keys (bool): If True, check expected payload keys.
        _check_unexpected_keys (bool): If True, check for unexpected payload keys.

    Example:
        class TestAnyUnitTaskElement(AbstractUnitTaskElementTest):
            _task_class = AnyTaskElement  # Replace with a concrete task element class
                that inherits from AbstractTaskElement

            def test_initialization_sets_default_values(self, my_task):
                # At least one test method must be defined in each test class.
                # Replace this with meaningful assertions for your task element.
                assert my_task is not None

            def test_missing_required_fields_raises(self, my_task):
                \"\"\"Test that MissingPayloadFieldError is raised when required fields
                are missing.\"\"\"
                self.assert_missing_required_fields_raise(my_task, ["attr1", "attr2"])
    """

    _task_class: type
    _check_payload_keys = False
    _check_unexpected_keys = False

    def _validate_task_class(self):
        """
        Validates that the `_task_class` attribute is set and is a subclass of
        AbstractTaskElement.

        Raises:
            NotImplementedError: If `_task_class` is not set in the subclass.
            TypeError: If `_task_class` is not a subclass of AbstractTaskElement.
        """
        if self._task_class is None:
            raise NotImplementedError("Subclasses must set the _task_class attribute.")
        if not issubclass(self._task_class, AbstractTaskElement):
            raise TypeError(
                "Invalid _task_class: must be a subclass of AbstractTaskElement."
            )

    @pytest.fixture
    def my_task(self):
        """
        Creates an instance of the configured task element class for testing.

        Returns:
            object: An instance of the configured task element class.

        Raises:
            NotImplementedError: If `_task_class` is not set in the subclass.
            TypeError: If `_task_class` is not a subclass of AbstractTaskElement.
        """
        self._validate_task_class()
        return self._task_class()

    def test_task_fixture_sanity(self, my_task):
        """
        Basic sanity test for the task fixture.

        Verifies that the fixture returns the correct class instance,
        that the default payload is a non-empty dict,
        and that the serialized payload is a dict with expected keys.
        """
        assert isinstance(my_task, self._task_class)
        assert isinstance(my_task._DEFAULT_PAYLOAD, dict)
        assert my_task._DEFAULT_PAYLOAD, "Default payload should not be empty."
        self.task_check_payload_keys(my_task)
        self.task_check_unexpected_keys(my_task)

    def task_check_payload_keys(self, task):
        """
        Verifies that the serialized payload contains all expected keys.

        Args:
            task (object): The task element instance to check.

        Raises:
            AssertionError: If any expected key is missing from the payload.
        """
        if not self._check_payload_keys:
            return

        payload = task._to_payload()
        assert isinstance(payload, dict)
        for key in task._DEFAULT_PAYLOAD.keys():
            assert key in payload, f"Payload missing expected key: {key}"

    def task_check_unexpected_keys(self, task_instance):
        """
        Verifies that the serialized payload does not contain any unexpected keys.

        Args:
            task_instance (object): The task element instance to check.

        Raises:
            AssertionError: If any unexpected key is found in the payload.
        """
        if not self._check_unexpected_keys:
            return
        allowed_extra_keys = {"tool", "files"}
        payload = task_instance._to_payload()
        unexpected_keys = (
            set(payload.keys())
            - set(task_instance._DEFAULT_PAYLOAD.keys())
            - allowed_extra_keys
        )
        assert not unexpected_keys, f"Payload has unexpected keys: {unexpected_keys}"

    def assert_missing_required_fields_raise(self, my_task, attrs: list[str]):
        """
        Assert that a MissingPayloadFieldError is raised when required fields are
        missing.

        This method sets the specified attributes in the task's payload to None,
        then checks that calling _to_payload() raises a MissingPayloadFieldError
        with the correct missing fields.

        Args:
            my_task: The task element instance to test.
            attrs (list[str]): List of attribute names that should be missing.

        Raises:
            AssertionError: If the exception is not raised or the missing fields
                do not match.
        """
        values = {attr: None for attr in attrs}
        my_task._payload.update(values)

        with pytest.raises(MissingPayloadFieldError) as excinfo:
            my_task._to_payload()
        missing = excinfo.value.missing_fields
        assert set(missing) == set(attrs)


class AbstractBaseFileTest(AbstractUnitTaskElementTest):
    """
    Base class for unit tests of ILovePDF File classes.

    Subclasses must set `_task_class` to a concrete subclass of File.

    Attributes:
        _task_class (Type): Concrete task element class to test.
        _check_payload_keys (bool): If True, check expected payload keys.
        _check_unexpected_keys (bool): If True, check for unexpected payload keys.

    Example:
        class TestAnyTaskElement(AbstractUnitTaskElementTest):
            _task_class = AnyTaskElement  # Must inherit from File

            def test_initialization_sets_default_values(self, my_task):
                # At least one test method must be defined in each test class.
                # Replace this with meaningful assertions for your file task element.
                assert my_task is not None
    """

    def _validate_task_class(self):
        super()._validate_task_class()
        if not issubclass(self._task_class, BaseFile):
            raise TypeError("Invalid _task_class: must be a subclass of File.")

    @pytest.fixture
    def my_task(self):
        self._validate_task_class()
        return self._task_class("some_server_filename", "some_filename")


class AbstractUnitFileTest(AbstractBaseFileTest):
    """
    Base class for unit tests of ILovePDF File classes.

    Subclasses must set `_task_class` to a concrete subclass of File.

    Attributes:
        _task_class (Type): Concrete task element class to test.
        _check_payload_keys (bool): If True, check expected payload keys.
        _check_unexpected_keys (bool): If True, check for unexpected payload keys.

    Example:
        class TestAnyTaskElement(AbstractUnitTaskElementTest):
            _task_class = AnyTaskElement  # Must inherit from File

            def test_initialization_sets_default_values(self, my_task):
                # At least one test method must be defined in each test class.
                # Replace this with meaningful assertions for your file task element.
                assert my_task is not None
    """

    def _validate_task_class(self):
        super()._validate_task_class()
        if not issubclass(self._task_class, File):
            raise TypeError("Invalid _task_class: must be a subclass of File.")


class AbstractUnitTaskTest(AbstractUnitTaskElementTest):
    """
    Base class for unit tests of ILovePDF task classes.

    Subclasses must set `_task_class` to a concrete subclass of Task and `_task_tool`
    to the tool name.

    Attributes:
        _task_class (Type): Concrete task class to test.
        _task_tool (str): Tool name for the task.

    Example:
        class MyTaskTest(AbstractUnitTaskTest):
            _task_class = AnyTask  # Replace with a concrete task class that inherits
                            from Task
            _task_tool = "anytool"

            def test_initialization_sets_default_values(self, my_task):
                # At least one test method must be defined in each test class.
                # Replace this with meaningful assertions for your task.
                assert my_task is not None
    """

    # _task_class is inherited from AbstractUnitTaskElementTest
    _task_tool: str | None = None

    def _validate_task_class(self):
        super()._validate_task_class()
        if self._task_tool is None:
            raise NotImplementedError(
                "Subclasses must set the _task_tool attribute. Example: "
                "'compressimage', 'resizeimage', 'rotateimage', 'cropimage'."
            )
        if not issubclass(self._task_class, Task):
            raise TypeError("Invalid _task_class: must be a subclass of Task.")

        assert self._task_class._task_status is not None

    @pytest.fixture
    def my_task(self):
        """
        Creates an instance of the task class for testing.

        Returns:
            object: An instance of the configured task class.

        Raises:
            NotImplementedError: If `_task_class` or `_task_tool` is not set in the
                subclass.
            TypeError: If `_task_class` is not a subclass of Task.
        """
        self._validate_task_class()
        return self._task_class("public_key", "secret_key", make_start=False)

    def test_tool(self, my_task):
        """
        Tests that the tool attribute is set correctly.

        Args:
            my_task: The task instance created by the fixture.
        """
        assert my_task._tool == my_task.tool == self._task_tool
        assert my_task._task_status == self._task_class._task_status
