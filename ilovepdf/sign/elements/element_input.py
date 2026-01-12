"""ElementInput module for iLovePDF signature elements.

Defines the ElementInput class, representing a text input field for PDF signatures.
"""

from .element_abstract import ElementAbstract


class ElementInput(ElementAbstract):
    """Signature element representing a text input field."""

    def __init__(self):
        super().__init__()
        self.info = {"label": "input text", "description": None}
        self.set_type("input")

    def set_label(self, text):
        self.info["label"] = text
        return self

    def set_text(self, text):
        self.info["description"] = text
        return self
