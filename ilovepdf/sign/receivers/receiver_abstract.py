"""Module containing the ReceiverAbstract class for handling receiver information."""


class ReceiverAbstract:
    """Abstract base class representing a receiver with name, email, type, and access code."""

    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email
        self.type = None
        self.access_code = None

    def get_name(self) -> str:
        return self.name

    def set_name(self, name: str):
        self.name = name
        return self

    def get_email(self) -> str:
        return self.email

    def set_email(self, email: str):
        self.email = email
        return self

    def get_type(self) -> str:
        return self.type

    def set_type(self, type_: str):
        self.type = type_
        return self

    def get_access_code(self):
        return self.access_code

    def set_access_code(self, access_code):
        self.access_code = access_code
        return self

    def to_dict(self):
        return {
            "name": self.get_name(),
            "email": self.get_email(),
            "type": self.get_type(),
            "access_code": self.get_access_code(),
        }
