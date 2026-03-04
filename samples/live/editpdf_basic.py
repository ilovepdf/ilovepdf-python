"""Live sample that edits a PDF by placing a text element on page 1."""

from ilovepdf import EditPdfTask

task = EditPdfTask()

task.add_file("tests/integration/files_samples/sample-1-2.pdf")

element = task.add_element()
element.type = "text"
element.pages = "1"
element.zindex = 1
element.dimensions = {"w": 200.0, "h": 80.0}
element.coordinates = {"x": 120.0, "y": 220.0}
element.text = "Live EditPdfTask sample"
element.text_align = "center"
element.font_size = 32
element.font_color = "#FF0000"

task.execute()
task.set_output_filename("editpdf_basic_live_result.pdf")
task.download("output_live")
