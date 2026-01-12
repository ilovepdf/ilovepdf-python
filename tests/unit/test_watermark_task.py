# pylint: disable=too-many-public-methods
"""Unit tests for the WatermarkTask class in the ilovepdf package."""

import pytest

from ilovepdf import WatermarkTask


class TestWatermarkTask:
    """Test suite for the WatermarkTask class."""

    @pytest.fixture
    def watermark_task(self):
        """Fixture that creates a WatermarkTask instance for testing."""
        task = WatermarkTask("public_key", "secret_key", make_start=False)
        return task

    def test_initialization_sets_default_values(self, watermark_task):
        """
        Ensure WatermarkTask is initialized with default values.
        """
        assert watermark_task.tool == "watermark"
        assert watermark_task.mode == "text"
        assert watermark_task.text is None
        assert watermark_task.image is None
        assert watermark_task.pages == "all"
        assert watermark_task.vertical_position == "middle"
        assert watermark_task.horizontal_position == "center"
        assert watermark_task.vertical_position_adjustment == 0
        assert watermark_task.horizontal_position_adjustment == 0
        assert watermark_task.mosaic is False
        assert watermark_task.rotation == 0
        assert watermark_task.font_family == "Arial Unicode MS"
        assert watermark_task.font_style is None
        assert watermark_task.font_size == 14
        assert watermark_task.font_color == "#000000"
        assert watermark_task.transparency == 100
        assert watermark_task.layer == "above"

    def test_trivial_setters_and_getters(self, watermark_task):
        """
        Test trivial setters and getters that do not have validation logic.
        """
        watermark_task.text = "Confidential"
        assert watermark_task.text == "Confidential"
        watermark_task.image = "logo.png"
        assert watermark_task.image == "logo.png"
        watermark_task.pages = "1,3,5"
        assert watermark_task.pages == "1,3,5"
        watermark_task.vertical_position_adjustment = 10
        assert watermark_task.vertical_position_adjustment == 10
        watermark_task.horizontal_position_adjustment = -5
        assert watermark_task.horizontal_position_adjustment == -5
        watermark_task.mosaic = True
        assert watermark_task.mosaic is True
        watermark_task.mosaic = False
        assert watermark_task.mosaic is False
        watermark_task.font_size = 20
        assert watermark_task.font_size == 20
        watermark_task.font_color = "#FF0000"
        assert watermark_task.font_color == "#FF0000"

    @pytest.mark.parametrize("mode", ["text", "image"])
    def test_mode_setter_valid(self, watermark_task, mode):
        watermark_task.mode = mode
        assert watermark_task.mode == mode

    @pytest.mark.parametrize("invalid_mode", ["audio", "video", "", None])
    def test_mode_setter_invalid(self, watermark_task, invalid_mode):
        with pytest.raises(ValueError):
            watermark_task.mode = invalid_mode

    @pytest.mark.parametrize("pos", ["bottom", "top", "middle"])
    def test_vertical_position_setter_valid(self, watermark_task, pos):
        watermark_task.vertical_position = pos
        assert watermark_task.vertical_position == pos

    @pytest.mark.parametrize("invalid_pos", ["center", "up", "", None])
    def test_vertical_position_setter_invalid(self, watermark_task, invalid_pos):
        with pytest.raises(ValueError):
            watermark_task.vertical_position = invalid_pos

    @pytest.mark.parametrize("pos", ["left", "center", "right"])
    def test_horizontal_position_setter_valid(self, watermark_task, pos):
        watermark_task.horizontal_position = pos
        assert watermark_task.horizontal_position == pos

    @pytest.mark.parametrize("invalid_pos", ["middle", "down", "", None])
    def test_horizontal_position_setter_invalid(self, watermark_task, invalid_pos):
        with pytest.raises(ValueError):
            watermark_task.horizontal_position = invalid_pos

    @pytest.mark.parametrize("angle", [0, 90, 180, 360])
    def test_rotation_setter_valid(self, watermark_task, angle):
        watermark_task.rotation = angle
        assert watermark_task.rotation == angle

    @pytest.mark.parametrize("invalid_angle", [-1, 361, 999])
    def test_rotation_setter_invalid(self, watermark_task, invalid_angle):
        with pytest.raises(ValueError):
            watermark_task.rotation = invalid_angle

    @pytest.mark.parametrize(
        "family",
        [
            "Arial",
            "Arial Unicode MS",
            "Verdana",
            "Courier",
            "Times New Roman",
            "Comic Sans MS",
            "WenQuanYi Zen Hei",
            "Lohit Marathi",
        ],
    )
    def test_font_family_setter_valid(self, watermark_task, family):
        watermark_task.font_family = family
        assert watermark_task.font_family == family

    @pytest.mark.parametrize("invalid_family", ["Helvetica", "Comic", "", None])
    def test_font_family_setter_invalid(self, watermark_task, invalid_family):
        with pytest.raises(ValueError):
            watermark_task.font_family = invalid_family

    @pytest.mark.parametrize("style", [None, "Bold", "Italic"])
    def test_font_style_setter_valid(self, watermark_task, style):
        watermark_task.font_style = style
        assert watermark_task.font_style == style

    @pytest.mark.parametrize("invalid_style", ["bold", "regular", "underline", 123])
    def test_font_style_setter_invalid(self, watermark_task, invalid_style):
        with pytest.raises(ValueError):
            watermark_task.font_style = invalid_style

    @pytest.mark.parametrize("transparency", [1, 50, 100])
    def test_transparency_setter_valid(self, watermark_task, transparency):
        watermark_task.transparency = transparency
        assert watermark_task.transparency == transparency

    @pytest.mark.parametrize("invalid_transparency", [0, 101, -5])
    def test_transparency_setter_invalid(self, watermark_task, invalid_transparency):
        with pytest.raises(ValueError):
            watermark_task.transparency = invalid_transparency

    @pytest.mark.parametrize("layer", ["above", "below"])
    def test_layer_setter_valid(self, watermark_task, layer):
        watermark_task.layer = layer
        assert watermark_task.layer == layer

    @pytest.mark.parametrize("invalid_layer", ["over", "under", "", None])
    def test_layer_setter_invalid(self, watermark_task, invalid_layer):
        with pytest.raises(ValueError):
            watermark_task.layer = invalid_layer

    def test_to_dict_requires_text_for_text_mode(self, watermark_task):
        watermark_task.mode = "text"
        watermark_task.text = None
        with pytest.raises(ValueError):
            watermark_task._to_dict()  # pylint: disable=protected-access
        watermark_task.text = "Watermark"
        result = watermark_task._to_dict()  # pylint: disable=protected-access
        assert result["text"] == "Watermark"

    def test_to_dict_requires_image_for_image_mode(self, watermark_task):
        watermark_task.mode = "image"
        watermark_task.image = None
        with pytest.raises(ValueError):
            watermark_task._to_dict()  # pylint: disable=protected-access
        watermark_task.image = "logo.png"
        result = watermark_task._to_dict()  # pylint: disable=protected-access
        assert result["image"] == "logo.png"

    def test_to_dict_filters_none_values(self, watermark_task):
        # Case 1: mode 'text', image=None
        watermark_task.mode = "text"
        watermark_task.text = "Watermark"
        watermark_task.image = None
        result = watermark_task._to_dict()  # pylint: disable=protected-access
        assert "image" not in result

        # Case 2: mode 'image', text=None
        watermark_task.mode = "image"
        watermark_task.text = None
        watermark_task.image = "logo.png"
        result = watermark_task._to_dict()  # pylint: disable=protected-access
        assert "text" not in result
