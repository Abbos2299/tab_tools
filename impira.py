from docquery import document, pipeline
import pdfminer
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
import io
import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import sys
from docquery import pipeline

model_name = "impira/docquery"  
docquery_pipe = pipeline("tableqa", model=model_name, use_auth_token=True)

# Define the questions here
questions = [
    "What is the load number?",
    "What is broker Email?",
    "What is Pick up location?",
    "What is Pick up date?",
    "What is the Delivery location?",
    "What is Delivery date?",
    "What is the Total amount?"
]

# Initialize Firebase credentials
cred = credentials.Certificate('tab-tools-firebase-adminsdk-8ncav-4f5ccee9af.json')
firebase_admin.initialize_app(cred)

# Get a Firestore client
db = firestore.client()

user_uid = sys.argv[1]
file_name = sys.argv[2]

def extract_text_from_pdf(file_path):
    resource_manager = PDFResourceManager()
    output_stream = io.StringIO()
    laparams = pdfminer.layout.LAParams()
    device = TextConverter(resource_manager, output_stream, laparams=laparams)
    with open(file_path, 'rb') as file:
        interpreter = PDFPageInterpreter(resource_manager, device)
        for page in PDFPage.get_pages(file):
            interpreter.process_page(page)
    file_text = output_stream.getvalue()
    device.close()
    output_stream.close()
    return file_text

def extract_information(text):
    # Initialize DocQuery pipeline
    docquery_pipe = pipeline("tableqa")

    # Extract information using DocQuery
    answers = docquery_pipe(text, questions)

    return answers

# Extract text from the PDF file
file_text = extract_text_from_pdf(file_name)

# Extract information from the extracted text
answers = extract_information(file_text)

# Print the answers
print("DocQuery Answers:")
for question, answer in zip(questions, answers):
    print(f"{question}: {answer}")

# Exit the script
sys.exit()
