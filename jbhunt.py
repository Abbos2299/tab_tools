import sys
import io
import pdfminer
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
import re
from datetime import datetime
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

timestamp = datetime.now().strftime("%y%m%d%H%M%S")

# Initialize Firebase credentials
cred = credentials.Certificate('tab-tools-firebase-adminsdk-8ncav-4f5ccee9af.json')
firebase_admin.initialize_app(cred)

# Get a Firestore client
db = firestore.client()

user_uid = sys.argv[1]
most_used_broker = sys.argv[2]
file_name = sys.argv[3]

def extract_text_from_pdf(file_path):
    resource_manager = PDFResourceManager()
    output_stream = io.StringIO()
    laparams = pdfminer.layout.LAParams()
    device = TextConverter(resource_manager, output_stream, laparams=laparams)
    with open(file_path, 'rb') as file:
        interpreter = PDFPageInterpreter(resource_manager, device)
        for page in PDFPage.get_pages(file):
            interpreter.process_page(page)
    text = output_stream.getvalue()
    device.close()
    output_stream.close()
    return text

def apply_regex_rules(text):
    load_number = re.search(r'Carrier Confirmation for Load (.+)', text)
    rate = re.search(r'Total Rate:(.+)', text)
    broker_email = re.search(r'J.B. Hunt Contact\n.+?\n(.+)', text)
    load_miles = re.search(r'Load Details\n(.+)', text)
    broker_email_address = broker_email.group(1) if broker_email else None
    if broker_email_address:
        email_match = re.search(r'Email:\s?([\w\.-]+@[\w\.-]+)', broker_email_address)
        if email_match:
            broker_email_address = email_match.group(1)
        elif re.match(r'^[\w\.-]+@[\w\.-]+$', broker_email_address):
            pass
        else:
            broker_email_address = None
    pick_up_info = re.search(r'Shipper\s?:?\s?1\n(.+?)\n(.+?)\n(.+?)\n', text, re.DOTALL)
    pick_up = ' '.join(pick_up_info.groups()) if pick_up_info else None
    pick_up_time = re.search(r'Pickup\n(.+)', text)
    pick_up_t = pick_up_time.group(1) if pick_up_time else None

    consignee_regex = r'Consignee # (\d+)\n(.+?)\n(.+?)\n(.+?)\n'
    consignees = re.findall(consignee_regex, text, re.DOTALL)
    consignee_location = ['\n'.join(consignee[1:]) for consignee in consignees]

    delivery_info = re.findall(r'Delivery\n(.+)', text)
    delivery_times = delivery_info[:-1]  # Exclude the last occurrence

    return (
        load_number.group(1) if load_number else None,
        rate.group(1) if rate else None,
        broker_email_address,
        load_miles.group(1) if load_miles else None,
        pick_up,
        pick_up_t,
        consignee_location,
        delivery_times,
    )

def save_result_to_firebase(load_number, rate, broker_email, load_miles, pick_up, pick_up_t, consignee_location, delivery_times):

    loads_ref = db.collection('users').document(user_uid).collection('Loads')

    # Create a new load document
    load_doc_ref = loads_ref.document(timestamp)

    # Create the "rules" document and set the "Last added load" field
    rules_doc_ref = loads_ref.document('rules')
    rules_doc_ref.set({
        'Last added load': timestamp
    })

    # Save the extracted information to the load document
    load_doc_ref.set({
        'FileName': file_name,
        'LoadNumber': load_number,
        'Rate': rate,
        'BrokerEmail': broker_email,
        'LoadMiles': load_miles,
        'PickUp': pick_up,
        'PickUpTime': pick_up_t,
        'Deliveries': consignee_location,
        'DeliveryTimes': delivery_times,
    })
    
# Extract text from the PDF
pdf_text = extract_text_from_pdf(file_name)

# Apply regex rules to extract information
(
    load_number, rate, broker_email, load_miles, pick_up, pick_up_t, consignee_location, delivery_times
) = apply_regex_rules(pdf_text)

# Save the result to Firebase
save_result_to_firebase(
    load_number, rate, broker_email, load_miles, pick_up, pick_up_t, consignee_location, delivery_times
)

sys.exit()
