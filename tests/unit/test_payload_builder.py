"""Unit tests for PayloadBuilder and TaskStateManager classes in the ilovepdf module.

These tests verify the correct behavior of payload building and task state management
operations.
"""

import pytest

from ilovepdf.task import PayloadBuilder, TaskStateManager

# pylint: disable=protected-access


class TestPayloadBuilderInitialization:
    """Unit tests for PayloadBuilder initialization."""

    def test_initialization_with_callable(self):
        """
        Test that PayloadBuilder initializes with a callable function.
        """

        def sample_payload():
            return {"key": "value"}

        builder = PayloadBuilder(sample_payload)
        assert builder._to_payload() == sample_payload()

    def test_initialization_stores_function_reference(self):
        """
        Test that PayloadBuilder stores the function reference correctly.
        """

        def payload_func():
            return {"data": "test"}

        builder = PayloadBuilder(payload_func)
        assert callable(builder._to_payload)


class TestPayloadBuilderBuildBody:
    """Unit tests for PayloadBuilder.build_body method."""

    def test_build_body_returns_dict(self):
        """
        Test that build_body returns a dictionary.
        """

        def payload_func():
            return {"key": "value"}

        builder = PayloadBuilder(payload_func)
        body = builder.build_body("1.0.0")
        assert isinstance(body, dict)

    def test_build_body_includes_data_key(self):
        """
        Test that build_body includes 'data' key in the result.
        """

        def payload_func():
            return {"key": "value"}

        builder = PayloadBuilder(payload_func)
        body = builder.build_body("1.0.0")
        assert "data" in body

    def test_build_body_includes_params_key(self):
        """
        Test that build_body includes 'params' key with version.
        """

        def payload_func():
            return {"key": "value"}

        builder = PayloadBuilder(payload_func)
        body = builder.build_body("1.0.0")
        assert "params" in body
        assert body["params"]["v"] == "1.0.0"

    def test_build_body_removes_timeout_keys(self):
        """
        Test that build_body removes timeout configuration keys.
        """

        def payload_func():
            return {"key": "value", "timeout": 30, "timeout_large": 60, "time_delay": 1}

        builder = PayloadBuilder(payload_func)
        body = builder.build_body("1.0.0")
        assert "timeout" not in body["data"]
        assert "timeout_large" not in body["data"]
        assert "time_delay" not in body["data"]

    def test_build_body_preserves_other_keys(self):
        """
        Test that build_body preserves keys that are not timeout-related.
        """

        def payload_func():
            return {"key": "value", "tool": "compressimage", "timeout": 30}

        builder = PayloadBuilder(payload_func)
        body = builder.build_body("1.0.0")
        assert body["data"]["key"] == "value"
        assert body["data"]["tool"] == "compressimage"
        assert "timeout" not in body["data"]

    def test_build_body_with_complex_payload(self):
        """
        Test that build_body handles complex nested payload structures.
        """

        def payload_func():
            return {
                "files": [{"name": "file1.jpg"}],
                "settings": {"quality": 80},
                "timeout": 30,
            }

        builder = PayloadBuilder(payload_func)
        body = builder.build_body("1.0.0")
        assert body["data"]["files"] == [{"name": "file1.jpg"}]
        assert body["data"]["settings"]["quality"] == 80
        assert "timeout" not in body["data"]

    def test_build_body_with_multiple_timeout_keys(self):
        """
        Test that build_body removes all timeout-related keys when present.
        """

        def payload_func():
            return {
                "key": "value",
                "timeout": 30,
                "timeout_large": 60,
                "time_delay": 1,
                "other": "data",
            }

        builder = PayloadBuilder(payload_func)
        body = builder.build_body("2.0.0")
        assert "timeout" not in body["data"]
        assert "timeout_large" not in body["data"]
        assert "time_delay" not in body["data"]
        assert body["data"]["other"] == "data"
        assert body["params"]["v"] == "2.0.0"


class TestPayloadBuilderValidateBody:
    """Unit tests for PayloadBuilder.validate_body static method."""

    def test_validate_body_with_valid_dict(self):
        """
        Test that validate_body returns True for valid dictionary.
        """
        body = {"data": {"key": "value"}, "params": {"v": "1.0"}}
        result = PayloadBuilder.validate_body(body)
        assert result is True

    def test_validate_body_with_empty_dict(self):
        """
        Test that validate_body raises ValueError for empty dictionary.
        """
        with pytest.raises(ValueError) as excinfo:
            PayloadBuilder.validate_body({})
        assert "Invalid body" in str(excinfo.value)

    def test_validate_body_with_none(self):
        """
        Test that validate_body raises ValueError for None.
        """
        with pytest.raises(ValueError):
            PayloadBuilder.validate_body(None)

    def test_validate_body_with_complex_dict(self):
        """
        Test that validate_body accepts complex dictionary structures.
        """
        body = {
            "data": {"files": [{"name": "file.jpg"}], "settings": {"quality": 80}},
            "params": {"v": "1.0"},
        }
        result = PayloadBuilder.validate_body(body)
        assert result is True


class TestTaskStateManagerInitialization:
    """Unit tests for TaskStateManager initialization."""

    def test_initialization_sets_default_values(self):
        """
        Test that TaskStateManager initializes with None values.
        """
        manager = TaskStateManager()
        assert manager.task is None
        assert manager.status is None
        assert manager.status_message is None
        assert manager.remaining_credits is None
        assert manager.remaining_files is None
        assert manager.remaining_pages is None

    def test_initialization_creates_all_attributes(self):
        """
        Test that all expected attributes are initialized.
        """
        manager = TaskStateManager()
        assert hasattr(manager, "task")
        assert hasattr(manager, "status")
        assert hasattr(manager, "status_message")
        assert hasattr(manager, "remaining_credits")
        assert hasattr(manager, "remaining_files")
        assert hasattr(manager, "remaining_pages")


class TestTaskStateManagerValidateTaskStarted:
    """Unit tests for TaskStateManager.validate_task_started method."""

    def test_validate_task_started_raises_when_task_is_none(self):
        """
        Test that validate_task_started raises ValueError when task is None.
        """
        manager = TaskStateManager()
        with pytest.raises(ValueError) as excinfo:
            manager.validate_task_started()
        assert "Current task does not exist" in str(excinfo.value)

    def test_validate_task_started_raises_when_task_is_empty_string(self):
        """
        Test that validate_task_started raises ValueError when task is empty string.
        """
        manager = TaskStateManager()
        manager.task = ""
        with pytest.raises(ValueError) as excinfo:
            manager.validate_task_started()
        assert "Current task does not exist" in str(excinfo.value)

    def test_validate_task_started_passes_when_task_is_set(self):
        """
        Test that validate_task_started passes when task is set.
        """
        manager = TaskStateManager()
        manager.task = "task_123"
        manager.validate_task_started()

    def test_validate_task_started_with_valid_task_id(self):
        """
        Test that validate_task_started accepts valid task IDs.
        """
        manager = TaskStateManager()
        manager.task = "abc123def456"
        manager.validate_task_started()


class TestTaskStateManagerSetTask:
    """Unit tests for TaskStateManager.set_task method."""

    def test_set_task_updates_task_attribute(self):
        """
        Test that set_task updates the task attribute.
        """
        manager = TaskStateManager()
        manager.set_task("task_123")
        assert manager.task == "task_123"

    def test_set_task_with_different_values(self):
        """
        Test that set_task works with different task ID formats.
        """
        manager = TaskStateManager()
        task_ids = ["task_1", "task_abc", "123456", "complex_task_id_123"]
        for task_id in task_ids:
            manager.set_task(task_id)
            assert manager.task == task_id

    def test_set_task_overwrites_previous_value(self):
        """
        Test that set_task overwrites the previous task ID.
        """
        manager = TaskStateManager()
        manager.set_task("task_1")
        assert manager.task == "task_1"
        manager.set_task("task_2")
        assert manager.task == "task_2"

    def test_set_task_allows_empty_string(self):
        """
        Test that set_task allows setting empty string.
        """
        manager = TaskStateManager()
        manager.set_task("")
        assert manager.task == ""


class TestTaskStateManagerGetTaskId:
    """Unit tests for TaskStateManager.get_task_id method."""

    def test_get_task_id_returns_none_when_not_set(self):
        """
        Test that get_task_id returns None when task is not set.
        """
        manager = TaskStateManager()
        assert manager.get_task_id() is None

    def test_get_task_id_returns_task_value(self):
        """
        Test that get_task_id returns the task ID.
        """
        manager = TaskStateManager()
        manager.set_task("task_123")
        assert manager.get_task_id() == "task_123"


class TestTaskStateManagerUpdateStatus:
    """Unit tests for TaskStateManager.update_status method."""

    def test_update_status_from_result_dict(self):
        """
        Test that update_status extracts status from result dictionary.
        """
        manager = TaskStateManager()
        result = {"status": "processing", "status_message": "Processing files"}
        manager.update_status(result)
        assert manager.status == "processing"
        assert manager.status_message == "Processing files"

    def test_update_status_with_missing_keys(self):
        """
        Test that update_status handles missing keys gracefully.
        """
        manager = TaskStateManager()
        result = {}
        manager.update_status(result)
        assert manager.status is None
        assert manager.status_message is None

    def test_update_status_with_partial_result(self):
        """
        Test that update_status handles partial result dictionary.
        """
        manager = TaskStateManager()
        result = {"status": "completed"}
        manager.update_status(result)
        assert manager.status == "completed"
        assert manager.status_message is None

    def test_update_status_overwrites_previous_values(self):
        """
        Test that update_status overwrites previous status values.
        """
        manager = TaskStateManager()
        manager.status = "idle"
        manager.status_message = "Waiting"

        result = {"status": "processing", "status_message": "Processing files"}
        manager.update_status(result)
        assert manager.status == "processing"
        assert manager.status_message == "Processing files"


class TestTaskStateManagerSetCredits:
    """Unit tests for TaskStateManager credit tracking methods."""

    def test_set_remaining_credits(self):
        """
        Test that set_remaining_credits updates the remaining_credits attribute.
        """
        manager = TaskStateManager()
        manager.set_remaining_credits(100)
        assert manager.remaining_credits == 100

    def test_set_remaining_files(self):
        """
        Test that set_remaining_files updates the remaining_files attribute.
        """
        manager = TaskStateManager()
        manager.set_remaining_files(5)
        assert manager.remaining_files == 5

    def test_set_remaining_pages(self):
        """
        Test that set_remaining_pages updates the remaining_pages attribute.
        """
        manager = TaskStateManager()
        manager.set_remaining_pages(10)
        assert manager.remaining_pages == 10

    def test_set_multiple_credit_values(self):
        """
        Test that multiple credit values can be set independently.
        """
        manager = TaskStateManager()
        manager.set_remaining_credits(100)
        manager.set_remaining_files(5)
        manager.set_remaining_pages(10)
        assert manager.remaining_credits == 100
        assert manager.remaining_files == 5
        assert manager.remaining_pages == 10
