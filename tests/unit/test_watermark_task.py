"""Unit tests for the WatermarkTask class in the ilovepdf module.

These tests verify initialization defaults, property validation, and payload
serialization for WatermarkTask.
"""

import pytest

from ilovepdf import WatermarkTask
from ilovepdf.exceptions import IntOutOfRangeError, InvalidChoiceError
from ilovepdf.exceptions.int_errors import NotAnIntError
from ilovepdf.watermark_task import (
    FONT_FAMILY_OPTIONS,
    FONT_STYLE_OPTIONS,
    HORIZONTAL_POSITION_OPTIONS,
    LAYER_OPTIONS,
    VERTICAL_POSITION_OPTIONS,
    WATERMARK_MODE_OPTIONS,
)

from .base_test import AbstractUnitTaskTest


# pylint: disable=protected-access,too-many-public-methods)
class TestWatermarkTask(AbstractUnitTaskTest):
    """Unit tests for WatermarkTask behavior and validation."""

    _task_class = WatermarkTask
    _task_tool = "watermark"

    def test_initialization_sets_default_values(self, my_task):
        """Validate default payload and property values after initialization."""

        assert my_task._DEFAULT_PAYLOAD == {
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
        assert my_task.mode == "text"
        assert my_task.text is None
        assert my_task.image is None
        assert my_task.pages == "all"
        assert my_task.vertical_position == "middle"
        assert my_task.horizontal_position == "center"
        assert my_task.vertical_position_adjustment == 0
        assert my_task.horizontal_position_adjustment == 0
        assert my_task.mosaic is False
        assert my_task.rotation == 0
        assert my_task.font_family == "Arial Unicode MS"
        assert my_task.font_style is None
        assert my_task.font_size == 14
        assert my_task.font_color == "#000000"
        assert my_task.transparency == 100
        assert my_task.layer == "above"

    @pytest.mark.parametrize("mode", WATERMARK_MODE_OPTIONS)
    def test_mode_accepts_valid_options(self, my_task, mode):
        """Ensure watermark mode accepts allowed values."""

        my_task.mode = mode
        assert my_task.mode == mode

    @pytest.mark.parametrize("mode", ["", "audio", "video", None])
    def test_mode_rejects_invalid_options(self, my_task, mode):
        """Ensure invalid watermark modes raise InvalidChoiceError."""

        with pytest.raises(InvalidChoiceError):
            my_task.mode = mode  # type: ignore[assignment]

    def test_text_accepts_strings_and_none(self, my_task):
        """Verify text setter allows strings and resets to None."""

        my_task.text = "Confidential"
        assert my_task.text == "Confidential"
        my_task.text = None
        assert my_task.text is None

    @pytest.mark.parametrize("value", [123, 1.2, object()])
    def test_text_rejects_non_string_values(self, my_task, value):
        """Ensure non-string text values raise TypeError."""

        with pytest.raises(TypeError):
            my_task.text = value  # type: ignore[assignment]

    def test_text_rejects_empty_string(self, my_task):
        """Ensure empty strings raise ValueError for text."""

        with pytest.raises(ValueError):
            my_task.text = ""

    def test_image_accepts_strings_and_none(self, my_task):
        """Verify image setter allows strings and resets to None."""

        my_task.image = "server_filename"
        assert my_task.image == "server_filename"
        my_task.image = None
        assert my_task.image is None

    @pytest.mark.parametrize("value", [123, 1.2, object()])
    def test_image_rejects_non_string_values(self, my_task, value):
        """Ensure non-string image values raise TypeError."""

        with pytest.raises(TypeError):
            my_task.image = value  # type: ignore[assignment]

    def test_image_rejects_empty_string(self, my_task):
        """Ensure empty strings raise ValueError for image."""

        with pytest.raises(ValueError):
            my_task.image = ""

    def test_pages_accepts_string(self, my_task):
        """Ensure setting pages with a valid string succeeds."""

        my_task.pages = "1,3,5"
        assert my_task.pages == "1,3,5"

    @pytest.mark.parametrize("value", [123, None])
    def test_pages_rejects_non_string(self, my_task, value):
        """Ensure non-string pages values raise TypeError."""

        with pytest.raises(TypeError):
            my_task.pages = value  # type: ignore[assignment]

    def test_pages_rejects_empty_string(self, my_task):
        """Ensure empty page expression raises ValueError."""

        with pytest.raises(ValueError):
            my_task.pages = ""

    @pytest.mark.parametrize("value", VERTICAL_POSITION_OPTIONS)
    def test_vertical_position_accepts_valid_options(self, my_task, value):
        """Ensure vertical position accepts allowed options."""

        my_task.vertical_position = value
        assert my_task.vertical_position == value

    @pytest.mark.parametrize("value", ["upper", "center", None])
    def test_vertical_position_rejects_invalid_options(self, my_task, value):
        """Ensure invalid vertical positions raise InvalidChoiceError."""

        with pytest.raises(InvalidChoiceError):
            my_task.vertical_position = value  # type: ignore[assignment]

    @pytest.mark.parametrize("value", HORIZONTAL_POSITION_OPTIONS)
    def test_horizontal_position_accepts_valid_options(self, my_task, value):
        """Ensure horizontal position accepts allowed options."""

        my_task.horizontal_position = value
        assert my_task.horizontal_position == value

    @pytest.mark.parametrize("value", ["middle", "center-left", None])
    def test_horizontal_position_rejects_invalid_options(self, my_task, value):
        """Ensure invalid horizontal positions raise InvalidChoiceError."""

        with pytest.raises(InvalidChoiceError):
            my_task.horizontal_position = value  # type: ignore[assignment]

    @pytest.mark.parametrize("value", [-1000, 0, 1000])
    def test_vertical_adjustment_accepts_range(self, my_task, value):
        """Ensure vertical adjustment accepts values within allowed range."""

        my_task.vertical_position_adjustment = value
        assert my_task.vertical_position_adjustment == value

    def test_vertical_adjustment_rejects_non_int(self, my_task):
        """Ensure non-integer adjustments raise NotAnIntError."""

        with pytest.raises(NotAnIntError):
            my_task.vertical_position_adjustment = 1.5  # type: ignore[assignment]

    @pytest.mark.parametrize("value", [-1001, 1001])
    def test_vertical_adjustment_rejects_out_of_range(self, my_task, value):
        """Ensure out-of-range adjustments raise IntOutOfRangeError."""

        with pytest.raises(IntOutOfRangeError):
            my_task.vertical_position_adjustment = value

    @pytest.mark.parametrize("value", [-1000, 0, 1000])
    def test_horizontal_adjustment_accepts_range(self, my_task, value):
        """Ensure horizontal adjustment accepts values within allowed range."""

        my_task.horizontal_position_adjustment = value
        assert my_task.horizontal_position_adjustment == value

    def test_horizontal_adjustment_rejects_non_int(self, my_task):
        """Ensure non-integer horizontal adjustments raise NotAnIntError."""

        with pytest.raises(NotAnIntError):
            my_task.horizontal_position_adjustment = "1"  # type: ignore[assignment]

    @pytest.mark.parametrize("value", [-1001, 1001])
    def test_horizontal_adjustment_rejects_out_of_range(self, my_task, value):
        """Ensure out-of-range horizontal adjustments raise IntOutOfRangeError."""

        with pytest.raises(IntOutOfRangeError):
            my_task.horizontal_position_adjustment = value

    @pytest.mark.parametrize("value", [True, False])
    def test_mosaic_accepts_boolean(self, my_task, value):
        """Ensure mosaic setter accepts boolean values."""

        my_task.mosaic = value
        assert my_task.mosaic is value

    @pytest.mark.parametrize("value", ["true", 1, None])
    def test_mosaic_rejects_non_boolean(self, my_task, value):
        """Ensure non-boolean mosaic values raise InvalidChoiceError."""

        with pytest.raises(InvalidChoiceError):
            my_task.mosaic = value  # type: ignore[assignment]

    @pytest.mark.parametrize("value", [0, 90, 180, 270, 360])
    def test_rotation_accepts_range(self, my_task, value):
        """Ensure rotation accepts the inclusive range 0-360."""

        my_task.rotation = value
        assert my_task.rotation == value

    def test_rotation_rejects_non_int(self, my_task):
        """Ensure non-integer rotation raises NotAnIntError."""

        with pytest.raises(NotAnIntError):
            my_task.rotation = "90"  # type: ignore[assignment]

    @pytest.mark.parametrize("value", [-1, 361])
    def test_rotation_rejects_out_of_range(self, my_task, value):
        """Ensure rotation outside 0-360 raises IntOutOfRangeError."""

        with pytest.raises(IntOutOfRangeError):
            my_task.rotation = value

    @pytest.mark.parametrize("value", FONT_FAMILY_OPTIONS)
    def test_font_family_accepts_valid_options(self, my_task, value):
        """Ensure font family accepts allowed options."""

        my_task.font_family = value
        assert my_task.font_family == value

    @pytest.mark.parametrize("value", ["Helvetica", "Comic", None])
    def test_font_family_rejects_invalid_options(self, my_task, value):
        """Ensure invalid font families raise InvalidChoiceError."""

        with pytest.raises(InvalidChoiceError):
            my_task.font_family = value  # type: ignore[assignment]

    @pytest.mark.parametrize("value", FONT_STYLE_OPTIONS)
    def test_font_style_accepts_valid_options(self, my_task, value):
        """Ensure font style accepts allowed options."""

        my_task.font_style = value
        assert my_task.font_style == value

    @pytest.mark.parametrize("value", ["bold", "regular", 1])
    def test_font_style_rejects_invalid_options(self, my_task, value):
        """Ensure invalid font styles raise InvalidChoiceError."""

        with pytest.raises(InvalidChoiceError):
            my_task.font_style = value  # type: ignore[assignment]

    @pytest.mark.parametrize("value", [1, 14, 500])
    def test_font_size_accepts_range(self, my_task, value):
        """Ensure font size accepts values within the allowed range."""

        my_task.font_size = value
        assert my_task.font_size == value

    def test_font_size_rejects_non_int(self, my_task):
        """Ensure non-integer font sizes raise NotAnIntError."""

        with pytest.raises(NotAnIntError):
            my_task.font_size = 10.5  # type: ignore[assignment]

    @pytest.mark.parametrize("value", [0, 501])
    def test_font_size_rejects_out_of_range(self, my_task, value):
        """Ensure font sizes outside 1-500 raise IntOutOfRangeError."""

        with pytest.raises(IntOutOfRangeError):
            my_task.font_size = value

    def test_font_color_accepts_string(self, my_task):
        """Ensure valid font color strings are accepted."""

        my_task.font_color = "#FF00FF"
        assert my_task.font_color == "#FF00FF"

    @pytest.mark.parametrize("value", [123, None])
    def test_font_color_rejects_non_string(self, my_task, value):
        """Ensure non-string font colors raise TypeError."""

        with pytest.raises(TypeError):
            my_task.font_color = value  # type: ignore[assignment]

    def test_font_color_rejects_empty_string(self, my_task):
        """Ensure empty font color strings raise ValueError."""

        with pytest.raises(ValueError):
            my_task.font_color = ""

    @pytest.mark.parametrize("value", [1, 50, 100])
    def test_transparency_accepts_range(self, my_task, value):
        """Ensure transparency accepts values within 1-100."""

        my_task.transparency = value
        assert my_task.transparency == value

    def test_transparency_rejects_non_int(self, my_task):
        """Ensure non-integer transparency raises NotAnIntError."""

        with pytest.raises(NotAnIntError):
            my_task.transparency = 50.0  # type: ignore[assignment]

    @pytest.mark.parametrize("value", [0, 101])
    def test_transparency_rejects_out_of_range(self, my_task, value):
        """Ensure transparency outside 1-100 raises IntOutOfRangeError."""

        with pytest.raises(IntOutOfRangeError):
            my_task.transparency = value

    @pytest.mark.parametrize("value", LAYER_OPTIONS)
    def test_layer_accepts_valid_options(self, my_task, value):
        """Ensure layer accepts allowed options."""

        my_task.layer = value
        assert my_task.layer == value

    @pytest.mark.parametrize("value", ["over", "under", None])
    def test_layer_rejects_invalid_options(self, my_task, value):
        """Ensure invalid layers raise InvalidChoiceError."""

        with pytest.raises(InvalidChoiceError):
            my_task.layer = value  # type: ignore[assignment]

    def test_to_payload_requires_text_in_text_mode(self, my_task):
        """Ensure text mode requires a text value when building payload."""

        my_task.mode = "text"
        my_task.text = None
        with pytest.raises(InvalidChoiceError):
            my_task._to_payload()
        my_task.text = "Draft"
        payload = my_task._to_payload()
        assert payload["text"] == "Draft"
        assert "image" not in payload

    def test_to_payload_requires_image_in_image_mode(self, my_task):
        """Ensure image mode requires an image value when building payload."""

        my_task.mode = "image"
        my_task.image = None
        with pytest.raises(InvalidChoiceError):
            my_task._to_payload()
        my_task.image = "server_file"
        payload = my_task._to_payload()
        assert payload["image"] == "server_file"
        assert "text" not in payload

    def test_to_payload_filters_none_values(self, my_task):
        """Ensure payload excludes keys with None values."""

        my_task.mode = "text"
        my_task.text = "Draft"
        my_task.image = None
        payload_text = my_task._to_payload()
        assert "image" not in payload_text

        my_task.mode = "image"
        my_task.text = None
        my_task.image = "server_file"
        payload_image = my_task._to_payload()
        assert "text" not in payload_image
