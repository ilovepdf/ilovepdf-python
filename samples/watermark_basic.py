"""Basic example: Add a text watermark to a PDF using the ilovepdf API.

This script demonstrates WatermarkTask with minimal configuration for adding a text
watermark.

Valid modes: "text", "image". See documentation for all options.
https://developer.ilovepdf.com/docs/api-reference/watermark-pdf
"""

from ilovepdf import WatermarkTask

# Instantiate the WatermarkTask class to start a new watermarking task.
# Get your API key pair at: https://developer.ilovepdf.com/user/projects

my_task = WatermarkTask("project_public_id", "project_secret_key")

# Add the PDF file
file = my_task.add_file("/path/to/file/document.pdf")

# Set watermark mode and content
my_task.mode = "text"  # You can also use "image" for an image watermark
my_task.text = "watermark text"

# Process the file and apply the watermark
my_task.execute()

# Optionally, set the output filename
my_task.set_output_filename("watermark_basic_result.pdf")

# Download the watermarked file to a folder
my_task.download("output_folder")
