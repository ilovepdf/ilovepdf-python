"""This script demonstrates how to add a text watermark to a PDF file using the ilovepdf API."""

from ilovepdf import WatermarkTask

# Instantiate the WatermarkTask class to start a new watermarking task.
# Get your API key pair at: https://developer.ilovepdf.com/user/projects

my_task = WatermarkTask("project_public_id", "project_secret_key")

# Add the PDF file to which you want to apply the watermark.
file = my_task.add_file("/path/to/file/document.pdf")

# Set watermark mode to 'text'
my_task.mode = "text"

# Set the watermark text
my_task.text = "watermark text"

# Process the file and apply the watermark
my_task.execute()

# Optionally set the output filename for the watermarked PDF
my_task.set_output_filename("document_watermarked.pdf")

# Finally, download the watermarked file. If no path is set, it will be downloaded to the current folder.
my_task.download()
