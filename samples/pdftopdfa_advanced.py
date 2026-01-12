"""
Module for demonstrating usage of PdfToPdfATask to convert PDF files to PDF/A format.
To get your key pair, please visit https://developer.ilovepdf.com/user/projects
"""

from ilovepdf import PdfToPdfATask

# Create the task instance with your public and secret keys
my_task = PdfToPdfATask("project_public_id", "project_secret_key")

# Add PDF files to be converted to PDF/A
my_task.add_file("/path/to/document1.pdf")
my_task.add_file("/path/to/document2.pdf")
my_task.add_file("/path/to/document3.pdf")

# Configure optional task parameters
# For example, you can select the PDF/A conformance level ('pdfa-1b', 'pdfa-2b', etc.)
my_task.conformance = "pdfa-2b"  # PDF/A conformance level

# Process the task (convert PDFs to PDF/A)
my_task.execute()

# Optional
# Set the output filename for the resulting file
# If multiple files are added, the result will be a ZIP
my_task.set_output_filename("documents_pdfa.zip")

# Download the converted file. It will be saved as 'documents_pdfa.zip' in the current folder
my_task.download()
