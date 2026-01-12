"""This module demonstrates how to merge PDF files using the ilovepdf Python SDK."""

from ilovepdf import MergeTask

# Initialize the merge task with your project keys
task = MergeTask("project_public_id", "project_secret_key")

# Upload files to be merged
task.add_file("/path/to/file/document-1.pdf")
task.add_file("/path/to/file/document-2.pdf")


# Execute the merge task and get the result
task.execute()

# Finally, download the merged file. It will be saved as 'merged.pdf' in the current folder
task.download()
