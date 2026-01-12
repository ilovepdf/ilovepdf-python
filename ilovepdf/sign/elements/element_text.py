"""ElementText module for iLovePDF signature elements.

Defines the ElementText class, representing a text field for PDF signatures.
"""

from .element_abstract import ElementAbstract


class ElementText(ElementAbstract):
    """Signature element representing a text field."""

    def __init__(self):
        super().__init__()
        self.set_type("text")
        self.set_text("text")

    def set_text(self, text):
        self.set_content(text)
        return self
