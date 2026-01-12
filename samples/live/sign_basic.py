"""Real example: digitally sign a PDF (sample.pdf) using SignTask.
No output file downloaded; inspect task result or API response.
"""

from ilovepdf import SignTask
from ilovepdf.sign import Signer

sign_task = SignTask()
file = sign_task.add_file("tests/integration/files_samples/sample.pdf")
signer = Signer(name="Live Tester", email="live@example.com")
signer.add_file(file)
sign_task.add_signer(signer)
sign_task.subject_signer = "Please sign"
sign_task.message_signer = "Live sample digital signature demo."
sign_task.execute()
# For live, inspect sign_task or manage further via UI/API.
