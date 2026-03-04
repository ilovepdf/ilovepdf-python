"""
Sample usage of ExtractTask for extracting text from PDF files.
To get your key pair, please visit https://developer.ilovepdf.com/user/projects
"""

from ilovepdf import ExtractTask

# Create the task instance with your public and secret keys
my_task = ExtractTask("project_public_id", "project_secret_key")

# Add PDF file to extract text from
my_task.add_file("/path/to/document1.pdf")

# Optional: configure extraction parameters
# Set detailed to True to include extra PDF properties in the extracted text
my_task.detailed = True

# Process the task (extract text from PDF)
my_task.execute()

# Set output filename for extracted text
my_task.set_output_filename("extract_basic_result.txt")

# Download the extracted text file to a folder
my_task.download("output_folder")
