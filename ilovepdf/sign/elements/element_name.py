"""Element for representing a name field in iLovePDF signature workflows."""

from .element_abstract import ElementAbstract


class ElementName(ElementAbstract):
    """Element representing a name field for digital signatures."""

    def __init__(self):
        super().__init__()
        self.set_type("name")
