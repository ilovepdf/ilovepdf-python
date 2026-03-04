"""Handles PDF watermark tasks using the iLovePDF API.

Provides the WatermarkTask class to configure text or image watermarks,
including positioning, typography, and rendering options.
"""

from typing import Any, Literal

from .exceptions import IntOutOfRangeError, InvalidChoiceError
from .file import File
from .helpers import (
    FONT_FAMILY_OPTIONS,
    FONT_STYLE_OPTIONS,
    IMAGE_FILE_EXTENSIONS,
    LAYER_OPTIONS,
    FontFamilyType,
    FontStyleType,
    LayerType,
)
from .task import Task
from .validators import BoolValidator, ChoiceValidator, IntValidator, StringValidator

WatermarkModeType = Literal["text", "image"]
WATERMARK_MODE_OPTIONS = {"text", "image"}

VerticalPositionType = Literal["bottom", "top", "middle"]
VERTICAL_POSITION_OPTIONS = {"bottom", "top", "middle"}

HorizontalPositionType = Literal["left", "center", "right"]
HORIZONTAL_POSITION_OPTIONS = {"left", "center", "right"}


class WatermarkTask(Task):
    """Configure and execute watermark tasks using the iLovePDF API.

    WatermarkTask allows adding text or image watermarks on PDF files with
    extensive customization. Users can adjust positioning, rotation, typography,
    color, transparency, and layering before executing the task.

    Args:
        public_key (str | None): API public key. Uses ``ILOVEPDF_PUBLIC_KEY`` when
            omitted.
        secret_key (str | None): API secret key. Uses ``ILOVEPDF_SECRET_KEY`` when
            omitted.
        make_start (bool): Whether to start the task immediately. Default is False.

    Example:
        task = WatermarkTask(public_key="your_public_key", secret_key="your_secret_key")
        task.add_file("/path/to/document.pdf")
        task.mode = "text"
        task.text = "Confidential"
        task.font_size = 28
        task.transparency = 60
        task.execute()
        task.download("/path/to/output.pdf")
    """

    _tool = "watermark"

    _DEFAULT_PAYLOAD = {
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

    allowed_extensions = ["pdf"]

    @property
    def mode(self) -> WatermarkModeType:
        """Gets the current watermark mode. Default is "text"."""

        return self._get_attr("mode")

    @mode.setter
    def mode(self, value: WatermarkModeType) -> None:
        """Sets the watermark mode.

        Args:
            value (WatermarkModeType): Must be one of WATERMARK_MODE_OPTIONS.
        """

        ChoiceValidator.validate(value, WATERMARK_MODE_OPTIONS, "mode")
        self._set_attr("mode", value)

    @property
    def text(self) -> str | None:
        """Gets the text used for text watermarks. Default is None."""

        return self._get_attr("text")

    @text.setter
    def text(self, value: str | None) -> None:
        """Sets the text used for text watermarks.

        Args:
            value (str | None): Must be a non-empty string when provided.
        """

        if value is None:
            self._set_attr("text", None)
            return
        StringValidator.validate(value, "text")
        self._set_attr("text", value)

    def set_watermark_image(self, file_path: str, **kwargs: Any) -> File:
        """
        Uploads and sets an image file to be used as a watermark.

        This method validates the image file extension, uploads it to the server,
        and configures it as the watermark image for the task.

        Args:
            file_path (str): Path to the image file to use as watermark.
            **kwargs (Any): Additional arguments to pass to the upload method.

        Returns:
            File: The uploaded file object with server filename information.

        Raises:
            ValueError: If the file extension is not valid for images.
            ProcessingError: If the task has not been started yet.

        Example:
            >>> task = WatermarkTask(public_key, secret_key)
            >>> task.start()
            >>> watermark_file = task.set_watermark_image('/path/to/logo.png')
        """
        file = self._validate_and_upload_file(
            file_path, extension_list=IMAGE_FILE_EXTENSIONS, **kwargs
        )
        self.image = file.server_filename
        return file

    @property
    def image(self) -> str | None:
        """Gets the server filename used for image watermarks. Default is None."""

        return self._get_attr("image")

    @image.setter
    def image(self, value: str | None) -> None:
        """Sets the server filename for image watermarks.

        Args:
            value (str | None): Must be a non-empty string when provided.
        """

        if value is None:
            self._set_attr("image", None)
            return
        StringValidator.validate(value, "image")
        self._set_attr("image", value)

    @property
    def pages(self) -> str:
        """Gets the page selection string. Default is "all"."""

        return self._get_attr("pages")

    @pages.setter
    def pages(self, value: str) -> None:
        """Sets the page selection string.

        Args:
            value (str): Page selection expression (e.g., "all", "1,3,5", "2-4").
        """

        StringValidator.validate(value, "pages")
        self._set_attr("pages", value)

    @property
    def vertical_position(self) -> VerticalPositionType:
        """Gets the vertical position. Default is "middle"."""

        return self._get_attr("vertical_position")

    @vertical_position.setter
    def vertical_position(self, value: VerticalPositionType) -> None:
        """Sets the vertical position.

        Args:
            value (VerticalPositionType): Must be one of VERTICAL_POSITION_OPTIONS.
        """

        ChoiceValidator.validate(value, VERTICAL_POSITION_OPTIONS, "vertical_position")
        self._set_attr("vertical_position", value)

    @property
    def horizontal_position(self) -> HorizontalPositionType:
        """Gets the horizontal position. Default is "center"."""

        return self._get_attr("horizontal_position")

    @horizontal_position.setter
    def horizontal_position(self, value: HorizontalPositionType) -> None:
        """Sets the horizontal position.

        Args:
            value (HorizontalPositionType): Must be one of HORIZONTAL_POSITION_OPTIONS.
        """

        ChoiceValidator.validate(
            value, HORIZONTAL_POSITION_OPTIONS, "horizontal_position"
        )
        self._set_attr("horizontal_position", value)

    @property
    def vertical_position_adjustment(self) -> int:
        """Gets the vertical adjustment in pixels. Default is 0."""

        return self._get_attr("vertical_position_adjustment")

    @vertical_position_adjustment.setter
    def vertical_position_adjustment(self, value: int) -> None:
        """Sets the vertical adjustment in pixels.

        Args:
            value (int): Must be between -1000 and 1000 inclusive.
        """

        IntValidator.validate_type(value, "vertical_position_adjustment")
        if not -1000 <= value <= 1000:
            raise IntOutOfRangeError(
                "vertical_position_adjustment must be between -1000 and 1000."
            )
        self._set_attr("vertical_position_adjustment", value)

    @property
    def horizontal_position_adjustment(self) -> int:
        """Gets the horizontal adjustment in pixels. Default is 0."""

        return self._get_attr("horizontal_position_adjustment")

    @horizontal_position_adjustment.setter
    def horizontal_position_adjustment(self, value: int) -> None:
        """Sets the horizontal adjustment in pixels.

        Args:
            value (int): Must be between -1000 and 1000 inclusive.
        """

        IntValidator.validate_type(value, "horizontal_position_adjustment")
        if not -1000 <= value <= 1000:
            raise IntOutOfRangeError(
                "horizontal_position_adjustment must be between -1000 and 1000."
            )
        self._set_attr("horizontal_position_adjustment", value)

    @property
    def mosaic(self) -> bool:
        """Gets the mosaic flag. Default is False."""

        return self._get_attr("mosaic")

    @mosaic.setter
    def mosaic(self, value: bool) -> None:
        """Sets the mosaic flag.

        Args:
            value (bool): Must be a boolean.
        """

        BoolValidator.validate(value, "mosaic")
        self._set_attr("mosaic", value)

    @property
    def rotation(self) -> int:
        """Gets the rotation angle in degrees. Default is 0."""

        return self._get_attr("rotation")

    @rotation.setter
    def rotation(self, value: int) -> None:
        """Sets the rotation angle in degrees.

        Args:
            value (int): Must be between 0 and 360 inclusive.
        """

        IntValidator.validate_range(value, 0, 360, "rotation")
        self._set_attr("rotation", value)

    @property
    def font_family(self) -> FontFamilyType:
        """Gets the font family. Default is "Arial Unicode MS"."""

        return self._get_attr("font_family")

    @font_family.setter
    def font_family(self, value: FontFamilyType) -> None:
        """Sets the font family.

        Args:
            value (FontFamilyType): Must be one of FONT_FAMILY_OPTIONS.
        """

        ChoiceValidator.validate(value, FONT_FAMILY_OPTIONS, "font_family")
        self._set_attr("font_family", value)

    @property
    def font_style(self) -> FontStyleType:
        """Gets the font style. Default is None."""

        return self._get_attr("font_style")

    @font_style.setter
    def font_style(self, value: FontStyleType) -> None:
        """Sets the font style.

        Args:
            value (FontStyleType): Must be one of FONT_STYLE_OPTIONS.
        """

        ChoiceValidator.validate(value, FONT_STYLE_OPTIONS, "font_style")
        self._set_attr("font_style", value)

    @property
    def font_size(self) -> int:
        """Gets the font size in points. Default is 14."""

        return self._get_attr("font_size")

    @font_size.setter
    def font_size(self, value: int) -> None:
        """Sets the font size in points.

        Args:
            value (int): Must be between 1 and 500 inclusive.
        """

        IntValidator.validate_range(value, 1, 500, "font_size")
        self._set_attr("font_size", value)

    @property
    def font_color(self) -> str:
        """Gets the font color in hexadecimal format. Default is "#000000"."""

        return self._get_attr("font_color")

    @font_color.setter
    def font_color(self, value: str) -> None:
        """Sets the font color in hexadecimal format.

        Args:
            value (str): Must be a valid non-empty string.
        """

        StringValidator.validate(value, "font_color")
        self._set_attr("font_color", value)

    @property
    def transparency(self) -> int:
        """Gets the transparency percentage. Default is 100."""

        return self._get_attr("transparency")

    @transparency.setter
    def transparency(self, value: int) -> None:
        """Sets the transparency percentage.

        Args:
            value (int): Must be between 1 and 100 inclusive.
        """

        IntValidator.validate_range(value, 1, 100, "transparency")
        self._set_attr("transparency", value)

    @property
    def layer(self) -> LayerType:
        """Gets the layer setting. Default is "above"."""

        return self._get_attr("layer")

    @layer.setter
    def layer(self, value: LayerType) -> None:
        """Sets the layer setting.

        Args:
            value (LayerType): Must be one of LAYER_OPTIONS.
        """

        ChoiceValidator.validate(value, LAYER_OPTIONS, "layer")
        self._set_attr("layer", value)

    def _to_payload(self) -> dict:
        """Serializes the watermark configuration for API submission."""

        payload = super()._to_payload()
        mode = payload.get("mode")
        if mode == "text" and not payload.get("text"):
            raise InvalidChoiceError("Text value must be provided for text watermark.")
        if mode == "image" and not payload.get("image"):
            raise InvalidChoiceError(
                "Image value must be provided for image watermark."
            )
        payload = {key: value for key, value in payload.items() if value is not None}
        return payload
