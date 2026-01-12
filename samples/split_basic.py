"""Sample script for basic PDF split using iLovePDF Python SDK.

This script demonstrates how to split a PDF file into specified page ranges
using SplitTask.

Valid split configuration options:
- my_task.ranges = "2-4,6-8"  # Split by page ranges. Default split_mode.
- my_task.fixed_range = 1      # Split every page into separate file.
- my_task.remove_pages = "1-2"  # Remove pages 1 and 2 from the PDF.
- my_task.filesize = 1024*50   # Split into parts of max 50KB.

For all accessors, see split_task.py and the documentation.

https://developer.ilovepdf.com/docs/api-reference/split-pdf
"""

from ilovepdf import SplitTask

# Start split task. Get your key pair at https://developer.ilovepdf.com/user/projects
my_task = SplitTask("project_public_id", "project_secret_key")

# Add the PDF file to split
file = my_task.add_file("/path/to/file/document.pdf")

# Example: split by ranges (default mode)
my_task.ranges = (
    "2-4,6-8"  # This will split the document into two parts: pages 2-4 and 6-8
)
# my_task.fixed_range = 1      # Uncomment to split every single page into separate file
# my_task.remove_pages = "1-2"  # Uncomment to remove pages 1-2

# Process files
my_task.execute()

# Set output filename (for zip containing split documents)
my_task.set_output_filename("split_basic_result.zip")

# Download the result zip to a folder
my_task.download("output_folder")
