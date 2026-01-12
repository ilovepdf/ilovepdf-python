"""Real example: convert multiple PDFs to PDF/A using PdfToPdfATask (advanced).
Downloads result as ZIP to output_live/pdftopdfa_advanced_result.zip.
"""

from ilovepdf import PdfToPdfATask

my_task = PdfToPdfATask()
my_task.add_file("tests/integration/files_samples/sample.pdf")
my_task.add_file("tests/integration/files_samples/sample.pdf")
my_task.add_file("tests/integration/files_samples/sample.pdf")
my_task.conformance = "pdfa-2b"
my_task.execute()
my_task.set_output_filename("pdftopdfa_advanced_result.zip")
my_task.download("output_live")
