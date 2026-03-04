"""Live EditPdfTask example with text, image, and SVG elements on page 1."""

from ilovepdf import EditPdfTask

task = EditPdfTask()

task.add_file("tests/integration/files_samples/sample-1-2.pdf")

text_element = task.add_element()
text_element.type = "text"
text_element.pages = "1"
text_element.zindex = 1
text_element.dimensions = {"w": 260.0, "h": 80.0}
text_element.coordinates = {"x": 120.0, "y": 150.0}
text_element.text = "Live Advanced EditPdfTask"
text_element.text_align = "center"
text_element.font_family = "Arial Unicode MS"
text_element.font_size = 36
text_element.font_style = "Bold"
text_element.font_color = "#FF6600"

image_element = task.add_element()
image_element.type = "image"
image_element.pages = "1"
image_element.zindex = 2
image_element.dimensions = {"w": 160.0, "h": 160.0}
image_element.coordinates = {"x": 60.0, "y": 360.0}
image_element.set_image("tests/integration/files_samples/ilovepdf-logo.png")

svg_element = task.add_element()
svg_element.type = "svg"
svg_element.pages = "1"
svg_element.zindex = 3
svg_element.dimensions = {"w": 200.0, "h": 200.0}
svg_element.coordinates = {"x": 320.0, "y": 340.0}
svg_element.set_image("tests/integration/files_samples/ilovepdf-logo.svg")

task.execute()
task.set_output_filename("editpdf_advanced_live_result.pdf")
task.download("output_live")
