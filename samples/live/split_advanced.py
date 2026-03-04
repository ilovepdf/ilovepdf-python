"""Live example: advanced PDF splitting using SplitTask.

This script demonstrates splitting a PDF into multiple ranges.
Replace credentials and file paths with your own values for a real test.

For API documentation, see: https://developer.ilovepdf.com/docs/api-reference/split
"""

from ilovepdf import SplitTask

split_task = SplitTask()

# Add the PDF file to be split
file = split_task.add_file("tests/integration/files_samples/sample.pdf")

# Define advanced split ranges as a string (e.g., split into three parts)
split_task.ranges = "1-2,3-5,6-"

# Execute the split task
split_task.execute()

# Set the output filename and download to the integration samples folder
split_task.set_output_filename("split_advanced_result.zip")
split_task.download("output_live")
