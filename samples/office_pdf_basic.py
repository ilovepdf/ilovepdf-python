"""This module demonstrates how to convert an Office file to PDF using the ilovepdf API."""

from ilovepdf import OfficePdfTask

# Initialize the OfficePdfTask with your project keys
task = OfficePdfTask("project_public_id", "project_secret_key")

# Add an Office file to convert to PDF
task.add_file("sample_excel.xlsx")

# Execute the Office to PDF conversion task
task.execute()

# Set the output filename for the PDF file
task.set_output_filename("sample_excel.pdf")

# Download the converted PDF file. It will be saved as 'merged.pdf' in the current folder
task.download()
