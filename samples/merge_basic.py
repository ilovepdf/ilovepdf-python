"""This module demonstrates how to merge PDF files using the ilovepdf Python SDK.

MergeTask allows you to combine multiple PDFs into a single file. Simply initialize,
add files, execute, and download.

https://www.iloveapi.com/docs/api-reference#merge-extra-parameters
"""

from ilovepdf import MergeTask

# Initialize the merge task with your project keys
my_task = MergeTask("project_public_id", "project_secret_key")

# Add each PDF to be merged
my_task.add_file("/path/to/file/document-1.pdf")
my_task.add_file("/path/to/file/document-2.pdf")

# Execute the merge task
my_task.execute()

# Set output filename for merged PDF
my_task.set_output_filename("merge_basic_result.pdf")

# Download the merged file (to a folder)
my_task.download("output_folder")
