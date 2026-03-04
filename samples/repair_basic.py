"""
Basic example of repairing a PDF document using the ilovepdf API.
"""

from ilovepdf import RepairTask

# You can call the task class directly
# To get your key pair, please visit https://developer.ilovepdf.com/user/projects
my_task = RepairTask("project_public_id", "project_secret_key")

# Add the file you want to repair
file = my_task.add_file("/path/to/file/document.pdf")

# Process the task (repair the file)
my_task.execute()

# Set output filename for repaired PDF
my_task.set_output_filename("repair_basic_result.pdf")

# Download the repaired PDF to a folder
my_task.download("output_folder")
