"""
Module for converting PDF files to PDF/A format using ilovepdf's PdfToPdfATask.

Sample usage of PdfToPdfATask for converting PDF files to PDF/A format. To get your key
pair, please visit https://developer.ilovepdf.com/user/projects
"""

from ilovepdf import PdfToPdfATask

# Create the task instance with your public and secret keys
my_task = PdfToPdfATask("project_public_id", "project_secret_key")

# Add PDF files to be converted to PDF/A
my_task.add_file("/path/to/document1.pdf")

# Configure optional task parameters
# For example, you can select the PDF/A conformance level ('pdfa-1b', 'pdfa-2b', etc.)
my_task.conformance = "pdfa-2b"  # PDF/A conformance level

# Process the task (convert PDFs to PDF/A)
my_task.execute()

# Set output filename for PDF/A result
my_task.set_output_filename("pdftopdfa_basic_result.pdf")

# Download the PDF/A result to a folder
my_task.download("output_folder")
