"""
Sample usage of SignTask for creating a basic digital signature workflow.

This example demonstrates how to use the SignTask class to digitally sign a PDF document using the iLovePDF API.
It shows how to add a file, create a signature element, assign it to a signer, and execute the signature task.

To get your key pair, please visit: https://developer.ilovepdf.com/user/projects

Configurable parameters:
- subject_signer: Subject of the signature request email (string)
- message_signer: Body of the signature request email (string)
- reminders: Number of days between reminders (int)
- lock_order: Whether to lock the signing order (bool)
- expiration_days: Number of days until the signature request expires (int)
- language: Language for the signature request (string, e.g., "en-US")
- uuid_visible: Whether to show the UUID in the signature (bool)
- brand_name: Custom brand name for the signature request (string)
- brand_logo: Custom brand logo file or URL

"""

from ilovepdf import SignTask
from ilovepdf.sign.elements.element_signature import ElementSignature
from ilovepdf.sign.receivers.signer import Signer

# Initialize the signature task with your project keys
sign_task = SignTask("project_public_id", "project_secret_key")

# Upload the file to be signed
file = sign_task.add_file("/path/to/file/document.pdf")

# Create the signature element and configure it
signature_element = ElementSignature()
signature_element.set_position(20, -20).set_pages("1").set_size(40)

# Create a signer
signer = Signer("My Name", "my.email@example.com")

# Assign the signature element to the signer
signer.add_elements(file, signature_element)

# Add the signer to the signature task
sign_task.add_receiver(signer)

# (Optional) Configure additional parameters if needed
# sign_task.set_subject("Please sign this document")
# sign_task.set_message("Hello, please review and sign the attached PDF.")
# sign_task.set_reminders(3)
# sign_task.set_lock_order(False)
# sign_task.set_expiration_days(30)
# sign_task.set_language("en-US")
# sign_task.set_uuid_visible(True)
# brand_logo_file = sign_task.upload_brand_logo("/path/to/logo.png")
# sign_task.set_brand("My Brand", brand_logo_file)

# Execute the signature task and get the result
signature = sign_task.execute().result
