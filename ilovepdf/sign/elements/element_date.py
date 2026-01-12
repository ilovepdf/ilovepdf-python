"""ElementDate module for iLovePDF signature elements.

Defines the ElementDate class, which represents a date field in a PDF signature workflow.
"""

from .element_abstract import ElementAbstract


class ElementDate(ElementAbstract):
    """Represents a date element for PDF signature fields.

    Provides various date formats for use in signature workflows.
    """

    date_formats = [
        "d-m-Y",
        "d/m/Y",
        "d.m.Y",
        "Y-m-d",
        "Y/m/d",
        "Y.m.d",
        "m-d-Y",
        "m/d/Y",
        "m.d.Y",
    ]
