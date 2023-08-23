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

# Initialize Firebase credentials
cred = credentials.Certificate('tab-tools-firebase-adminsdk-8ncav-4f5ccee9af.json')
firebase_admin.initialize_app(cred)

# Get a Firestore client
db = firestore.client()

user_uid = sys.argv[1]
most_used_broker = sys.argv[2]
file_name = sys.argv[3]

print(user_uid)
print(most_used_broker)
print(file_name)

def extract_text_from_pdf(file_path):
    resource_manager = PDFResourceManager()
    output_stream = io.StringIO()
    codec = 'utf-8'
    laparams = pdfminer.layout.LAParams()
    device = TextConverter(resource_manager, output_stream, codec=codec, laparams=laparams)
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
    rate = re.search(r'Total Rate: (.+)', text)
    broker_email = re.search(r'J.B. Hunt Contact.+Email: (.+)', text)
    load_miles = re.search(r'Load Details\n(.+)', text)

    pick_up = re.search(r'Shipper :1|Shipper # 1|Shipper: 1\n(.+)', text)
    pick_up_time = re.search(r'Pick Up\n(.+Pickup)', text)
    pick_up_number = re.search(r'Pick Up\n.+Shipper ID:(.+)?.+', text)
    pu_po_number = re.search(r'Pick Up\n.+PO #:(.+)', text)

    delivery = re.search(r'Consignee # 1|Consignee: 1|Consignee :1\n(.+)', text)
    delivery_time = re.search(r'Delivery\n(.+Pickup)', text)
    delivery_number = re.search(r'Delivery\n.+Shipper ID:(.+)?.+', text)
    del_po_number = re.search(r'Delivery\n.+PO #:(.+)', text)

    pick_up_2 = re.search(r'Shipper :2|Shipper # 2|Shipper: 2\n(.+)', text)
    pick_up_2_time = re.search(r'Pick Up 2\n(.+Pickup)', text)
    pick_up_2_number = re.search(r'Pick Up 2\n.+Shipper ID:(.+)?.+', text)
    pu2_po_number = re.search(r'Pick Up 2\n.+PO #:(.+)', text)

    delivery_2 = re.search(r'Consignee # 2\n(.+)', text)
    delivery_2_time = re.search(r'Delivery 2\n(.+Pickup)', text)
    delivery_2_number = re.search(r'Delivery 2\n.+Shipper ID:(.+)?.+', text)
    del2_po_number = re.search(r'Delivery 2\n.+PO #:(.+)', text)

    pick_up_3 = re.search(r'Shipper :3\n(.+)', text)
    pick_up_3_time = re.search(r'Pick Up 3\n(.+Pickup)', text)
    pick_up_3_number = re.search(r'Pick Up 3\n.+Shipper ID:(.+)?.+', text)
    pu3_po_number = re.search(r'Pick Up 3\n.+PO #:(.+)', text)

    delivery_3 = re.search(r'Consignee # 3\n(.+)', text)
    delivery_3_time = re.search(r'Delivery 3\n(.+Pickup)', text)
    delivery_3_number = re.search(r'Delivery 3\n.+Shipper ID:(.+)?.+', text)
    del3_po_number = re.search(r'Delivery 3\n.+PO #:(.+)', text)

    pick_up_4 = re.search(r'Shipper :4\n(.+)', text)
    pick_up_4_time = re.search(r'Pick Up 4\n(.+Pickup)', text)
    pick_up_4_number = re.search(r'Pick Up 4\n.+Shipper ID:(.+)?.+', text)
    pu4_po_number = re.search(r'Pick Up 4\n.+PO #:(.+)', text)

    delivery_4 = re.search(r'Consignee # 4\n(.+)', text)
    delivery_4_time = re.search(r'Delivery 4\n(.+Pickup)', text)
    delivery_4_number = re.search(r'Delivery 4\n.+Shipper ID:(.+)?.+', text)
    del4_po_number = re.search(r'Delivery 4\n.+PO #:(.+)', text)

    return (
        load_number.group(1) if load_number else None,
        rate.group(1) if rate else None,
        broker_email.group(1) if broker_email else None,
        load_miles.group(1) if load_miles else None,
        pick_up.group(1) if pick_up else None,
        pick_up_time.group(1) if pick_up_time else None,
        pick_up_number.group(1) if pick_up_number else None,
        pu_po_number.group(1) if pu_po_number else None,
        delivery.group(1) if delivery else None,
        delivery_time.group(1) if delivery_time else None,
        delivery_number.group(1) if delivery_number else None,
        del_po_number.group(1) if del_po_number else None,
        pick_up_2.group(1) if pick_up_2 else None,
        pick_up_2_time.group(1) if pick_up_2_time else None,
        pick_up_2_number.group(1) if pick_up_2_number else None,
        pu2_po_number.group(1) if pu2_po_number else None,
        delivery_2.group(1) if delivery_2 else None,
        delivery_2_time.group(1) if delivery_2_time else None,
        delivery_2_number.group(1) if delivery_2_number else None,
        del2_po_number.group(1) if del2_po_number else None,
        pick_up_3.group(1) if pick_up_3 else None,
        pick_up_3_time.group(1) if pick_up_3_time else None,
        pick_up_3_number.group(1) if pick_up_3_number else None,
        pu3_po_number.group(1) if pu3_po_number else None,
        delivery_3.group(1) if delivery_3 else None,
        delivery_3_time.group(1) if delivery_3_time else None,
        delivery_3_number.group(1) if delivery_3_number else None,
        del3_po_number.group(1) if del3_po_number else None,
        pick_up_4.group(1) if pick_up_4 else None,
        pick_up_4_time.group(1) if pick_up_4_time else None,
        pick_up_4_number.group(1) if pick_up_4_number else None,
        pu4_po_number.group(1) if pu4_po_number else None,
        delivery_4.group(1) if delivery_4 else None,
        delivery_4_time.group(1) if delivery_4_time else None,
        delivery_4_number.group(1) if delivery_4_number else None,
        del4_po_number.group(1) if del4_po_number else None
    )

def save_result_to_firebase(load_number, rate, broker_email, load_miles, pick_up, pick_up_time, pick_up_number, pu_po_number, delivery, delivery_time, delivery_number, del_po_number, pick_up_2, pick_up_2_time, pick_up_2_number, pu2_po_number, delivery_2, delivery_2_time, delivery_2_number, del2_po_number, pick_up_3, pick_up_3_time, pick_up_3_number, pu3_po_number, delivery_3, delivery_3_time, delivery_3_number, del3_po_number, pick_up_4, pick_up_4_time, pick_up_4_number, pu4_po_number, delivery_4, delivery_4_time, delivery_4_number, del4_po_number):
    # Get the loads collection for the user
    loads_ref = db.collection('users').document(user_uid).collection('loads')

    # Get the latest load document number
    latest_load = loads_ref.order_by('document_number', direction=firestore.Query.DESCENDING).limit(1).get()
    if latest_load:
        document_number = latest_load[0].to_dict()['document_number'] + 1
    else:
        document_number = 1

    # Create a new load document
    load_doc_ref = loads_ref.document(str(document_number))

    # Save the extracted information to the load document
    load_doc_ref.set({
        'LoadNumber': load_number,
        'Rate': rate,
        'BrokerEmail': broker_email,
        'LoadMiles': load_miles,
        'PickUp': pick_up,
        'PickUpTime': pick_up_time,
        'PickUpNumber': pick_up_number,
        'PUPoNumber': pu_po_number,
        'Delivery': delivery,
        'DeliveryTime': delivery_time,
        'DeliveryNumber': delivery_number,
        'DelPoNumber': del_po_number,
        'PickUp2': pick_up_2,
        'PickUp2Time': pick_up_2_time,
        'PickUp2Number': pick_up_2_number,
        'PU2PoNumber': pu2_po_number,
        'Delivery2': delivery_2,
        'Delivery2Time': delivery_2_time,
        'Delivery2Number': delivery_2_number,
        'Del2PoNumber': del2_po_number,
        'PickUp3': pick_up_3,
        'PickUp3Time': pick_up_3_time,
        'PickUp3Number': pick_up_3_number,
        'PU3PoNumber': pu3_po_number,
        'Delivery3': delivery_3,
        'Delivery3Time': delivery_3_time,
        'Delivery3Number': delivery_3_number,
        'Del3PoNumber': del3_po_number,
        'PickUp4': pick_up_4,
        'PickUp4Time': pick_up_4_time,
        'PickUp4Number': pick_up_4_number,
        'PU4PoNumber': pu4_po_number,
        'Delivery4': delivery_4,
        'Delivery4Time': delivery_4_time,
        'Delivery4Number': delivery_4_number,
        'Del4PoNumber': del4_po_number
    })

# Extract text from the PDF
pdf_text = extract_text_from_pdf(file_name)

# Apply regex rules to extract information
(
    load_number, rate, broker_email, load_miles,
    pick_up, pick_up_time, pick_up_number, pu_po_number,
    delivery, delivery_time, delivery_number, del_po_number,
    pick_up_2, pick_up_2_time, pick_up_2_number, pu2_po_number,
    delivery_2, delivery_2_time, delivery_2_number, del2_po_number,
    pick_up_3, pick_up_3_time, pick_up_3_number, pu3_po_number,
    delivery_3, delivery_3_time, delivery_3_number, del3_po_number,
    pick_up_4, pick_up_4_time, pick_up_4_number, pu4_po_number,
    delivery_4, delivery_4_time, delivery_4_number, del4_po_number
) = apply_regex_rules(pdf_text)

# Save the result to Firebase
save_result_to_firebase(
    load_number, rate, broker_email, load_miles,
    pick_up, pick_up_time, pick_up_number, pu_po_number,
    delivery, delivery_time, delivery_number, del_po_number,
    pick_up_2, pick_up_2_time, pick_up_2_number, pu2_po_number,
    delivery_2, delivery_2_time, delivery_2_number, del2_po_number,
    pick_up_3, pick_up_3_time, pick_up_3_number, pu3_po_number,
    delivery_3, delivery_3_time, delivery_3_number, del3_po_number,
    pick_up_4, pick_up_4_time, pick_up_4_number, pu4_po_number,
    delivery_4, delivery_4_time, delivery_4_number, del4_po_number
)

print("jbhunt.py launched successfully")
sys.exit()
