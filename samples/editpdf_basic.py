"""Basic example: Edit a PDF with a text element using EditPdfTask.

Complexity level: Basic.
This script shows how to add a single text element to the first page of a PDF.
"""

from ilovepdf import EditPdfTask

# Replace with your project keys from https://developer.ilovepdf.com/user/projects
PUBLIC_KEY = "project_public_id"
SECRET_KEY = "project_secret_key"

task = EditPdfTask(PUBLIC_KEY, SECRET_KEY)

# Add the PDF file you want to edit
task.add_file("/path/to/input/document.pdf")

# Configure a text element
element = task.add_element()
element.type = "text"
element.pages = "1"
element.zindex = 1
element.dimensions = {"w": 160.0, "h": 60.0}
element.coordinates = {"x": 120.0, "y": 220.0}
element.text = "Edited with iLovePDF"
element.text_align = "center"
element.font_color = "#FF0000"
element.font_size = 28

# Execute the task and download the edited PDF
task.execute()
task.set_output_filename("editpdf_basic_result.pdf")
task.download("/path/to/output/folder")
