"""Sample script to protect a PDF file using ilovepdf-python."""

from ilovepdf import ProtectTask

# You can call the task class directly
# To get your key pair, please visit https://developer.ilovepdf.com/user/projects
my_task = ProtectTask("project_public_id", "project_secret_key")

# Add the file you want to protect
file = my_task.add_file("/path/to/file/document.pdf")

# Set a password to protect the PDF
my_task.set_password("your_secure_password")

# Process the task (protect the file)
my_task.execute()

# Set the output filename for the protected file
my_task.set_output_filename("document_protect.pdf")

# Finally, download the protected file. It will be saved as 'document_protect.pdf' in the current folder
my_task.download()
