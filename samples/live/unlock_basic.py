# pylint: disable=C0301
"""Live example: unlock a password-protected PDF using UnlockTask.

This script demonstrates how to use the ilovepdf library to remove password protection from a PDF file.
Replace credentials and file paths with your own values for a real test.

For API documentation, see: https://developer.ilovepdf.com/docs/api-reference/unlock
"""

from ilovepdf import UnlockTask

# Initialize the unlock task (credentials should be set via environment or .env for live testing)
unlock_task = UnlockTask()

# Add the password-protected PDF file from the integration samples folder
file = unlock_task.add_file("tests/integration/files_samples/sample_protected_mysecret.pdf")

# Process the file to remove password protection
unlock_task.execute()

# Set the output filename and download to the specified folder
unlock_task.set_output_filename("sample_protected_mysecret_unlocked.pdf")
unlock_task.download("output_live")
