"""Basic example to convert a PDF file to Markdown using PdfMarkdownTask.

Demonstrates how to use the ilovepdf library to convert a PDF file to Markdown
text via the PdfMarkdownTask class.

For more info, see:
    https://www.iloveapi.com/docs/api-reference#pdfmarkdown-extra-parameters
"""

from ilovepdf import PdfMarkdownTask

# Initialize the pdfmarkdown task with your API keys
# Get your keys at https://developer.ilovepdf.com/user/projects
my_task = PdfMarkdownTask("project_public_id", "project_secret_key")

# Add the input PDF file to the task
my_task.add_file("/path/to/file/document.pdf")

# Process files
my_task.execute()

# Set output filename (recommended for clarity)
my_task.set_output_filename("pdfmarkdown_basic_sample.md")

# Download the Markdown result to a folder
my_task.download("output_folder")
