"""Real example: convert PDF sample.pdf to PDF/A using PdfToPdfATask.
Downloads converted file into output_live/pdftopdfa_basic_result.pdf.
"""

from ilovepdf import PdfToPdfATask

my_task = PdfToPdfATask()
my_task.add_file("tests/integration/files_samples/sample.pdf")
my_task.conformance = "pdfa-2b"
my_task.execute()
my_task.set_output_filename("pdftopdfa_basic_result.pdf")
my_task.download("output_live")
