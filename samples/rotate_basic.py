"""Basic example of rotating a PDF file using the ilovepdf API.

This script demonstrates how to use the RotateTask class from the ilovepdf package
to rotate a PDF document by a specified angle and download the result.

"""

from ilovepdf import RotateTask

# You can instantiate the RotateTask class directly.
# To obtain your API key pair, visit: https://developer.ilovepdf.com/user/projects
# my_task = RotateTask("project_public_id", "project_secret_key")
my_task = RotateTask("project_public_id", "project_secret_key")

# Add the PDF file you want to rotate.
file = my_task.add_file("/path/to/file/document.pdf")
# Set the rotation angle for the PDF (e.g., 90, 180, or 270 degrees).
file.set_rotation(90)

# Execute the rotation task.
my_task.execute()

# Set the output filename for the rotated PDF.
my_task.set_output_filename("document_rotated.pdf")

# Download the rotated PDF. It will be saved as 'document_protect.pdf' in the current directory.
my_task.download()
