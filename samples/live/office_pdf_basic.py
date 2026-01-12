"""Real example: convert office file sample.docx to PDF using OfficePdfTask.
Downloads PDF into output_live/office_pdf_basic_result.pdf.
"""

from ilovepdf import OfficePdfTask

my_task = OfficePdfTask()
my_task.add_file("tests/integration/files_samples/sample_word.docx")
my_task.execute()
my_task.set_output_filename("office_pdf_basic_result.pdf")
my_task.download("output_live")
