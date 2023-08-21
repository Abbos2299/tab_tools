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
        print("Text Exctracted")
        print(all_text)

        # List of broker companies
        broker_companies = [
            "AFC Brokerage",
"AFC Logistics",
"AIT Truckload",
"AIT Worldwide",
"Allen Lund",
"Alliance Highway",
"ALLY LOGISTICS",
"AM Transport ",
"American Group",
"American Sugar",
"American Transportation",
"Amsino",
"Amstan Logistics",
"ArcBest Corp",
"ArcBest Dedicated",
"Archerhub",
"Sunset Transportation",
"Armstrong Transport",
"Arrive Logistics",
"ASCEND",
"Ascent Global",
"Ashley Distribution",
"ATS Logistics",
"Axle Logistics",
"B. R. Williams",
"BAT Logistics",
"Bay & Bay",
"Becker Logistics",
"Beemac Logistics",
"Best Logistics",
"BFT Trucking",
"Blue Marlin Logistics",
"BlueGrace Logistics",
"BM2 Freight",
"BMM Logistics",
"BNSF Logistics",
"Buchanan Logistics",
"BZS TRANSPORT",
"C.H. Robinson",
"C.L. Services",
"C&L Logistics",
"Capable Transport",
"CAPITAL LOGISTICS",
"Capstone Logistics",
"Cardinal Logistics",
"Cardinal Logistics",
"CarrierHawk",
"Centerstone",
"Chariot Logistics",
"Circle Logistics",
"Commodity Transportation",
"Concept International",
"Confiance LLC",
"Convoy",
"Cornerstone Systems",
"Corporate Traffic",
"Covenant Transport",
"Cowan Logistics",
"COYOTE",
"Creech Brokerage",
"CRST The Transportation",
"Custom Pro",
"CW Carriers",
"Czechmate",
"D2 FREIGHT",
"Day & Ross",
"DestiNATION Transport",
"DIAMOND LOGISTICS",
"Direct Connect Logistix",
"Direct Connect Transport",
"DSV A/S",
"Dupré Logistics",
"DYNAMIC LOGISTIX",
"Dynamo Freight",
"Ease Logistics",
"EASE Logistics Services",
"Echo Global",
"Edge Logistics",
"ELI Solutions",
"ELIT Transit Solutions",
"EMERGE TECH",
"England Logistics",
"eShipping",
"Evans Delivery",
"EVE INTERNATIONAL",
"everest transportation",
"EXPRESS LOGISTICS",
"Fastmore",
"FEDEX CUSTOM FREIGHT",
"Fifth Wheel Freight",
"FitzMark",
"FLS Transportation",
"FreedomTrans USA",
"Freezpak Logistics",
"FreightEx Logistics",
"Frontier Logistics",
"Genpro Inc.",
"GIX Logistics",
"GlobalTranz",
"GO2 EXPRESS",
"Gulf Relay Logistics",
"Haines City Truck",
"Hazen Transfer",
"High Tide Logistics",
"HTS Logistics",
"Hub Group",
"InstiCo",
"Integrity Express",
"ITF LOGISTICS GROUP",
"ITS Logistics",
"J .B. Hunt",
"JEAR Logistics",
"jerue Companies",
"Johanson Transportation",
"John J. Jerue Truck",
"K & L FREIGHT",
"KAG Logistics",
"Keller Freight Solutions",
"Kenco Transportation",
"Kirsch Transportation",
"Kiss Logistics",
"KLG Logistics Services",
"Knight-Swift Transportation",
"Koch Logistics",
"Kodiak Transportation",
"Koola Logistics",
"Landmark Logistics",
"LandStar Global",
"LANDSTAR INWAY",
"Landstar Ranger",
"LIBERTY COMMERICAL",
"LinQ Transport",
"Loadsmart",
"Logistic Dynamics",
"Logistics One Brokerage",
"Logistics Plus",
"Longship",
"Magellan Transport",
"Marathon Transport",
"Marten Transport",
"Matson Logistics",
"Max Trans Logistics",
"McLeod Logistics",
"MDB Logistics",
"Meadow Lark Agency",
"MegaCorp Logistics",
"MIDWEST EXPRESS FREIGHT",
"Mode Global",
"Moeller Logistics",
"MoLo Solutions",
"Motus Freight",
"Nationwide Logistics",
"Navajo Expedited",
"Network Transport",
"NFI",
"Nolan Transportation Group",
"NORTHEAST LOGISTICS",
"ODW Logistics",
"Old Frontier Family",
"OpenRoad Transportation",
"Packer Transportation",
"PAM Transport",
"PATHMARK TRANSPORTATION",
"Patterson Companies",
"Paul Logistics",
"Payne Trucking",
"PEPSI LOGISTICS",
"Performance Logistics",
"Perimeter Logistics",
"PHOENIX SUPPLY",
"PINK PANTHERS",
"PLS Logistics",
"Priority-1",
"R&R Express",
"R2 Logistics",
"Radiant Logistics",
"RB Humphreys",
"Red Classic",
"Redwood logistics",
"Redwood Logistics",
"REED TRANSPORT ",
"Reliable Transportation",
"RFX",
"RJ Logistics",
"RJS",
"RLS Logistics",
"ROAR LOGISTICS",
"ROYAL TRANSPORTATION",
"RPM carrier",
"RPM Freight Systems",
"RXO, Inc.",
"RYAN TRANSPORTATION ",
"Ryder Supply Chain",
"S & H Transport",
"S and S Nationwide",
"Scan Global Logistics",
"Schneider",
"Schneider Shipment",
"Scotlynn USA Division",
"Simple Logistics",
"Spartan Logistics",
"SPI Logistics",
"Spirit Logistics",
"Spot Inc",
"ST Freight",
"Starland Global Logistics",
"Steam Logistics",
"Summit Eleven",
"Sunrise Logistics",
"Surge Transportation",
"Synchrogistics",
"TA Services",
"Tallgrass Freight",
"TAYLOR LOGISTICS",
"TERRY ENTERPRISES",
"The Worthington Company",
"Thomas E. Keller Trucking",
"TII Logistics",
"TORCH LOGISTICS",
"Torch3pl",
"Total Quality Logistics",
"TRAFFIX",
"Trailer Bridge",
"TransAmerica Express",
"Transfix",
"TRANSLOOP",
"Transplace",
"Trident Transport",
"Trinity Logistics",
"Triple T Transport",
"U.S. Xpress",
"Uber Freight",
"UNIVERSAL CAPACITY",
"Universal Logistics",
"Unlimited Logistics",
"US Logistics",
"US1 Network",
"USAT Logistics",
"Value Logistics",
"Venture Connect",
"VERIHA LOGISTICS",
"Veritiv Logistics",
"Watco Logistics",
"Werner Enterprises",
"West Motor Freight",
"Worldwide Express ",
"XPO Logistics",
"Yellow Logistics",
"Zengistics",
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
