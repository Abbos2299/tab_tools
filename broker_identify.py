import subprocess
import sys
from flask import Flask, request
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import storage
from datetime import timedelta
import requests
import time
import os
import re
import io
import urllib.parse
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams


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

    broker_name = None  # Initialize broker_name
    last_added_blob = None

    for blob in blobs:
        if not last_added_blob or blob.updated > last_added_blob.updated:
            last_added_blob = blob

    if last_added_blob:
        file_name = urllib.parse.unquote(last_added_blob.name.split(
            '/')[-1])  # Get the file name from the blob URL
        file_url = last_added_blob.generate_signed_url(
            expiration=timedelta(minutes=15))

        # Download the file from Firebase
        response = requests.get(file_url)
        with open(file_name, 'wb') as f:
            f.write(response.content)

            # Extract text from the PDF using pdfminer
            text = extract_text_from_pdf(file_name)

            # Check if "J.B. Hunt" appears more than once in the text
            if text.lower().count("j.b. hunt") > 1:
                broker_name = "J. B. Hunt Transportation"

    # If broker_name is identified, launch jbhunt.py
    if broker_name:
        subprocess.call([sys.executable, "jbhunt.py",
                         user_uid, file_name])

    else:
        print("Broker not identified")
        subprocess.call([sys.executable, "impira.py",
                         user_uid, file_name])

    return 'Success'


def extract_text_from_pdf(pdf_path):
    """
    Extract text from a PDF file using pdfminer.
    """
    print(f"Extracting text from PDF: {pdf_path}")  # Debug output
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

    # Print the extracted text for debugging
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
