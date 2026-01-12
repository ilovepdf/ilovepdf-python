"""Basic example of rotating a PDF file using the ilovepdf API.

This script demonstrates how to use the RotateTask class from the ilovepdf
package to rotate a PDF document by a specified angle and download the result.
"""

from ilovepdf import RotateTask

# You can instantiate the RotateTask class directly.
# To obtain your API key pair, visit: https://developer.ilovepdf.com/user/projects
my_task = RotateTask("project_public_id", "project_secret_key")

# Add the PDF file you want to rotate. Use the 'rotate' property (0, 90, 180, 270).
file = my_task.add_file("/path/to/file/document.pdf")
file.rotate = 90  # Rotate by 90 degrees

# Execute the rotation task.
my_task.execute()

# Set the output filename for the rotated PDF.
my_task.set_output_filename("document_rotated.pdf")

# Set output filename for rotated PDF
my_task.set_output_filename("rotate_basic_result.pdf")

# Download the rotated PDF to a folder
my_task.download("output_folder")
