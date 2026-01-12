# pylint: disable=C0301
"""Live example: advanced PDF optimization using CompressTask.

This script demonstrates optimizing multiple PDFs with custom compression levels.
Replace credentials and file paths with your own values for a real test.
"""

from ilovepdf import CompressTask

# Initialize the compress task (credentials should be set via environment or .env for live testing)
compress_task = CompressTask()

# Add multiple image files to be compressed
files = [
    compress_task.add_file("tests/integration/files_samples/sample.pdf"),
    compress_task.add_file("tests/integration/files_samples/sample_2MB.pdf"),
]

# Set advanced compression level
compress_task.compression_level = "extreme"

# Execute the compression task
compress_task.execute()

# Set the output filename and download the result to the integration samples folder
compress_task.set_output_filename("compress_advanced_result.zip")
compress_task.download("output_live")
