"""Real example: digital signature workflow on sample.pdf with two signers (SignTask).
No direct output file; inspect task result or API for document links.
"""

from ilovepdf import SignTask
from ilovepdf.sign import Signer

sign_task = SignTask()
file = sign_task.add_file("tests/integration/files_samples/sample.pdf")
signers = [
    Signer(name="Advanced Tester One", email="one@example.com"),
    Signer(name="Advanced Tester Two", email="two@example.com"),
]
for signer in signers:
    signer.add_file(file)
    sign_task.add_signer(signer)
sign_task.subject_signer = "Advanced Workflow"
sign_task.message_signer = "Sign this contract."
sign_task.lock_order = False
sign_task.language = "en-US"
sign_task.expiration_days = 30
sign_task.execute()
# For live, follow up using API/web.
