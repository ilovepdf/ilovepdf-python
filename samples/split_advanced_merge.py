"""Sample script for advanced split and merge using iLovePDF API.

Demonstrates how to split a PDF into custom ranges and merge the results
into a single document using SplitTask properties.

For details, see: https://www.iloveapi.com/docs/api-reference#split-extra-parameters
"""

from ilovepdf import SplitTask

# Initialize split task (use your project keys from ilovepdf.com/user/projects)
my_task = SplitTask("project_public_id", "project_secret_key")

# Add the PDF file
file = my_task.add_file("/path/to/file/document.pdf")

# Split the PDF into ranges
my_task.ranges = "2-4,6-8"  # Each part becomes a separate file

# Set that we want the splitted files to be merged into a single document
my_task.merge_after = True

# Process
my_task.execute()

# Set name for the output file (the merged result)
# Set output filename for advanced split-merge result
my_task.set_output_filename("split_advanced_merge_result.pdf")

# Download the output to the output folder
my_task.download("output_folder")
