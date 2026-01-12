"""This module defines the SignTask class for handling signature tasks in the ilovepdf
package."""

#


from typing import Any, Dict, List, Literal, Optional, Sequence

from ilovepdf.exceptions import NotImplementedException

from .sign import Signer
from .task import Task
from .validators import BoolValidator, ChoiceValidator, IntValidator, StringValidator

MAX_SIGNERS = 50

LanguageType = Literal[
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
]

LANGUAGE_OPTIONS = {
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

MAXIMUM_NUMBER_ALLOWED = 5


# pylint: disable=too-many-instance-attributes, too-many-public-methods
class SignTask(Task):
    """Class representing a signature task in the ilovepdf package."""

    _tool = "sign"
    _endpoint_execute = "signature"
    _task_status = "draft"

    _DEFAULT_PAYLOAD = {
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

    _LIST_ATTRS: Sequence[str] = ("files", "signers")
    REQUIRED_FIELDS = ["files", "signers"]

    # Getters and Setters of brand_name
    @property
    def brand_name(self) -> str:
        """Get the brand name for the signature task."""
        return self._get_attr("brand_name")

    @brand_name.setter
    def brand_name(self, value: str):
        """Set the brand name for the signature task."""
        StringValidator.validate_type(value, "brand_name")
        self._set_attr("brand_name", value)

    # Getters and Setters of brand_logo
    @property
    def brand_logo(self) -> str:
        """Get the brand logo for the signature task."""
        return self._get_attr("brand_logo")

    @brand_logo.setter
    def brand_logo(self, value: str):
        """Set the brand logo for the signature task."""
        StringValidator.validate_type(value, "brand_logo")
        self._set_attr("brand_logo", value)

    # Getters and Setters of signers
    @property
    def signers(self) -> List[Signer]:
        """Get the list of signers for the signature task."""
        return self._get_attr("signers")

    def add_signer(self, signer: Optional[Signer] = None) -> Signer:
        """Add a signer to the signature task."""
        if len(self.signers) >= MAX_SIGNERS:
            raise ValueError("Maximum number of signers reached")
        if signer is None:
            signer = Signer()
        if not isinstance(signer, Signer):
            raise TypeError("signer must be an instance of Signer")
        self._set_attr("signers", self.signers + [signer])
        return signer

    # Getters and Setters of language
    @property
    def language(self) -> LanguageType:
        """Get the language for the signature task."""
        return self._get_attr("language")

    @language.setter
    def language(self, value: LanguageType):
        """Set the language for the signature task."""
        ChoiceValidator.validate(value, LANGUAGE_OPTIONS, "language")
        self._set_attr("language", value)

    # Getters and Setters of lock_order
    @property
    def lock_order(self) -> bool:
        """Get the lock order for the signature task."""
        return self._get_attr("lock_order")

    @lock_order.setter
    def lock_order(self, value: bool):
        """Set the lock order for the signature task."""
        BoolValidator.validate(value, "lock_order")
        self._set_attr("lock_order", value)

    # Getters and Setters of message_signer
    @property
    def message_signer(self) -> str:
        """Get the message signer for the signature task."""
        return self._get_attr("message_signer")

    @message_signer.setter
    def message_signer(self, value: str):
        """Set the message signer for the signature task."""
        StringValidator.validate_type(value, "message_signer")
        self._set_attr("message_signer", value)

    # Getters and Setters of subject_signer
    @property
    def subject_signer(self) -> str:
        """Get the subject signer for the signature task."""
        return self._get_attr("subject_signer")

    @subject_signer.setter
    def subject_signer(self, value: str):
        StringValidator.validate_type(value, "subject_signer")
        self._set_attr("subject_signer", value)

    # Getters and Setters of uuid_visible
    @property
    def uuid_visible(self) -> bool:
        """Get the visibility of the UUID for the signature task."""
        return self._get_attr("uuid_visible")

    @uuid_visible.setter
    def uuid_visible(self, value: bool):
        """Set the visibility of the UUID for the signature task."""
        BoolValidator.validate(value, "uuid_visible")
        self._set_attr("uuid_visible", value)

    # Getters and Setters of expiration_days
    @property
    def expiration_days(self) -> int:
        """Get the expiration days for the signature task."""
        return self._get_attr("expiration_days")

    @expiration_days.setter
    def expiration_days(self, value: int):
        """Set the expiration days for the signature task."""
        IntValidator.validate_non_negative(value, "expiration_days")
        self._set_attr("expiration_days", value)

    # Getters and Setters of signer_reminders
    @property
    def signer_reminders(self) -> bool:
        """Get the status of signer reminders for the signature task."""
        return self._get_attr("signer_reminders")

    @signer_reminders.setter
    def signer_reminders(self, value: bool):
        """Set the status of signer reminders for the signature task."""
        BoolValidator.validate(value, "signer_reminders")
        self._set_attr("signer_reminders", value)

    # Getters and Setters of signer_reminder_days_cycle
    @property
    def signer_reminder_days_cycle(self) -> int:
        """Get the number of days between signer reminders for the signature task."""
        return self._get_attr("signer_reminder_days_cycle")

    @signer_reminder_days_cycle.setter
    def signer_reminder_days_cycle(self, value: int):
        """Set the number of days between signer reminders for the signature task."""
        IntValidator.validate_non_negative(value, "signer_reminder_days_cycle")
        self._set_attr("signer_reminder_days_cycle", value)

    # Getters and Setters of verify_enabled
    @property
    def verify_enabled(self) -> bool:
        """Get the status of verification for the signature task."""
        return self._get_attr("verify_enabled")

    @verify_enabled.setter
    def verify_enabled(self, value: bool):
        """Set the status of verification for the signature task."""
        BoolValidator.validate(value, "verify_enabled")
        self._set_attr("verify_enabled", value)

    def download(self, path=None):
        raise NotImplementedException("This API call is not available for a SignTask")

    def _to_payload(self) -> Dict[str, Any]:
        payload = super()._to_payload()
        del payload["tool"]
        return payload

    def append_file(self, file):
        if len(self.files) == MAXIMUM_NUMBER_ALLOWED:
            raise ValueError("Maximum number of files reached.")
        return super().append_file(file)
