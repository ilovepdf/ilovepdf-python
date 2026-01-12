"""Witness receiver module for iLovePDF signature workflows.

Defines the Witness class, representing a witness (viewer) in a PDF signature process.
"""

from .receiver_abstract import ReceiverAbstract


class Witness(ReceiverAbstract):
    """Represents a witness (viewer) receiver in a PDF signature workflow."""

    def __init__(self, name: str, email: str):
        super().__init__(name, email)
        self.set_type("viewer")
