"""Integration tests for EditPdfTask using the iLovePDF API.

Covers:
- Full workflow: add an element, set parameters, execute, and download results.
"""

from ilovepdf import EditPdfTask

from .base_task_integration_test import BaseTaskIntegrationTest


class TestEditPdfTaskIntegration(BaseTaskIntegrationTest):
    """
    Integration tests for EditPdfTask using the iLovePDF API.

    Covers:
    - Single file processing with a basic edit element.
    - Full workflow: add file, configure element, execute, and download results.
    """

    task_class = EditPdfTask

    def test_editpdf_basic_flow_text_type(self):
        """
        Test a basic flow for adding a text element.
        """
        self.add_sample_file("sample-1-2.pdf")

        element = self.task.add_element()
        element.type = "text"
        element.pages = "1"
        element.zindex = 1
        element.dimensions = {"w": 120.0, "h": 200.0}
        element.coordinates = {"x": 120.0, "y": 300.0}

        element.text = "Edit Task Test - Text Element"
        element.align = "center"
        element.font_color = "#FF0000"
        element.font_size = 48
        element.underline_text = 0.5

        self.execute_task()
        self.download_result("editpdf_text_type_output.pdf")

    def test_editpdf_basic_flow_image_type(self):
        """
        Test a basic flow for adding an image element.
        """
        self.add_sample_file("sample-1-2.pdf")

        element = self.task.add_element()
        element.type = "image"
        element.pages = "1"
        element.zindex = 1

        # Set a large size for the SVG
        element.dimensions = {"w": 400.0, "h": 400.0}
        # Center the SVG on a standard A4 page (595x842 points)
        element.coordinates = {"x": (595.0 - 400.0) / 2, "y": (842.0 - 400.0) / 2}

        img_filename = self.resolve_sample_file_path("ilovepdf-logo.png")
        element.set_image(img_filename)

        self.execute_task()
        self.download_result("editpdf_image_type_output.pdf")

    def test_editpdf_basic_flow_svg_type(self):
        """
        Test a basic flow for adding an svg element.
        """
        self.add_sample_file("sample-1-2.pdf")

        element = self.task.add_element()
        element.type = "svg"
        element.pages = "1"
        element.zindex = 1
        # Set a large size for the SVG
        element.dimensions = {"w": 400.0, "h": 400.0}
        # Center the SVG on a standard A4 page (595x842 points)
        element.coordinates = {"x": (595.0 - 400.0) / 2, "y": (842.0 - 400.0) / 2}

        img_filename = self.resolve_sample_file_path("ilovepdf-logo.svg")
        element.set_image(img_filename)

        self.execute_task()
        self.download_result("editpdf_svg_type_output.pdf")

    def test_editpdf_advanced_flow_all_type(self):
        """
        Test a more advanced flow with multiple element types.
        """
        self.add_sample_file("sample-1-2.pdf")

        # Add text element
        text_element = self.task.add_element()
        text_element.type = "text"
        text_element.pages = "1"
        text_element.zindex = 1
        text_element.dimensions = {"w": 120.0, "h": 200.0}
        text_element.coordinates = {"x": 120.0, "y": 300.0}
        text_element.text = "Edit Task Test - All Types"
        text_element.align = "center"
        text_element.font_color = "#FF0000"
        text_element.font_size = 48
        text_element.underline_text = 0.5

        # Add image element
        image_element = self.task.add_element()
        image_element.type = "image"
        image_element.pages = "1"
        image_element.zindex = 2
        image_element.dimensions = {"w": 200.0, "h": 200.0}
        image_element.coordinates = {"x": 50.0, "y": 50.0}
        img_filename = self.resolve_sample_file_path("ilovepdf-logo.png")
        image_element.set_image(img_filename)

        # Add svg element
        svg_element = self.task.add_element()
        svg_element.type = "svg"
        svg_element.pages = "1"
        svg_element.zindex = 3
        svg_element.dimensions = {"w": 150.0, "h": 150.0}
        svg_element.coordinates = {"x": 400.0, "y": 600.0}
        svg_filename = self.resolve_sample_file_path("ilovepdf-logo.svg")
        svg_element.set_image(svg_filename)

        self.execute_task()
        self.download_result("editpdf_all_types_output.pdf")
