"""Advanced example to detect form fields in multiple PDFs using FormsDetectTask.

Demonstrates how to use the ilovepdf library to detect form fields in several
PDF files via the FormsDetectTask class. When multiple files are processed,
the result is bundled as a single ZIP archive.

For more info, see:
    https://www.iloveapi.com/docs/api-reference#formsdetect-extra-parameters
"""

from ilovepdf import FormsDetectTask

# Initialize the forms detect task with your API keys
# Get your keys at https://developer.ilovepdf.com/user/projects
my_task = FormsDetectTask("project_public_id", "project_secret_key")

# Add multiple input PDF files to the task
my_task.add_file("/path/to/file/document.pdf")
my_task.add_file("/path/to/file/document2.pdf")
my_task.add_file("/path/to/file/document3.pdf")

# Process files
my_task.execute()

# Set output filename (recommended for clarity); results are bundled as a ZIP
my_task.set_output_filename("forms_detect_advanced_sample.zip")

# Download the result to a folder
my_task.download("output_folder")
