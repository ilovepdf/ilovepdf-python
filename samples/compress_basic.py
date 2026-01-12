"""This module demonstrates how to use the ilovepdf library to compress a PDF file using the CompressTask class."""

from ilovepdf import CompressTask

# You can call the task class directly
# To get your key pair, please visit https://developer.ilovepdf.com/user/projects
my_task = CompressTask("project_public_id", "project_secret_key")

# file var keeps info about server file id, name...
# it can be used later to cancel file
file = my_task.add_file("/path/to/file/document.pdf")
# process files
my_task.execute()

# and finally download file. If no path is set, it will be downloaded in the current folder
my_task.download()
