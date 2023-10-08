from docquery import document, pipeline
import pdfminer
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
import io
import json

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
    # Define the questions to ask
    questions = [
        "What is the load number?",
        "What is broker Email?",
        "What is Pick up location?",
        "What is Pick up date?",
        "What is the Delivery location?",
        "What is Delivery date?",
        "What is the Total amount?"
    ]

    # Initialize DocQuery pipeline
    docquery_pipe = pipeline("tableqa")

    # Extract information using DocQuery
    answers = docquery_pipe(text, questions)

    return answers

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

# Replace 'all_text' with the path to your PDF file
file_path = 'path_to_your_pdf_file.pdf'
file_text = extract_text_from_pdf(file_path)

answers = extract_information(file_text)
print("DocQuery Answers:")
for question, answer in zip(questions, answers):
    print(f"{question}: {answer}")

# Note: You can also create a Flask route to receive a PDF file and extract information from it.
