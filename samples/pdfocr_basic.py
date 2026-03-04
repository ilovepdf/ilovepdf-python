"""
Module for demonstrating how to use the PdfOcrTask class from ilovepdf to perform OCR
on a PDF file.

To get your key pair, please visit https://developer.ilovepdf.com/user/projects
"""

from ilovepdf import PdfOcrTask

# Create an OCR task instance
my_task = PdfOcrTask("project_public_id", "project_secret_key")

# Add the PDF file you want to process with OCR
file = my_task.add_file("/path/to/file/document.pdf")

# Sets the OCR language to Spanish; English is used by default if not specified.
# This parameter is optional.
file.ocr_languages = "spa"

# Execute the OCR task
my_task.execute()

# Set output filename for OCR PDF
my_task.set_output_filename("pdfocr_basic_result.pdf")

# Download the processed OCR file to a folder
my_task.download("output_folder")
