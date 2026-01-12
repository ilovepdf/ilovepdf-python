"""This module defines the SignTask class for handling signature tasks in the ilovepdf package."""

# pylint: disable=too-many-instance-attributes, too-many-public-methods

from ilovepdf.exceptions import NotImplementedException

from .task import ProcessTask


class SignTask(ProcessTask):
    """Class representing a signature task in the ilovepdf package."""

    def __init__(self, public_key=None, secret_key=None, make_start=True):
        super().__init__(public_key, secret_key, make_start, tool="sign")
        self.lock_order = None
        self.expiration_days = None
        self.language = None
        self.subject_signer = None
        self.message_signer = None
        self.signers = []
        self.uuid_visible = None
        self.reminders = None
        self.verify_enabled = None
        self.brand_name = None
        self.brand_logo = None
        self._endpoint_execute = "signature"

    def add_receiver(self, signer):
        self.signers.append(signer)
        return self

    def get_verify_signature_verification(self):
        return self.verify_enabled

    def set_verify_signature_verification(self, verification):
        self.verify_enabled = verification
        return self

    def get_message(self):
        return self.message_signer

    def set_message(self, message):
        self.message_signer = message
        return self

    def get_subject(self):
        return self.subject_signer

    def set_subject(self, subject):
        self.subject_signer = subject
        return self

    def get_reminders(self):
        return self.reminders

    def set_reminders(self, days_between):
        self.reminders = days_between
        return self

    def get_lock_order(self):
        return int(self.lock_order) if self.lock_order is not None else None

    def set_lock_order(self, lock_order):
        self.lock_order = int(lock_order)
        return self

    def get_expiration_days(self):
        return self.expiration_days

    def set_expiration_days(self, expiration_days):
        self.expiration_days = expiration_days
        return self

    def set_brand(self, brand_name, brand_logo):
        self.brand_name = brand_name
        self.brand_logo = getattr(brand_logo, "server_filename", brand_logo)
        return self

    def get_language(self):
        return self.language

    def set_language(self, language):
        self.language = language
        return self

    def get_signers(self):
        return self.signers

    def set_signers(self, signers):
        self.signers = signers
        return self

    def get_signers_data(self):
        data = []
        for signer in self.get_signers():
            # It is assumed that each signer has a to_dict() method
            data.append(signer.to_dict())
        return data

    def get_uuid_visible(self):
        return self.uuid_visible

    def set_uuid_visible(self, uuid_visible):
        self.uuid_visible = uuid_visible
        return self

    def upload_brand_logo(self, file_path):
        raise NotImplementedException(
            "This method is not implemented in this Python version."
        )

    def upload_brand_logo_from_url(self, url, bearer_token=None):
        raise NotImplementedException(
            "This method is not implemented in this Python version."
        )

    def download(self, path=None):
        raise NotImplementedException("This API call is not available for a SignTask")

    def enable_encryption(self, enable):
        raise NotImplementedException("This method is not available for a SignTask")

    def set_file_encryption(self, encrypt_key=None):
        raise NotImplementedException("This method is not available for a SignTask")

    def _to_dict(self):
        res = super()._to_dict()
        res["signers"] = self.get_signers_data()
        del res["tool"]
        return res

    def _get_body(self):
        res = super()._get_body()
        res["json"] = res["data"]
        del res["data"]
        return res
