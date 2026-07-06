"""Basic example to summarize a PDF file using SummarizeTask.

Demonstrates how to use the ilovepdf library to generate an AI-powered summary
of a PDF file via the SummarizeTask class. By default, the summary language is
English ("en") and output format is PDF ("pdf").

You can customize the language (e.g., "es", "fr", "de") and output format
("pdf" or "md").

For more info, see:
https://www.iloveapi.com/docs/api-reference#summarize-extra-parameters
"""

from ilovepdf import SummarizeTask

# Start the summarize task. Get your keys at https://developer.ilovepdf.com/user/projects
my_task = SummarizeTask("project_public_id", "project_secret_key")

# Optionally set the language for the summary (see LANGUAGE_OPTIONS in the source)
my_task.language = "en"  # Comment out for default "en"

# Optionally set the output format (valid: "pdf", "md")
my_task.output_format = "pdf"  # Comment out for default "pdf"

# Add the input PDF file to the task
file = my_task.add_file("/path/to/file/document.pdf")

# Process files
my_task.execute()

# Set output filename (recommended for clarity)
my_task.set_output_filename("summary_basic_sample.pdf")

# Download the summarized file to a folder
my_task.download("output_folder")
