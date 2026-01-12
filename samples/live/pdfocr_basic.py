"""Real example: OCR sample.pdf using PdfOcrTask with Spanish language.
Downloads OCR PDF into output_live/pdfocr_basic_result.pdf.
"""

from ilovepdf import PdfOcrTask

my_task = PdfOcrTask()
file = my_task.add_file("tests/integration/files_samples/sample.pdf")
file.ocr_languages = "spa"
my_task.execute()
my_task.set_output_filename("pdfocr_basic_result.pdf")
my_task.download("output_live")
