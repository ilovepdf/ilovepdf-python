"""Validator receiver module for iLovePDF signature workflows.

Defines the Validator class, representing a validator participant in a PDF signature process.
"""

from .receiver_abstract import ReceiverAbstract


class Validator(ReceiverAbstract):
    """Represents a validator participant in a PDF signature workflow."""

    def __init__(self, name: str, email: str):
        super().__init__(name, email)
        self.set_type("validator")
