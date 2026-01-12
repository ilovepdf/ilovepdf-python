"""This script demonstrates how to use the ilovepdf WatermarkTask to add a text watermark to a PDF file."""

from ilovepdf import WatermarkTask

# Instantiate the WatermarkTask class to start a new watermarking task.
# Get your API key pair at: https://developer.ilovepdf.com/user/projects

my_task = WatermarkTask(
    "project_public_id",
    "project_secret_key",
)

# Add the PDF file to which you want to apply the watermark.
file = my_task.add_file("/path/to/file/document.pdf")

# set mode to text
my_task.mode = "text"

# set the text
my_task.text = "watermark text"

# set pages to apply the watermark
my_task.pages = "1-5,7"

# set vertical position
my_task.vertical_position = "top"

# set horizontal position
my_task.horizontal_position = "right"

# adjust vertical position
my_task.vertical_position_adjustment = 100

# adjust horizontal position
my_task.horizontal_position_adjustment = 100

# set font family
my_task.font_family = "Arial"

# set the font size
my_task.font_size = 12

# set color to red
my_task.font_color = "#ff0000"

# set transparency
my_task.transparency = 50

# set the layer
my_task.layer = "below"

# and set name for output file.
# the task will set the correct file extension for you.
my_task.set_output_filename("document_watermarked.pdf")

# process files
my_task.execute()

# and finally download the unlocked file. If no path is set, it will be downloaded on current folder
my_task.download()
