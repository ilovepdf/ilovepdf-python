"""
Advanced usage of SignTask for digital signature workflows.

This example demonstrates how to use the SignTask class to create advanced
digital signature workflows with multiple elements and receivers (signer,
validator, witness) using the iLovePDF API.

You can configure options such as email subject and body, reminders,
expiration days, language, brand, and visibility settings. The script also
shows how to add various signature elements (signature, date, initials,
input, name, text) and assign them to different receivers.

To get your key pair, please visit:
https://developer.ilovepdf.com/user/projects

Configurable parameters:
- verify_signature_verification: bool
- subject: string (email subject)
- message: string (email body)
- reminders: int (days between reminders)
- lock_order: bool
- expiration_days: int
- language: string (e.g., "en-US")
- uuid_visible: bool
- brand_name: string
- brand_logo: file path or URL

Receivers:
- Signer: The person who will sign the document.
- Validator: The person who will validate the signature.
- Witness: The person who will witness the signature.

Elements:
- ElementSignature, ElementDate, ElementInitials, ElementInput,
  ElementName, ElementText

"""

from ilovepdf import SignTask
from ilovepdf.sign.elements.element_date import ElementDate
from ilovepdf.sign.elements.element_initials import ElementInitials
from ilovepdf.sign.elements.element_input import ElementInput
from ilovepdf.sign.elements.element_name import ElementName
from ilovepdf.sign.elements.element_signature import ElementSignature
from ilovepdf.sign.elements.element_text import ElementText
from ilovepdf.sign.receivers.signer import Signer
from ilovepdf.sign.receivers.validator import Validator
from ilovepdf.sign.receivers.witness import Witness

# Initialize the SignTask with your public and secret keys
sign_task = SignTask("public_key", "secret_key")

# Set the Signature settings
EMAIL_SUBJECT = "My subject"
EMAIL_BODY = "Body of the first message"

REMINDER_DAYS = 3
DAYS_UNTIL_SIGNATURE_EXPIRES = 130
TASK_LANGUAGE = "en-US"

sign_task.set_verify_signature_verification(True).set_subject(
    EMAIL_SUBJECT
).set_message(EMAIL_BODY).set_reminders(REMINDER_DAYS).set_lock_order(
    False
).set_expiration_days(
    DAYS_UNTIL_SIGNATURE_EXPIRES
).set_language(
    TASK_LANGUAGE
).set_uuid_visible(
    True
)

# Upload the file to be signed
file = sign_task.add_file("/path/to/file/document.pdf")

# Set brand
brand_logo_file = sign_task.upload_brand_logo("/path/to/file/image.png")
# Alternatively, you can download it from the cloud
# brand_logo_file = sign_task.upload_brand_logo('https://urltoimage/image.png')
sign_task.set_brand("My brand name", brand_logo_file)

##############
# ELEMENTS   #
##############
# Define the elements to be placed in the documents
elements = []

# Gravity positioning
# Xvalues: ['left','center','right']
# YValues: ['top','middle','bottom']
# horizontal_position_adjustment: integer
# vertical_position_adjustment: integer
signature_element = ElementSignature()
signature_element.set_gravity_position("left", "top", 3, -2).set_pages(
    "1,2"
)  # define the pages with a comma

date_element = ElementDate()
date_element.set_position(30, -30).set_pages(
    "1-2"
)  # ranges can also be defined this way

initials_element = ElementInitials()
initials_element.set_position(40, -40).set_pages(
    "1,2,3-6"
)  # You can define multiple ranges

input_element = ElementInput()
input_element.set_position(50, -50).set_label("Passport Number").set_text(
    "Please put your passport number"
).set_pages(
    "-2,-1"
)  # Set the last and second to last page

name_element = ElementName()
name_element.set_position(60, -60).set_size(40).set_pages("1")

text_element = ElementText()
text_element.set_position(70, -70).set_text("This is a text field").set_size(
    40
).set_pages("1")

# Add Elements
elements.append(signature_element)
elements.append(date_element)
elements.append(initials_element)
elements.append(input_element)
elements.append(name_element)
elements.append(text_element)

###############
# RECEIVERS   #
###############
# Create the receivers
signer = Signer("Signer", "signer@email.com")
validator = Validator("Validator", "validator@email.com")
witness = Witness("Witness", "witness@email.com")

# Add elements to the receivers that need it
signer.add_elements(file, elements)

# Add all receivers to the Sign task
sign_task.add_receiver(validator)
sign_task.add_receiver(signer)
sign_task.add_receiver(witness)

# Lastly, send the signature request
signature = sign_task.execute().result
print(signature)
