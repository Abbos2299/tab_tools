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

app = Flask(__name__)
cred = credentials.Certificate('tab-tools-firebase-adminsdk-8ncav-4f5ccee9af.json')
firebase_admin.initialize_app(cred)

# Set the TESSDATA_PREFIX environment variable
os.environ['TESSDATA_PREFIX'] = '/usr/local/share/tessdata'

@app.route('/launch', methods=['GET'])
def launch_python_file():
    user_uid = request.args.get('uid')
    print('User UID:', user_uid)

    bucket_name = 'tab-tools.appspot.com'
    bucket = storage.bucket(bucket_name)
    folder_name = user_uid  # Replace with the appropriate user UID
    blobs = bucket.list_blobs(prefix=folder_name)

    # Wait for 2 seconds
    time.sleep(2)

    # Iterate over the blobs and get the last added file
    last_added_blob = None
    for blob in blobs:
        if not last_added_blob or blob.updated > last_added_blob.updated:
            last_added_blob = blob

    if last_added_blob:
        file_name = urllib.parse.unquote(last_added_blob.name.split('/')[-1])  # Get the file name from the blob URL
        file_url = last_added_blob.generate_signed_url(expiration=timedelta(minutes=15))
        print('Last added file URL:', file_url)

        # Download the file from Firebase
        response = requests.get(file_url)
        with open(file_name, 'wb') as f:
            f.write(response.content)

        print(f'File "{file_name}" downloaded successfully')

        # Process the downloaded file with Pytesseract
        images = convert_from_path(file_name)
        all_text = ""
        for i, image in enumerate(images):
            text = pytesseract.image_to_string(image)
            all_text += text

        # Print the extracted text
        print("Extracted text from PDF:")
        print(all_text)

        # Wait for 20 seconds
        time.sleep(20)

        # Delete the file
        os.remove(file_name)
        print(f'File "{file_name}" deleted successfully')

        # Check if a broker name was found
        if broker_name:
            # Create Firestore document with the broker name
            db = firestore.client()
            users_ref = db.collection('users')
            user_doc_ref = users_ref.document(user_uid)

            loads_ref = user_doc_ref.collection('Loads')
            load_doc_ref = loads_ref.document(file_name)

            load_doc_ref.set({
                'Broker Company Name': broker_name
            })

            print(f'Firestore document created for Load "{file_name}" with Broker Company Name: {broker_name}')
        else:
            print('No broker name found in the PDF')

    else:
        print('No files found in the folder')

    return 'Success'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
