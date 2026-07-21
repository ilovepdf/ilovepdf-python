"""Basic example to detect form fields in a PDF using FormsDetectTask.

Demonstrates how to use the ilovepdf library to detect form fields in a PDF
file via the FormsDetectTask class. This task analyzes a PDF and identifies
any form fields it contains.

For more info, see:
    https://www.iloveapi.com/docs/api-reference#formsdetect-extra-parameters
"""

from ilovepdf import FormsDetectTask

# Initialize the forms detect task with your API keys
# Get your keys at https://developer.ilovepdf.com/user/projects
my_task = FormsDetectTask("project_public_id", "project_secret_key")

# Add the input PDF file to the task
my_task.add_file("/path/to/file/document.pdf")

# Process files
my_task.execute()

# Set output filename (recommended for clarity)
my_task.set_output_filename("forms_detect_basic_sample.pdf")

# Download the result to a folder
my_task.download("output_folder")
