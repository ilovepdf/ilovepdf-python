"""Real example: add text watermark to sample.pdf using WatermarkTask.
Downloads PDF file into output_live/watermark_basic_result.pdf.
"""

from ilovepdf import WatermarkTask

my_task = WatermarkTask()
file = my_task.add_file("tests/integration/files_samples/sample.pdf")
my_task.mode = "text"
my_task.text = "Live Sample Watermark"
my_task.execute()
my_task.set_output_filename("watermark_basic_result.pdf")
my_task.download("output_live")
