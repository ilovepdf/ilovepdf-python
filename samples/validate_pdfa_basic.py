"""This module demonstrates a basic example of how to use the ilovepdf library
to validate if a PDF file is PDF/A compliant using the ValidatePdfATask class."""

from ilovepdf.validate_pdfa_task import ValidatePdfATask

# Replace with your actual public and secret keys or use environment variables
PUBLIC_KEY = "project_public_id"
SECRET_KEY = "project_secret_key"

# Create the validation task instance
task = ValidatePdfATask(PUBLIC_KEY, SECRET_KEY)

# Add the PDF file to be validated
task.add_file("/path/to/document.pdf")

# Execute the validation task
task.execute()

# Access the validation result
result = task.validation_result

if result is not None:
    if result.get("status") == "Conformant":
        print("The file is PDF/A compliant.")
    else:
        print("The file is NOT PDF/A compliant.")
        reasons = result.get("reason", [])
        for reason in reasons:
            print(f"  - {reason}")
else:
    print("No validation result available. Check if the task executed successfully.")

# Note:
# - Replace '/path/to/document.pdf' with the path to your PDF file.
# - This script only validates compliance; it does not convert the file.
