"""Basic example to smart split a PDF file using SmartSplitTask.

Demonstrates how to use the ilovepdf library to split a PDF file via the
SmartSplitTask class using AI-powered content analysis. The prompt guides the
AI to identify natural document sections (e.g., chapters) to split on.

For more info, see:
    https://www.iloveapi.com/docs/api-reference#splitsmart-extra-parameters
"""

from ilovepdf import SmartSplitTask

# Initialize the smart split task with your API keys
# Get your keys at https://developer.ilovepdf.com/user/projects
my_task = SmartSplitTask("project_public_id", "project_secret_key")

# Add the input PDF file to the task
my_task.add_file("/path/to/file/document.pdf")

# Set the prompt to guide the AI (required)
my_task.prompt = "Split at chapter boundaries"

# Process files
my_task.execute()

# Set output filename (recommended for clarity)
my_task.set_output_filename("smart_split_basic_sample.zip")

# Download the result to a folder (a ZIP with the split PDFs)
my_task.download("output_folder")
