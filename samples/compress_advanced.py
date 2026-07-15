"""Advanced example for PDF compression using CompressTask.

Demonstrates setting custom compression_level, output filename and download
location. Valid values for compression_level: "low", "recommended", "extreme".

This script also shows how to set a custom output filename and download
to a specific folder.

See:
https://www.iloveapi.com/docs/api-reference#compress-extra-parameters
"""

from ilovepdf import CompressTask

# Initialize the compress task with your API keys
my_task = CompressTask("project_public_id", "project_secret_key")

# Optionally change compression level (default: "recommended")
my_task.compression_level = "extreme"  # Smallest size, lowest quality

# Add the PDF file to compress
file = my_task.add_file("/path/to/file/document.pdf")

# Set a custom name for output file
# Set output filename for advanced compression result
my_task.set_output_filename("compress_advanced_result.pdf")

# Execute the task (compress the file)
my_task.execute()

# Download the result to the output folder
my_task.download("output_folder")
