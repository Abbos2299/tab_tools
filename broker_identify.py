import subprocess
import sys
import tempfile
from flask import Flask, request
import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
import time
import os
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
import io


app = Flask(__name__)
cred = credentials.Certificate(
    'tab-tools-firebase-adminsdk-8ncav-4f5ccee9af.json')
firebase_admin.initialize_app(cred)


@app.route('/launchidentify', methods=['GET'])
def launch_python_file():
    user_uid = request.args.get('uid')

    bucket_name = 'tab-tools.appspot.com'
    bucket = storage.bucket(bucket_name)
    folder_name = user_uid  # Replace with the appropriate user UID

    blobs = bucket.list_blobs(prefix=folder_name)

    time.sleep(1)
    for blob in blobs:
        if blob.name.lower().endswith('.pdf'):
            # Create a temporary file to save the PDF content
            with tempfile.NamedTemporaryFile(suffix=".pdf") as temp_pdf_file:
                # Download the PDF content to the temporary file
                blob.download_to_filename(temp_pdf_file.name)

                # Extract text from the PDF using pdfminer
                text = extract_text_from_pdf(temp_pdf_file.name)

                # Process the extracted text as needed
    return 'Success'


def extract_text_from_pdf(pdf_path):
    """
    Extract text from a PDF file using pdfminer.
    """
    rsrcmgr = PDFResourceManager()
    retstr = io.StringIO()
    codec = 'utf-8'
    laparams = LAParams()

    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    with open(pdf_path, 'rb') as fp:
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        password = ""
        maxpages = 0
        caching = True
        pagenos = set()

        for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password, caching=caching, check_extractable=True):
            interpreter.process_page(page)

    text = retstr.getvalue()
    device.close()
    retstr.close()

    # Print the extracted text
    print("Extracted Text:")
    print(text)

    return text


@app.route('/locationcheck', methods=['GET'])
def location_check():
    user_uid = request.args.get('uid')
    latitude = request.args.get('lat')
    longitude = request.args.get('lon')

    if latitude is not None and longitude is not None:
        print(f'Latitude: {latitude}, Longitude: {longitude}')
        return 'Success'
    else:
        return 'Location check failed'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
