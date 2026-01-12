"""Example script for converting images to PDF using ilovepdf's ImagePdfTask.

This script demonstrates how to use the ImagePdfTask class from the ilovepdf package
to convert multiple image files into a single PDF document. You will need your
project's public and secret keys from https://developer.ilovepdf.com/user/projects.

Steps:
1. Create an ImagePdfTask instance with your credentials.
2. Add image files to the task.
3. Optionally configure PDF parameters (orientation, margin, page size, merging).
4. Execute the task to process the images.
5. Set the output filename.
6. Download the resulting PDF.
"""

from ilovepdf import ImagePdfTask

# Example usage of ImagePdfTask for converting images to PDF.
# To get your key pair, please visit https://developer.ilovepdf.com/user/projects

# Create the task instance with your public and secret keys
my_task = ImagePdfTask("project_public_id", "project_secret_key")

# Add image files to be converted to PDF
# You can add multiple images; they will be merged if merge_after is True
my_task.add_file("/path/to/image1.jpg")
my_task.add_file("/path/to/image2.png")

# Configure task parameters (optional)
my_task.orientation = "portrait"  # 'portrait' or 'landscape'
my_task.margin = 10  # Margin in points
my_task.pagesize = "A4"  # 'fit', 'A4', or 'letter'
my_task.merge_after = True  # Merge all images into a single PDF

# Process the task (convert images to PDF)
my_task.execute()

# Set the output filename for the resulting PDF
my_task.set_output_filename("images_merged.pdf")

# Download the PDF file. It will be saved as 'images_merged.pdf' in the current folder
my_task.download()
