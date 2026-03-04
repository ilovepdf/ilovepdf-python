"""Advanced PDF split example using iLovePDF Python SDK.

Demonstrates splitting a PDF into custom page ranges, and setting output filename.
API supports using properties instead of set_XXX methods. For more advanced options,
see SplitTask docstring and https://developer.ilovepdf.com/docs/api-reference/split-pdf
"""

from ilovepdf import SplitTask

# Initialize split task (get your keys at https://developer.ilovepdf.com/user/projects)
my_task = SplitTask("project_public_id", "project_secret_key")

# Add the PDF file
file = my_task.add_file("/path/to/file/document.pdf")

# Split the document into multiple parts based on defined page ranges
my_task.ranges = "2-4,6-8"  # Each range will export as a separate document

# Process files
my_task.execute()

# (Optional) Set name for each splitted PDF inside the zip (otherwise server names them)
# Set output filename for advanced split result (ZIP)
my_task.set_output_filename("split_advanced_result.zip")

# Download the zip to the output folder
my_task.download("output_folder")
