"""Real example: convert HTML (via URL) to PDF using HtmlToPdfTask.
Downloads converted PDF into output_live/html_to_pdf_basic_result.pdf.
"""

from ilovepdf import HtmlToPdfTask

my_task = HtmlToPdfTask()
my_task.add_file_from_url("https://example.com")
my_task.page_orientation = "portrait"
my_task.page_size = "A4"
my_task.execute()
my_task.set_output_filename("html_to_pdf_basic_result.pdf")
my_task.download("output_live")
