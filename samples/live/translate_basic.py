"""Live example: AI-powered PDF translation using TranslateTask.

This script demonstrates translating a PDF document to a target language.
Downloads the translated file to output_live/translate_basic_result.pdf.
"""

from ilovepdf import TranslateTask

my_task = TranslateTask()
my_task.add_file("tests/integration/files_samples/sample.pdf")
my_task.language_input = "eng"
my_task.language_output = "spa"
my_task.execute()
my_task.set_output_filename("translate_basic_result.pdf")
my_task.download("output_live")
