"""
This module demonstrates how to convert an Office file to PDF using the ilovepdf API.
"""

from ilovepdf import OfficePdfTask

# Initialize the OfficePdfTask with your project keys
my_task = OfficePdfTask("project_public_id", "project_secret_key")

# Add an Office file to convert to PDF
my_task.add_file("sample_excel.xlsx")

# Execute the Office to PDF conversion task
my_task.execute()

# Set the output filename for the PDF file
my_task.set_output_filename("sample_excel.pdf")

# Set output filename for Office-to-PDF result
my_task.set_output_filename("office_pdf_basic_result.pdf")

# Download the converted PDF to a folder
my_task.download("output_folder")
