"""
Sample usage of HtmlToPdfTask for converting HTML content to PDF.

This example demonstrates how to use the HtmlToPdfTask class to convert HTML files or URLs to PDF
using the iLovePDF API. You can configure options such as page orientation, margin, view width,
page size, single page mode, ad blocking, and popup removal.

To get your key pair, please visit: https://developer.ilovepdf.com/user/projects

Configurable parameters:
- page_orientation: "portrait" or "landscape"
- page_margin: integer (points)
- view_width: integer (pixels)
- page_size: string (e.g., "A4")
- single_page: bool
- block_ads: bool
- remove_popups: bool
"""

from ilovepdf import HtmlToPdfTask

# Create the task instance with your public and secret keys
my_task = HtmlToPdfTask("project_public_id", "project_secret_key")


# Add HTML file to be converted to PDF
# You can add a local HTML file or a remote HTML file via URL
# my_task.add_file("/path/to/document.html")
my_task.add_file_from_url("https://example.com")

# Optional: configure task parameters
my_task.page_orientation = "landscape"  # "portrait" or "landscape"
my_task.page_margin = 10  # Margin in points
my_task.view_width = 1200  # View width in pixels
my_task.page_size = "A4"  # Page size, e.g., "A4"
my_task.single_page = False  # Single page mode
my_task.block_ads = True  # Block ads in HTML
my_task.remove_popups = True  # Remove popups from HTML

# Process the task (convert HTML to PDF)
my_task.execute()

# Optional: set the output filename for the resulting PDF
my_task.set_output_filename("converted_html.pdf")

# Download the PDF file. It will be saved as 'converted_html.pdf' in the current folder
my_task.download()
