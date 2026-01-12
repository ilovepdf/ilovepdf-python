"""Sample script to protect a PDF file using ilovepdf-python.

Demonstrates setting a password to encrypt a PDF using the ProtectTask
with the correct (property-based) API.
https://developer.ilovepdf.com/docs/api-reference/protect-pdf
"""

from ilovepdf import ProtectTask

# Start the protect task. Get your keys at https://developer.ilovepdf.com/user/projects
my_task = ProtectTask("project_public_id", "project_secret_key")

# Add the file you want to protect
file = my_task.add_file("/path/to/file/document.pdf")

# Set a password to protect the PDF (non-empty string)
my_task.password = "your_secure_password"

# Process the task (protect the file)
my_task.execute()

# Set the output filename for the protected file
my_task.set_output_filename("document_protect.pdf")

# Set output filename for protected PDF
my_task.set_output_filename("protect_basic_result.pdf")

# Download the protected PDF to a folder
my_task.download("output_folder")
