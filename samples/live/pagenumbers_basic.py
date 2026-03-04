"""
This sample demonstrates how to add page numbers to a PDF file using the iLovePDF API.
It shows how to set the position, format, font size, color, transparency, and whether
to show page numbers on the cover page. Finally, it executes the task and downloads
the modified PDF file.
"""

from ilovepdf import PageNumbersTask

task = PageNumbersTask()
task.add_file("tests/integration/files_samples/sample.pdf")
task.position = "bottom_center"
task.format = "Page {page_number} of {total_pages}"
task.font_size = 14
task.font_color = "#007ACC"
task.transparency = 90
task.show_on_cover = False
task.execute()
task.set_output_filename("sample_with_pagenumbers_live.pdf")
task.download("output_live")
