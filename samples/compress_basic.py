"""Basic example to compress a PDF file using CompressTask.

Demonstrates how to use the ilovepdf library to compress a single PDF file via the
CompressTask class. By default, compression_level is set to 'recommended' (balance of
quality and size), but you can set it to 'low', 'recommended', or 'extreme'.

Example:
    my_task.compression_level = "low"  # Set to smallest size, lowest quality

For more info, see:
https://www.iloveapi.com/docs/api-reference#compress-extra-parameters
"""

from ilovepdf import CompressTask

# Start the compress task. Get your keys at https://developer.ilovepdf.com/user/projects
my_task = CompressTask("project_public_id", "project_secret_key")

# Optionally set the compression level (valid: "low", "recommended", "extreme")
my_task.compression_level = "low"  # Comment out for default "recommended"

# Add the input PDF file to the task
file = my_task.add_file("/path/to/file/document.pdf")

# Process files
my_task.execute()

# Set output filename (recommended for clarity)
my_task.set_output_filename("compress_basic_sample.pdf")

# Download the compressed file to a folder
my_task.download("output_folder")
