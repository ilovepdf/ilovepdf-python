"""ElementInitials module for iLovePDF signature elements.

This module defines the ElementInitials class, representing an initials field
for digital signatures in PDF documents.
"""

from .element_abstract import ElementAbstract


class ElementInitials(ElementAbstract):
    """Signature element representing an initials field."""

    def __init__(self):
        super().__init__()
        self.size = 28
        self.set_type("initials")
