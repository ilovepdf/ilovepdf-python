"""ProtectTask for the iLovePDF Python API.
Handles PDF protection tasks, such as setting passwords and permissions.
"""

# pylint: disable=abstract-method

from .task import ProcessTask


class ProtectTask(ProcessTask):
    """
    ProtectTask for the iLovePDF Python API.
    Handles PDF protection tasks, such as setting passwords and permissions.
    """

    def __init__(self, public_key, secret_key, make_start=True):
        super().__init__(public_key, secret_key, make_start, tool="protect")
        self.password = None

    def set_password(self, password: str):
        if not isinstance(password, str) or not password:
            raise ValueError("Password must be a non-empty string")
        self.password = password
        return self

    def add_file(self, file_path, extra_params=None):
        self._validate_file_extension(file_path)
        return super().add_file(file_path, extra_params)

    def _to_dict(self):
        """
        Converts the ProtectTask instance to a dictionary, including the password option.
        """
        base = super()._to_dict()
        base["password"] = self.password
        return base
