"""Unit tests for the SignTask class in the ilovepdf module.

This module contains unit tests for the SignTask class, covering its
initialization, setters, and methods for managing files and signers.
"""

import pytest

from ilovepdf import File, SignTask
from ilovepdf.exceptions import (
    IntOutOfRangeError,
    InvalidChoiceError,
    NotAnIntError,
    NotImplementedException,
)
from ilovepdf.sign import Signer
from ilovepdf.sign_task import LANGUAGE_OPTIONS, MAXIMUM_NUMBER_ALLOWED

from .base_test import AbstractUnitTaskTest
from .samples_utils import FileSamples, SignerSamples


# pylint: disable=protected-access, too-many-public-methods, attribute-defined-outside-init
class TestSignTask(AbstractUnitTaskTest):
    """Unit tests for the SignTask class."""

    _task_class = SignTask
    _task_tool = "sign"

    def test_initialization_sets_default_values(self, my_task):
        """Test that default values are set on initialization."""
        assert MAXIMUM_NUMBER_ALLOWED == 5
        assert my_task._DEFAULT_PAYLOAD == {
            "files": [],
            "brand_name": None,
            "brand_logo": None,
            "signers": [],
            "language": "en-US",
            "lock_order": False,
            "message_signer": None,
            "subject_signer": None,
            "uuid_visible": True,
            "expiration_days": 120,
            "signer_reminders": True,
            "signer_reminder_days_cycle": 1,
            "verify_enabled": True,
        }

        assert LANGUAGE_OPTIONS == {
            "en-US",
            "es",
            "fr",
            "it",
            "ca",
            "zh-cn",
            "zh-tw",
            "ar",
            "ru",
            "de",
            "ja",
            "pt",
            "bg",
            "ko",
            "nl",
            "el",
            "hi",
            "id",
            "ms",
            "pl",
            "sv",
            "th",
            "tr",
            "uk",
            "vi",
            "zh-Hans",
            "zh-Hant",
        }

        assert my_task.files == []
        assert my_task.brand_name is None
        assert my_task.brand_logo is None
        assert my_task.signers == []
        assert my_task.language == "en-US"
        assert my_task.lock_order is False
        assert my_task.message_signer is None
        assert my_task.subject_signer is None
        assert my_task.uuid_visible is True
        assert my_task.expiration_days == 120
        assert my_task.signer_reminders is True
        assert my_task.signer_reminder_days_cycle == 1
        assert my_task.verify_enabled is True

    def test_append_file(self, my_task):
        """Test adding files up to the maximum allowed and raising ValueError if
        exceeded."""
        # Add the maximum allowed number of files
        for k in range(MAXIMUM_NUMBER_ALLOWED):
            file = File(
                server_filename=f"srv_fname_{k}",
                filename=f"fname_{k}",
            )
            my_task.append_file(file)

        # Assert that the number of files is equal to the maximum allowed
        assert len(my_task.files) == MAXIMUM_NUMBER_ALLOWED

        # Try to add one more file and expect a ValueError
        extra_file = File(
            server_filename="srv_fname_extra",
            filename="fname_extra",
        )
        with pytest.raises(ValueError, match="Maximum number of files reached."):
            my_task.append_file(extra_file)

    # Test brand_name
    @pytest.mark.parametrize("value", ["some", ""])
    def test_set_brand_name(self, my_task, value):
        """Test setting a valid brand_name."""
        my_task.brand_name = value
        assert my_task.brand_name == value

    @pytest.mark.parametrize("value", [None, 1, []])
    def test_set_brand_name_is_invalid(self, my_task, value):
        """
        Test setting an invalid brand_name raises an error.
        Covers:
        - None, int, or list input (StringValidator enforces non-empty str)
        """
        # StringValidator strictly rejects None, int, and list
        with pytest.raises((TypeError, ValueError)):
            my_task.brand_name = value

    # Test brand_logo
    @pytest.mark.parametrize("value", ["some", ""])
    def test_set_brand_logo(self, my_task, value):
        """Test setting a valid brand_logo."""
        my_task.brand_logo = value
        assert my_task.brand_logo == value

    @pytest.mark.parametrize("value", [None, 1, []])
    def test_set_brand_logo_is_invalid(self, my_task, value):
        """
        Test setting an invalid brand_logo raises an error.
        Covers:
        - None, int, empty string, or list input (StringValidator enforces non-empty
            str)
        """
        # StringValidator strictly rejects None, int, "", and list
        with pytest.raises((TypeError, ValueError)):
            my_task.brand_logo = value

    # Test language
    @pytest.mark.parametrize("language", LANGUAGE_OPTIONS)
    def test_set_language(self, my_task, language):
        """Test setting a valid language."""
        my_task.language = language
        assert my_task.language == language

    @pytest.mark.parametrize("language", ["", 1, "other", None])
    def test_set_language_is_invalid(self, my_task, language):
        """Test setting an invalid language raises InvalidChoiceError."""
        with pytest.raises(InvalidChoiceError):
            my_task.language = language

    # Test lock_order
    @pytest.mark.parametrize("value", [True, False])
    def test_set_lock_order(self, my_task, value):
        """Test setting a valid lock_order."""
        my_task.lock_order = value
        assert my_task.lock_order == value

    @pytest.mark.parametrize("value", ["", 1, "other", None])
    def test_set_lock_order_invalid(self, my_task, value):
        """
        Test setting an invalid lock_order raises InvalidChoiceError. Covers:
        - Passing None value (BoolValidator should reject None)
        - Passing int or str value (BoolValidator should reject)
        """
        # None explicitly tested as invalid edge case
        with pytest.raises(InvalidChoiceError):
            my_task.lock_order = value

    # Test message_signer
    @pytest.mark.parametrize("value", ["some", ""])
    def test_set_message_signer(self, my_task, value):
        """Test setting a valid message_signer."""
        my_task.message_signer = value
        assert my_task.message_signer == value

    @pytest.mark.parametrize("value", [None, 1, []])
    def test_set_message_signer_is_invalid(self, my_task, value):
        """
        Test setting an invalid message_signer raises error.
        Covers:
        - None, int, "" and list (StringValidator strictly enforces valid non-empty str)
        """
        # StringValidator strictly rejects None, int, "", and list
        with pytest.raises((TypeError, ValueError)):
            my_task.message_signer = value

    # Test subject_signer
    @pytest.mark.parametrize("value", ["some", ""])
    def test_set_subject_signer(self, my_task, value):
        """Test setting a valid subject_signer."""
        my_task.subject_signer = value
        assert my_task.subject_signer == value

    @pytest.mark.parametrize("value", [None, 1, []])
    def test_set_subject_signer_is_invalid(self, my_task, value):
        """
        Test setting an invalid subject_signer raises error.
        Covers:
        - None, int, "" and list (StringValidator strictly enforces valid non-empty str)
        """
        # StringValidator strictly rejects None, int, "", and list
        with pytest.raises((TypeError, ValueError)):
            my_task.subject_signer = value

    # Test uuid_visible
    @pytest.mark.parametrize("value", [True, False])
    def test_set_uuid_visible(self, my_task, value):
        """Test setting a valid uuid_visible."""
        my_task.uuid_visible = value
        assert my_task.uuid_visible == value

    @pytest.mark.parametrize("value", ["", 1, "other", None])
    def test_set_uuid_visible_invalid(self, my_task, value):
        """
        Test setting an invalid uuid_visible raises InvalidChoiceError. Covers:
        - None as input (BoolValidator strictly enforces boolean)
        - 1, "other", "" as invalid types
        """
        # None is now a documented test case
        with pytest.raises(InvalidChoiceError):
            my_task.uuid_visible = value

    # Test expiration_days
    @pytest.mark.parametrize("value", [0, 1, 100])
    def test_set_expiration_days(self, my_task, value):
        """Test setting a valid expiration_days including boundary value 0."""
        my_task.expiration_days = value
        assert my_task.expiration_days == value

    @pytest.mark.parametrize("value", [None, "0", "1", "100"])
    def test_set_expiration_days_not_an_int(self, my_task, value):
        """Test setting a non-integer expiration_days raises NotAnIntError."""
        with pytest.raises(NotAnIntError):
            my_task.expiration_days = value

    @pytest.mark.parametrize("value", [-100, -1])
    def test_set_expiration_days_negative(self, my_task, value):
        """Test setting a negative expiration_days raises IntOutOfRangeError."""
        with pytest.raises(IntOutOfRangeError):
            my_task.expiration_days = value

    # Test signer_reminders
    @pytest.mark.parametrize("value", [True, False])
    def test_set_signer_reminders(self, my_task, value):
        """Test setting a valid signer_reminders."""
        my_task.signer_reminders = value
        assert my_task.signer_reminders == value

    @pytest.mark.parametrize("value", ["", 1, "other", None])
    def test_set_signer_reminders_invalid(self, my_task, value):
        """
        Test setting an invalid signer_reminders raises InvalidChoiceError. Covers:
        - None as input (BoolValidator strictly enforces boolean)
        - 1, "other", "" as invalid types
        """
        # None is now a documented test case
        with pytest.raises(InvalidChoiceError):
            my_task.signer_reminders = value

    # Test signer_reminder_days_cycle
    @pytest.mark.parametrize("value", [0, 1, 100])
    def test_set_signer_reminder_days_cycle(self, my_task, value):
        """Test setting a valid signer_reminder_days_cycle."""
        my_task.signer_reminder_days_cycle = value
        assert my_task.signer_reminder_days_cycle == value

    @pytest.mark.parametrize("value", [None, "0", "1", "100"])
    def test_set_signer_reminder_days_cycle_not_an_int(self, my_task, value):
        """Test setting a non-integer signer_reminder_days_cycle raises
        NotAnIntError."""
        with pytest.raises(NotAnIntError):
            my_task.signer_reminder_days_cycle = value

    @pytest.mark.parametrize("value", [-100, -1])
    def test_set_signer_reminder_days_cycle_invalid(self, my_task, value):
        """Test setting a negative signer_reminder_days_cycle raises
        IntOutOfRangeError."""
        with pytest.raises(IntOutOfRangeError):
            my_task.signer_reminder_days_cycle = value

    # Test verify_enabled
    @pytest.mark.parametrize("value", [True, False])
    def test_set_verify_enabled(self, my_task, value):
        """Test setting a valid verify_enabled."""
        my_task.verify_enabled = value
        assert my_task.verify_enabled == value

    @pytest.mark.parametrize("value", ["", 1, "other", None])
    def test_set_verify_enabled_invalid(self, my_task, value):
        """
        Test setting an invalid verify_enabled raises InvalidChoiceError. Covers:
        - None as input (BoolValidator strictly enforces boolean)
        - 1, "other", "" as invalid types
        """
        # None is now a documented test case
        with pytest.raises(InvalidChoiceError):
            my_task.verify_enabled = value

    def test_add_signer(self, my_task):
        """Test adding signers to the SignTask."""
        signer1 = my_task.add_signer()
        assert isinstance(signer1, Signer)
        assert my_task.signers[-1] == signer1
        assert my_task.signers == [signer1]

    def test_add_signer_max_signers(self, my_task):
        """Test that adding more than the maximum allowed signers raises an error."""
        max_signers = 50
        for _ in range(max_signers):
            my_task.add_signer()
        assert len(my_task.signers) == max_signers

        with pytest.raises(ValueError, match="Maximum number of signers reached"):
            my_task.add_signer()

    def test_add_signer_error(self, my_task):
        """Test that adding an invalid signer raises an error."""
        with pytest.raises(TypeError):
            my_task.add_signer("invalid_element")

    @pytest.mark.parametrize("file", [FileSamples.file1, FileSamples.file2])
    def test_add_file(self, my_task, file):
        """Test adding files to the SignTask and verifying payload structure."""
        res_file = my_task.append_file(file)
        assert isinstance(res_file, File)
        assert res_file is file
        assert my_task.files[-1] == res_file

    def test_full_flow_basic(self, my_task):
        """Test the full flow of adding multiple files and signers to a SignTask
        and verifying the payload structure."""

        # Create files
        file1 = FileSamples.file1
        file2 = FileSamples.file2
        file3 = FileSamples.file3
        file4 = FileSamples.file4

        # Step 1: Add files
        my_task.append_file(file1)
        my_task.append_file(file2)
        my_task.append_file(file3)
        my_task.append_file(file4)

        # Step 2: Add signers
        signer1 = my_task.add_signer(SignerSamples.signer1)
        signer2 = my_task.add_signer(SignerSamples.signer2)

        # Step 3: Check payload
        payload = my_task._to_payload()
        assert payload["files"] == [
            file1._to_payload(),
            file2._to_payload(),
            file3._to_payload(),
            file4._to_payload(),
        ]

        assert payload["signers"] == [
            signer1._to_payload(),
            signer2._to_payload(),
        ]

    def test_download_not_implemented(self, my_task):
        """Test that download method raises NotImplementedException."""
        with pytest.raises(
            NotImplementedException,
            match="This API call is not available for a SignTask",
        ):
            my_task.download()
