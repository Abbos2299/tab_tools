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
import urllib.parse
import os
import pytesseract
from pdf2image import convert_from_path
import re
from docquery import document, pipeline

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

        images = convert_from_path(file_name)
        all_text = ""
        for i, image in enumerate(images):
            text = pytesseract.image_to_string(image)
            all_text += text
        broker_companies = [
            "J.B. Hunt",
        ]

        # Initialize a dictionary to count the occurrences of each broker company
        broker_counts = {company: 0 for company in broker_companies}

        # Search for matches with broker companies
        for company in broker_companies:
            matches = re.findall(r'\b' + re.escape(company) +
                                 r'\b', all_text, flags=re.IGNORECASE)
            count = len(matches)
            broker_counts[company] = count

        # Find the most used broker company
        most_used_broker = max(broker_counts, key=broker_counts.get)

       



    if broker_counts[most_used_broker] > 0:
        print(most_used_broker)

    # Correct the identified broker company names if needed
        if most_used_broker == "J.B. Hunt":
            most_used_broker = "J. B. Hunt Transportation"
            subprocess.call([sys.executable, "jbhunt.py",
                        user_uid, most_used_broker, file_name])
        else:
            print("RC don't identified")
            subprocess.call([sys.executable, "impira.py",
                     user_uid, file_name])

        # Wait for 1 seconds
        time.sleep(1)
        # Delete the file
        os.remove(file_name)

    else:
        print('No files found in the folder')

    return 'Success'


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
