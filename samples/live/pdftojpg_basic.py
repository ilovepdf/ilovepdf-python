"""This module demonstrates a basic live example of how to use the ilovepdf library
to convert a PDF file to JPG images using the PdfToJpgTask class.

This script is intended for manual/live testing with real API credentials and sample
    files.
"""

from ilovepdf import PdfToJpgTask

my_task = PdfToJpgTask()


my_task.add_file("tests/integration/files_samples/sample.pdf")

my_task.pdfjpg_mode = "pages"


my_task.execute()


my_task.set_output_filename("pdftojpgtask_mode_pages.zip")

my_task.download()
