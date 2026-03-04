"""
Helper functions and type definitions for the iLovePDF Python library.
"""

from typing import Literal

# Define type literals and options for various attributes used in the library

FontFamilyType = Literal[
    "Arial",
    "Arial Unicode MS",
    "Verdana",
    "Courier",
    "Times New Roman",
    "Comic Sans MS",
    "WenQuanYi Zen Hei",
    "Lohit Marathi",
]

FONT_FAMILY_OPTIONS = {
    "Arial",
    "Arial Unicode MS",
    "Verdana",
    "Courier",
    "Times New Roman",
    "Comic Sans MS",
    "WenQuanYi Zen Hei",
    "Lohit Marathi",
}

FontStyleType = Literal[None, "Bold", "Italic"]
FONT_STYLE_OPTIONS = {None, "Bold", "Italic"}

LayerType = Literal["above", "below"]
LAYER_OPTIONS = {"above", "below"}


IMAGE_FILE_EXTENSIONS = ["jpg", "jpeg", "png", "gif", "bmp", "tiff", "tif", "webp"]
