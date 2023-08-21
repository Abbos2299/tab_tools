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

app = Flask(__name__)
cred = credentials.Certificate(
    'tab-tools-firebase-adminsdk-8ncav-4f5ccee9af.json')
firebase_admin.initialize_app(cred)


@app.route('/launch', methods=['GET'])
def launch_python_file():
    user_uid = request.args.get('uid')
    print('User UID:', user_uid)

    bucket_name = 'tab-tools.appspot.com'
    bucket = storage.bucket(bucket_name)
    folder_name = user_uid  # Replace with the appropriate user UID
    blobs = bucket.list_blobs(prefix=folder_name)

    # Wait for 2 seconds
    time.sleep(1)

    # Iterate over the blobs and get the last added file
    last_added_blob = None
    for blob in blobs:
        if not last_added_blob or blob.updated > last_added_blob.updated:
            last_added_blob = blob

    if last_added_blob:
        file_name = urllib.parse.unquote(last_added_blob.name.split(
            '/')[-1])  # Get the file name from the blob URL
        file_url = last_added_blob.generate_signed_url(
            expiration=timedelta(minutes=15))
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

        # List of broker companies
        broker_companies = [
            "AFC Brokerage",
            "AFC Logistics",
            "AIT Truckload Solutions",
            "AIT Worldwide Logistics",
            "Allen Lund",
            "Alliance Highway Capacity",
            "ALLY LOGISTICS LLC",
            "AM Transport Services, Inc",
            "American Group, LLC",
            "American Sugar Refining, Inc.",
            "American Transportation Group, LLC",
            "Amsino",
            "Amstan Logistics",
            "ArcBest Corp.",
            "ArcBest Dedicated, LLC",
            "Archerhub",
            "Armada/Sunset Transportation",
            "Armstrong Transport Group",
            "Arrive Logistics",
            "ASCEND, LLC",
            "Ascent Global Logistics",
            "Ashley Distribution Services",
            "ATS Logistics Services, Inc",
            "Axle Logistics",
            "B. R. Williams Trucking, Inc",
            "BAT Logistics",
            "Bay & Bay Transportation",
            "Becker Logistics",
            "Beemac Logistics",
            "Best Logistics",
            "BFT Trucking",
            "Blue Marlin Logistics Group",
            "BlueGrace Logistics",
            "BM2 Freight Services",
            "BMM Logistics",
            "BNSF Logistics",
            "Buchanan Logistics",
            "BZS TRANSPORT",
            "C.H. Robinson",
            "C.L. Services",
            "C&L Logistics, Inc",
            "Capable Transport, Inc.",
            "CAPITAL LOGISTICS GROUP",
            "Capstone Logistics",
            "Cardinal Logistics",
            "Cardinal Logistics Management Corp.",
            "CarrierHawk",
            "Centerstone Logistics",
            "Chariot Logistics",
            "Circle Logistics, Inc",
            "Commodity Transportation Services, LLC",
            "Concept International Transportation",
            "Confiance LLC",
            "Convoy",
            "Cornerstone Systems",
            "Corporate Traffic Logistics",
            "Covenant Transport Solutions",
            "Cowan Logistics",
            "COYOTE",
            "Creech Brokerage, Inc",
            "CRST The Transportation Solution",
            "Custom Pro Logistics llc",
            "CW Carriers USA Inc",
            "Czechmate Logistics Inc.",
            "D2 FREIGHT SOLUTIONS, LLC",
            "Day & Ross",
            "DestiNATION Transport, LLC",
            "DIAMOND LOGISTICS",
            "Direct Connect Logistix",
            "Direct Connect Transport, Inc.",
            "DSV A/S",
            "Dupré Logistics",
            "DYNAMIC LOGISTIX",
            "Dynamo Freight LLC",
            "Ease Logistics",
            "EASE Logistics Services",
            "Echo Global Logistics",
            "Edge Logistics",
            "ELI Solutions, LLC",
            "ELIT Transit Solutions, LLC",
            "EMERGE TECH LLC",
            "England Logistics",
            "eShipping, LLC",
            "Evans Delivery Company, Inc",
            "EVE INTERNATIONAL LOGISTICS INC",
            "everest transportation system",
            "EXPRESS LOGISTICS, INC",
            "Fastmore",
            "FEDEX CUSTOM CRITICAL FREIGHT SOLUTIONS",
            "Fifth Wheel Freight",
            "FitzMark",
            "FLS Transportation Services",
            "FreedomTrans USA, LLC",
            "Freezpak Logistics",
            "FreightEx Logistics, LLC",
            "Frontier Logistics LLC",
            "Genpro Inc.",
            "GIX Logistics, Inc",
            "GlobalTranz",
            "GO2 EXPRESS",
            "Gulf Relay Logistics, LLC",
            "Haines City Truck Brokers",
            "Hazen Transfer",
            "High Tide Logistics",
            "HTS Logistics",
            "Hub Group",
            "InstiCo",
            "Integrity Express Logistics",
            "ITF LOGISTICS GROUP LLC",
            "ITS Logistics",
            "J.B. Hunt Transport, Inc",
            "JEAR Logistics, LLC",
            "jerue Companies",
            "Johanson Transportation Service",
            "John J. Jerue Truck Broker, Inc.",
            "K & L FREIGHT MANAGEMENT",
            "KAG Logistics",
            "Keller Freight Solutions",
            "Kenco Transportation Management LLC",
            "Kirsch Transportation",
            "Kiss Logistics",
            "KLG Logistics Services, LLC",
            "Knight-Swift Transportation",
            "Koch Logistics",
            "Kodiak Transportation, LLC",
            "Koola Logistics",
            "Landmark Logistics, Inc",
            "LandStar Global Logistics",
            "LANDSTAR INWAY",
            "Landstar Ranger",
            "LIBERTY COMMERICAL",
            "LinQ Transport, Inc",
            "Loadsmart",
            "Logistic Dynamics",
            "Logistics One Brokerage, Inc.",
            "Logistics Plus",
            "Longship",
            "Magellan Transport Logistics",
            "Marathon Transport, Inc",
            "Marten Transport",
            "Marten Transport Logistics LLC",
            "Matson Logistics",
            "Max Trans Logistics of Chattanooga LLC",
            "McLeod Logistics",
            "MDB Logistics",
            "Meadow Lark Agency, Inc",
            "MegaCorp Logistics",
            "MIDWEST EXPRESS FREIGHT SOLUTIONS",
            "Mode Global",
            "Moeller Logistics",
            "MoLo Solutions",
            "Motus Freight",
            "Nationwide Logistics",
            "Navajo Expedited",
            "Network Transport",
            "NFI",
            "Nolan Transportation Group, LLC",
            "NORTHEAST LOGISTICS",
            "ODW Logistics",
            "Old Frontier Family Inc",
            "OpenRoad Transportation, Inc.",
            "Packer Transportation & Logistics",
            "PAM Transport Inc",
            "PATHMARK TRANSPORTATION",
            "Patterson Companies",
            "Paul Logistics, Inc",
            "Payne Trucking Co.",
            "PEPSI LOGISTICS COMPANY, INC.",
            "Performance Logistics",
            "Perimeter Logistics LLC",
            "PHOENIX SUPPLY CHAIN",
            "PINK PANTHERS",
            "PLS Logistics",
            "Priority-1 Inc.",
            "R&R Express",
            "R2 Logistics",
            "Radiant Logistics",
            "RB Humphreys",
            "Red Classic",
            "Redwood logistics",
            "Redwood Logistics",
            "REED TRANSPORT",
            "Reliable Transportation Solutions",
            "RFX",
            "RJ Logistics, LLC",
            "RJS",
            "RLS Logistics",
            "ROAR LOGISTICS",
            "ROYAL TRANSPORTATION SERVICES",
            "RPM carrier",
            "RPM Freight Systems",
            "RXO, Inc.",
            "RYAN TRANSPORTATION SERVICE, INC",
            "Ryder Supply Chain Solutions",
            "S & H Transport, Inc.",
            "S and S Nationwide",
            "Scan Global Logistics",
            "Schneider",
            "Schneider Shipment",
            "Scotlynn USA Division",
            "Simple Logistics, LLC",
            "Spartan Logistics Services, LLC",
            "SPI Logistics",
            "Spirit Logistics",
            "Spot Inc.",
            "ST Freight",
            "Starland Global Logistics LLC",
            "Steam Logistics",
            "Summit Eleven Inc.",
            "Sunrise Logistics, Inc.",
            "Surge Transportation Inc",
            "Synchrogistics LLC",
            "TA Services",
            "Tallgrass Freight Co.",
            "TAYLOR LOGISTICS, INC",
            "TERRY ENTERPRISES, INC.",
            "The Worthington Company",
            "Thomas E. Keller Trucking, INC.",
            "TII Logistics Inc",
            "TORCH LOGISTICS, LLC",
            "Torch3pl",
            "Total Quality Logistics",
            "TRAFFIX",
            "Trailer Bridge",
            "TransAmerica Express Logistics",
            "Transfix",
            "TRANSLOOP",
            "Trident Transport, LLC",
            "Trinity Logistics",
            "Triple T Transport",
            "U.S. Xpress Enterprises",
            "Uber Freight/Transplace Inc.",
            "UNIVERSAL CAPACITY SOLUTIONS",
            "Universal Logistics Holdings",
            "Unlimited Logistics",
            "US Logistics",
            "US1 Network",
            "USAT Logistics",
            "Value Logistics Inc",
            "Venture Connect",
            "VERIHA LOGISTICS",
            "Veritiv Logistics Solutions",
            "Watco Logistics",
            "Werner Enterprises",
            "West Motor Freight of PA",
            "Worldwide Express/GlobalTranz",
            "XPO Logistics, LLC",
            "Yellow Logistics",
            "Zengistics Solutions Inc"
        ]

        # Initialize a dictionary to count the occurrences of each broker company
        broker_counts = {company: 0 for company in broker_companies}

        # Search for matches with broker companies
        for company in broker_companies:
            matches = re.findall(r'\b' + re.escape(company) + r'\b', all_text, flags=re.IGNORECASE)
            count = len(matches)
            broker_counts[company] = count

        # Find the most used broker company
        most_used_broker = max(broker_counts, key=broker_counts.get)
        print("Most used broker company:", most_used_broker)

        # Wait for 20 seconds
        time.sleep(3)
        # Delete the file
        os.remove(file_name)
        print(f'File "{file_name}" deleted successfully')

    else:
        print('No files found in the folder')

    return 'Success'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
