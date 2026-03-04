"""Advanced example: Edit a PDF with text, image, and SVG elements using EditPdfTask.

Complexity level: Advanced.
This script demonstrates stacking multiple element types on the first page of a PDF.
"""

from ilovepdf import EditPdfTask

# Replace with your project keys from https://developer.ilovepdf.com/user/projects
PUBLIC_KEY = "project_public_id"
SECRET_KEY = "project_secret_key"

task = EditPdfTask(PUBLIC_KEY, SECRET_KEY)

# Add the PDF file you want to edit
task.add_file("/path/to/input/document.pdf")

# Configure a rich text element
text_element = task.add_element()
text_element.type = "text"
text_element.pages = "1"
text_element.zindex = 1
text_element.dimensions = {"w": 260.0, "h": 80.0}
text_element.coordinates = {"x": 120.0, "y": 150.0}
text_element.text = "Advanced EditPdfTask Sample"
text_element.text_align = "center"
text_element.font_family = "Arial Unicode MS"
text_element.font_size = 36
text_element.font_style = "Bold"
text_element.font_color = "#FF6600"

# Configure an image element (PNG/JPG/JPEG/GIF)
image_element = task.add_element()
image_element.type = "image"
image_element.pages = "1"
image_element.zindex = 2
image_element.dimensions = {"w": 160.0, "h": 160.0}
image_element.coordinates = {"x": 60.0, "y": 360.0}
image_element.set_image("/path/to/assets/logo.png")

# Configure an SVG element
svg_element = task.add_element()
svg_element.type = "svg"
svg_element.pages = "1"
svg_element.zindex = 3
svg_element.dimensions = {"w": 200.0, "h": 200.0}
svg_element.coordinates = {"x": 320.0, "y": 340.0}
svg_element.set_image("/path/to/assets/logo.svg")

# Execute the task and download the edited PDF
task.execute()
task.set_output_filename("editpdf_advanced_result.pdf")
task.download("/path/to/output/folder")
