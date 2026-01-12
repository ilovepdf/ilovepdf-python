"""Sample script for advanced split and merge using iLovePDF API.

Demonstrates how to split a PDF into ranges and merge the results into a single document.
"""

from ilovepdf import SplitTask

# You can use the task class directly
# To get your key pair, please visit https://developer.ilovepdf.com/user/projects
my_task = SplitTask("project_public_id", "project_secret_key")

# File variable keeps info about server file id, name, etc.
# It can be used later to cancel file
file = my_task.add_file("/path/to/file/document.pdf")

# Set ranges to split the document
my_task.set_ranges("2-4,6-8")

# Set that we want splitted files to be merged into a new one
my_task.set_merge_after(True)

# Set name for merged document
my_task.set_output_filename("split")

# Process files
my_task.execute()

# And finally download file. If no path is set, it will be downloaded in the current folder
my_task.download("path/to/download")
