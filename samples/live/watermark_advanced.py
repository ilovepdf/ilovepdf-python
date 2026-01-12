# pylint: disable=C0301
"""Live example: advanced watermarking using WatermarkTask.

This script demonstrates adding a text watermark with custom options.
Replace credentials and file paths with your own values for a real test.

For API documentation, see: https://developer.ilovepdf.com/docs/api-reference/watermark
"""

from ilovepdf import WatermarkTask

# Initialize the watermark task (credentials should be set via environment or .env for live testing)
watermark_task = WatermarkTask()

# Add the PDF file to watermark
file = watermark_task.add_file("tests/integration/files_samples/sample.pdf")

# Configure advanced watermark options
watermark_task.text = "Confidential"
watermark_task.vertical_position = "bottom"
watermark_task.horizontal_position = "center"
watermark_task.transparency = 50
watermark_task.font_size = 24

# Process the watermarking
watermark_task.execute()

# Set the output filename and download to the specified folder
watermark_task.set_output_filename("watermark_advanced_result.pdf")
watermark_task.download("output_live")
