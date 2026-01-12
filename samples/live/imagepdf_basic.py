"""Real example: convert images to PDF using ImagePdfTask.
Downloads merged PDF into output_live/imagepdf_basic_result.pdf.
"""

from ilovepdf import ImagePdfTask

my_task = ImagePdfTask()
my_task.add_file("tests/integration/files_samples/sample-img-1.jpg")
my_task.add_file("tests/integration/files_samples/sample-img-2.png")
my_task.orientation = "portrait"
my_task.margin = 10
my_task.pagesize = "A4"
my_task.merge_after = True
my_task.execute()
my_task.set_output_filename("imagepdf_basic_result.pdf")
my_task.download("output_live")
