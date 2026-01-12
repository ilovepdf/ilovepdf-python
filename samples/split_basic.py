"""Sample script for basic PDF split using iLovePDF Python SDK.

This script demonstrates how to split a PDF file into specified page ranges using the SplitTask.
"""

from ilovepdf import SplitTask

# You can call the task class directly
# To get your key pair, please visit https://developer.ilovepdf.com/user/projects
my_task = SplitTask("project_public_id", "project_secret_key")

# File variable keeps info about server file id, name, etc.
# It can be used later to cancel file
file = my_task.add_file("/path/to/file/document.pdf")

# Set ranges to split the document
my_task.set_ranges("2-4,6-8")  # To split the document into pages 2-4 and 6-8
# my_task.set_fixed_range(1)
# my_task.set_remove_pages('1-2')  # To remove pages 1-2
# my_task.set_output_filename("sample_split_output.pdf")  # Optional

# Process files
my_task.execute()

# And finally download file. If no path is set, it will be downloaded in the current folder
my_task.download()
