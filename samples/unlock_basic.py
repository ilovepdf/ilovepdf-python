"""This module demonstrates a basic example of how to use the ilovepdf library
to unlock a password-protected PDF file using the UnlockTask class."""

from ilovepdf import UnlockTask

# You can call the task class directly
# To get your key pair, please visit https://developer.ilovepdf.com/user/projects
unlock_task = UnlockTask("project_public_id", "project_secret_key")

# Add the password-protected PDF file (no extra_params needed)
file = unlock_task.add_file("/path/to/file/sample_protected_mysecret.pdf")

# Process files (unlock)
unlock_task.execute()

# Set the output filename and download to the specified folder
unlock_task.set_output_filename("sample_protected_mysecret_unlocked.pdf")
unlock_task.download("output_folder")
