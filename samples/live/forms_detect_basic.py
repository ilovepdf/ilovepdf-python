"""Live example: PDF form detection using FormsDetectTask.

This script demonstrates detecting form fields in a PDF document.
Downloads the result to output_live/forms_detect_basic_result.pdf.
"""

from ilovepdf import FormsDetectTask

my_task = FormsDetectTask()
my_task.add_file("tests/integration/files_samples/sample-form.pdf")
my_task.execute()
my_task.set_output_filename("forms_detect_basic_result.pdf")
my_task.download("output_live")
