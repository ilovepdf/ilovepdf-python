"""Advanced example to translate a PDF file using TranslateTask.

Demonstrates how to use the ilovepdf library to translate a PDF file via the
TranslateTask class. By default, the output format is PDF ("pdf").

For more info, see:
    https://www.iloveapi.com/docs/pdf-guides/translate-api
"""

from ilovepdf import TranslateTask

my_task = TranslateTask("project_public_id", "project_secret_key")

# Source and target languages are required before execute
my_task.language_input = "eng"
my_task.language_output = "spa"

# Optionally set the output format (valid: "pdf", "txt")
# "pdf" tries to keep the original formatting
# "txt" extracts translated content as plain text
my_task.output_format = "pdf"

file = my_task.add_file("/path/to/file/document.pdf")

my_task.execute()

my_task.set_output_filename("translate_advanced_sample.pdf")
my_task.download("output_folder")
