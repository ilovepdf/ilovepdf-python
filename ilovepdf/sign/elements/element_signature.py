"""ElementSignature module for iLovePDF signature elements.

Defines the ElementSignature class, representing a signature field for PDF signatures.
"""

from .element_abstract import ElementAbstract


class ElementSignature(ElementAbstract):
    """Signature element representing a signature field."""

    def __init__(self):
        super().__init__()
        self.size = 28
        self.set_type("signature")
