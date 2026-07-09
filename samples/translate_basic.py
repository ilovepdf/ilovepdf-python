"""Basic example to translate a PDF file using TranslateTask.

Demonstrates how to use the ilovepdf library to translate a PDF file via the
TranslateTask class. By default, the output format is PDF ("pdf").

For more info, see:
    https://www.iloveapi.com/docs/pdf-guides/translate-api
"""

from ilovepdf import TranslateTask

# Initialize the translate task with your API keys
my_task = TranslateTask("project_public_id", "project_secret_key")

# Add the input PDF file to the task
file = my_task.add_file("/path/to/file/document.pdf")

# Set source and target languages (both required before execute)
my_task.language_input = "eng"
my_task.language_output = "fra"

# Process files
my_task.execute()

# Set output filename (recommended for clarity)
my_task.set_output_filename("translate_basic_sample.pdf")

# Download the translated file to a folder
my_task.download("output_folder")
