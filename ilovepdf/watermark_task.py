"""
This module defines the WatermarkTask class for interacting with the iLovePDF API
to add text or image watermarks to PDF documents.
"""

from typing import Literal, Optional

from .task import ProcessTask

MODE_VALID = ("text", "image")
ModeType = Literal["text", "image"]

VERTICAL_POSITION_VALID = ("bottom", "top", "middle")
HORIZONTAL_POSITION_VALID = ("left", "center", "right")
FONT_FAMILY_VALID = (
    "Arial",
    "Arial Unicode MS",
    "Verdana",
    "Courier",
    "Times New Roman",
    "Comic Sans MS",
    "WenQuanYi Zen Hei",
    "Lohit Marathi",
)
FONT_STYLE_VALID = (None, "Bold", "Italic")
LAYER_VALID = ("above", "below")


class WatermarkTask(ProcessTask):
    """
    Class for the watermark task using the iLovePDF API.
    """

    DEFAULTS_VALUES = {
        "mode": "text",
        "text": None,
        "image": None,
        "pages": "all",
        "vertical_position": "middle",
        "horizontal_position": "center",
        "vertical_position_adjustment": 0,
        "horizontal_position_adjustment": 0,
        "mosaic": False,
        "rotation": 0,
        "font_family": "Arial Unicode MS",
        "font_style": None,
        "font_size": 14,
        "font_color": "#000000",
        "transparency": 100,
        "layer": "above",
    }

    def __init__(self, public_key=None, secret_key=None, make_start=True):
        super().__init__(public_key, secret_key, make_start, tool="watermark")

    @property
    def mode(self) -> str:
        return self._params.get("mode", "text")

    @mode.setter
    def mode(self, mode: ModeType):
        """
        Set the watermark mode for the task.

        Accepted values: "text", "image".
        Default: "text"
        """
        if mode not in MODE_VALID:
            raise ValueError("Invalid mode")
        self._params["mode"] = mode

    @property
    def text(self) -> Optional[str]:
        return self._params.get("text", None)

    @text.setter
    def text(self, value: str):
        """
        Text to be stamped. Required if mode is "text".
        """
        self._params["text"] = value

    @property
    def image(self) -> Optional[str]:
        return self._params.get("image", None)

    @image.setter
    def image(self, value: str):
        """
        The image to stamp if mode is "image".
        Must refer to the server_filename (JPG or PNG).
        """
        self._params["image"] = value

    @property
    def pages(self) -> str:
        return self._params.get("pages", "all")

    @pages.setter
    def pages(self, value: str):
        """
        Pages to be stamped. Examples: "all", "3-end", "1,3,4-9".
        Default: "all"
        """
        self._params["pages"] = value

    @property
    def vertical_position(self) -> str:
        return self._params.get("vertical_position", "middle")

    @vertical_position.setter
    def vertical_position(self, value: str):
        """
        Vertical position: "bottom", "top", "middle". Default: "middle"
        """
        if value not in VERTICAL_POSITION_VALID:
            raise ValueError("Invalid vertical_position")
        self._params["vertical_position"] = value

    @property
    def horizontal_position(self) -> str:
        return self._params.get("horizontal_position", "center")

    @horizontal_position.setter
    def horizontal_position(self, value: str):
        """
        Horizontal position: "left", "center", "right". Default: "center"
        """
        if value not in HORIZONTAL_POSITION_VALID:
            raise ValueError("Invalid horizontal_position")
        self._params["horizontal_position"] = value

    @property
    def vertical_position_adjustment(self) -> int:
        return self._params.get("vertical_position_adjustment", 0)

    @vertical_position_adjustment.setter
    def vertical_position_adjustment(self, value: int):
        """
        Offset pixels from vertical position. Accepts positive/negative values.
        """
        self._params["vertical_position_adjustment"] = int(value)

    @property
    def horizontal_position_adjustment(self) -> int:
        return self._params.get("horizontal_position_adjustment", 0)

    @horizontal_position_adjustment.setter
    def horizontal_position_adjustment(self, value: int):
        """
        Offset pixels from horizontal position. Accepts positive/negative values.
        """
        self._params["horizontal_position_adjustment"] = int(value)

    @property
    def mosaic(self) -> bool:
        return self._params.get("mosaic", False)

    @mosaic.setter
    def mosaic(self, value: bool):
        """
        If true, stamps the image or text 9 times per page. Default: False
        """
        self._params["mosaic"] = bool(value)

    @property
    def rotation(self) -> int:
        return self._params.get("rotation", 0)

    @rotation.setter
    def rotation(self, value: int):
        """
        Angle of rotation (0-360). Default: 0
        """
        if not 0 <= int(value) <= 360:
            raise ValueError("rotation must be between 0 and 360")
        self._params["rotation"] = int(value)

    @property
    def font_family(self) -> str:
        return self._params.get("font_family", "Arial Unicode MS")

    @font_family.setter
    def font_family(self, value: str):
        """
        Font family. Default: "Arial Unicode MS"
        """
        if value not in FONT_FAMILY_VALID:
            raise ValueError("Invalid font_family")
        self._params["font_family"] = value

    @property
    def font_style(self) -> Optional[str]:
        return self._params.get("font_style", None)

    @font_style.setter
    def font_style(self, value: Optional[str]):
        """
        Font style: None (Regular), "Bold", "Italic". Default: None
        """
        if value not in FONT_STYLE_VALID:
            raise ValueError("Invalid font_style")
        self._params["font_style"] = value

    @property
    def font_size(self) -> int:
        return self._params.get("font_size", 14)

    @font_size.setter
    def font_size(self, value: int):
        """
        Font size. Default: 14
        """
        self._params["font_size"] = int(value)

    @property
    def font_color(self) -> str:
        return self._params.get("font_color", "#000000")

    @font_color.setter
    def font_color(self, value: str):
        """
        Hexadecimal font color. Default: "#000000"
        """
        self._params["font_color"] = value

    @property
    def transparency(self) -> int:
        return self._params.get("transparency", 100)

    @transparency.setter
    def transparency(self, value: int):
        """
        Opacity percentage (1-100). Default: 100
        """
        if not 1 <= int(value) <= 100:
            raise ValueError("transparency must be between 1 and 100")
        self._params["transparency"] = int(value)

    @property
    def layer(self) -> str:
        return self._params.get("layer", "above")

    @layer.setter
    def layer(self, value: str):
        """
        Layer: "above" (over content), "below" (below content). Default: "above"
        """
        if value not in LAYER_VALID:
            raise ValueError("Invalid layer")
        self._params["layer"] = value

    def _to_dict(self):
        data = super()._to_dict()
        if data.get("mode") == "text" and not data.get("text"):
            raise ValueError("Text is required when mode is 'text'")
        if data.get("mode") == "image" and not data.get("image"):
            raise ValueError("Image is required when mode is 'image'")
        return {k: v for k, v in data.items() if v is not None}
