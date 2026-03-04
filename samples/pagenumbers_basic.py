"""This module demonstrates a basic example of how to use the ilovepdf library
to add page numbers to a PDF file using the PageNumbersTask class."""

import os

from ilovepdf import PageNumbersTask

# Get API credentials from environment variables
PUBLIC_KEY = os.getenv("ILOVEPDF_PUBLIC_KEY", "project_public_id")
SECRET_KEY = os.getenv("ILOVEPDF_SECRET_KEY", "project_secret_key")

# Path to the input PDF file (replace with your actual file path)
INPUT_PDF = (
    os.getenv("FOLDER_SAMPLE_PATH", "tests/integration/files_samples") + "/sample.pdf"
)

# Path to save the output PDF file with page numbers
OUTPUT_PDF = "sample_with_pagenumbers.pdf"


# Create the PageNumbersTask instance
task = PageNumbersTask(public_key=PUBLIC_KEY, secret_key=SECRET_KEY)

# Add the PDF file to the task
task.add_file(INPUT_PDF)

# Configure page numbering options
task.position = "bottom_center"  # Options: top_left, top_center, top_right, bottom_left, bottom_center, bottom_right
task.format = "Page {page_number} of {total_pages}"  # Supports placeholders
task.font_size = 12
task.font_color = "#FF0000"  # Red color for demonstration
task.transparency = 80  # 80% opacity
task.show_on_cover = False  # Do not show page number on cover

# Process the task (add page numbers)
task.execute()

# Download the result
task.download(OUTPUT_PDF)
print(f"Output saved to: {OUTPUT_PDF}")
