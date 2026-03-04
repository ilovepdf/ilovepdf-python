"""This module demonstrates a basic example of how to use the ilovepdf library
to convert a PDF file to JPG images using the PdfToJpgTask class."""

from ilovepdf import PdfToJpgTask

# Replace with your actual API credentials
# To get your key pair, visit https://developer.ilovepdf.com/user/projects
my_task = PdfToJpgTask("project_public_id", "project_secret_key")

# Add a PDF file to convert
my_task.add_file("/path/to/sample.pdf")

# Set conversion mode (optional, default is 'pages')
# 'pages': converts each page to a JPG image
# 'extract': extracts images embedded in the PDF
my_task.pdfjpg_mode = "pages"

# Process the task (convert PDF to JPG)
my_task.execute()

# Optionally set the output filename for the resulting ZIP file
my_task.set_output_filename("pdftojpgtask_mode_page.zip")

# Download the ZIP file containing JPG images. It will be saved in the current folder.
my_task.download()
