"""Sample script for advanced PDF split using iLovePDF Python SDK.

Demonstrates splitting a PDF into custom ranges and setting output filenames.
"""

from ilovepdf import SplitTask

# You can call the task class directly
# To get your key pair, please visit https://developer.ilovepdf.com/user/projects
my_task = SplitTask("project_public_id", "project_secret_key")

# File variable keeps info about server file id, name, etc.
# It can be used later to cancel file
file = my_task.add_file("/path/to/file/document.pdf")

# Set ranges to split the document
my_task.set_ranges("2-4,6-8")

# Set name for output zip file (package)
my_task.set_packaged_filename("split_documents")

# Set name for splitted document (inside the zip file)
my_task.set_output_filename("split")

# Process files
my_task.execute()

# And finally download file. If no path is set, it will be downloaded in the current folder
my_task.download("path/to/download")
