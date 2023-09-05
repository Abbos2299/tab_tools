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

app = Flask(__name__)
cred = credentials.Certificate('tab-tools-firebase-adminsdk-8ncav-4f5ccee9af.json')
firebase_admin.initialize_app(cred)


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

# The rest of your code remains the same

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)



@app.route('/launchidentify', methods=['GET'])
def launch_python_file():
    user_uid = request.args.get('uid')
    
    bucket_name = 'tab-tools.appspot.com'
    bucket = storage.bucket(bucket_name)
    folder_name = user_uid  # Replace with the appropriate user UID
    blobs = bucket.list_blobs(prefix=folder_name)
     
    # Wait for 1 seconds
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

        # Download the file from Firebase
        response = requests.get(file_url)
        with open(file_name, 'wb') as f:
            f.write(response.content)

        # Process the downloaded file with Pytesseract
        images = convert_from_path(file_name)
        all_text = ""
        for i, image in enumerate(images):
            text = pytesseract.image_to_string(image)
            all_text += text
            
        #print(all_text)
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
"American Transport Group",
"Amsino",
"Amstan Logistics",
"ArcBest Corp",
"Achest",
"Archerhub",
"Sunset Transportation",
"Armstrong Transport",
"Arrive Logistics",
"ASCEND",
"Ascent Global",
"Ashley Distribution",
"ATS Logistics",
"axlelogistics",
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
"C&L",
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
"Dupre Logistics",
"DYNAMIC LOGISTIX",
"Dynamo Freight",
"Ease Logistics",
"EASE Logistics Services",
"Echo Global",
"Edge Logistics",
"ELISqutions",
"ELITE TRANSITSOLU",
"emergemarket",
"englandlogistics",
"eShipping",
"Evans Delivery",
"EVE INTERNATIONAL",
"everest",
"EXPRESS LOGISTICS",
"Fastmore",
"FEDEX CUSTOM CRITICAL",
"Fifth Wheel Freight",
"FitzMark",
"FLS Transportation",
"freedomtransusa",
"Freezpak Logistics",
"FreightEx Logistics",
"Frontier Logistics",
"Genpro Inc.",
"GIX Logistics",
"GlobalTranz",
"G02 EXPRESS",
"GulfRelay",
"Haines City Truck",
"Hazen Transfer",
"High Tide Logistics",
"HTS Logistics",
"Hub Group",
"InstiCo",
"Integrity Express",
"ITF LOGISTICS GROUP",
"ITS Logistics",
"J.B. Hunt",
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
"LIBERTY",
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
"NTG",
"NORTH EAST LOGISTICS",
"ODW Logistics",
"Old Frontier Family",
"OpenRoad Transportation",
"Packer Transponallun",
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
"PLS",
"Priority 1",
"R&R FREIGHT",
"R2 Logistics",
"Radiant Logistics",
"RB Humphreys",
"Red Classic",
"Redwood",
"REED TRANSPORT ",
"RTS",
"RFX",
"RJ Logistics",
"RJ S",
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
"SCAN GLOBAL",
"Schneider",
"Schneider Shipment",
"Scotlynn USA Division",
"Sim Ie Lo istics,LLC",
"Spartan Logistics",
"SP1 Logistics",
"Spirit Logistics",
"spotinc",
"ST Freight",
"Starland Global Logistics",
"Steam Logistics",
"Summit E1even",
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
"TransAm Logistics",
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

        if broker_counts[most_used_broker] > 0:
            print(most_used_broker)

            # Correct the identified broker company names if needed
            if most_used_broker == "J.B. Hunt":
                most_used_broker = "J. B. Hunt Transportation"
                subprocess.call([sys.executable, "jbhunt.py", user_uid, most_used_broker, file_name])
            
            elif most_used_broker == "Priority 1":
                most_used_broker = "Priority 1 Logistics"
    
            elif most_used_broker == "G02 EXPRESS":
                most_used_broker = "GO2 EXPRESS"
                
            elif most_used_broker == "NTG":
                most_used_broker = "Nolan Transportation Group, LLC" 
    
            elif most_used_broker == "SCAN GLOBAL":
                most_used_broker = "SCAN GLOBAL LOGISTICS"
    
            elif most_used_broker == "everest":
                most_used_broker = "EVEREST transportation systems"
    
            elif most_used_broker == "PLS":
                most_used_broker = "PLS Logistics Services"
    
            elif most_used_broker == "LIBERTY":
                most_used_broker = "LIBERTY COMMERCIAL"
    
            elif most_used_broker == "Redwood":
                most_used_broker = "REDWOOD"
    
            elif most_used_broker == "NORTH EAST LOGISTICS":
                most_used_broker = "NORTHEAST LOGISTICS"
    
            elif most_used_broker == "TransAm Logistics":
                most_used_broker = "TransAm Logistics, Inc"
    
            elif most_used_broker == "ELISqutions":
                most_used_broker = "ELI Solutions, LLC"
    
            elif most_used_broker == "freedomtransusa":
                most_used_broker = "Freedom Trans USA, LLC"
    
            elif most_used_broker == "C&L":
                most_used_broker = "C & L LOGISTICS, INC."
    
            elif most_used_broker == "GulfRelay":
                most_used_broker = "Gulf Rlay Logistics, LLC"
    
            elif most_used_broker == "axlelogistics":
                most_used_broker = "AXLE LOGISTICS, LLC"
    
            elif most_used_broker == "Achest":
                most_used_broker = "ArcBest Dedicated, LLC"
                
            elif most_used_broker == "Sim Ie Lo istics,LLC":
                most_used_broker = "Simple Logistics, LLC"
    
            elif most_used_broker == "RJ S":
                most_used_broker = "RJS"
    
            elif most_used_broker == "FEDEX CUSTOM CRITICAL":
                most_used_broker = "FEDEX CUSTOM CRITICAL"
    
            elif most_used_broker == "englandlogistics":
                most_used_broker = "englandlogistics"
    
            elif most_used_broker == "Summit E1even":
                most_used_broker = "Summit Eleven Inc"
    
            elif most_used_broker == "ELITE TRANSITSOLU":
                most_used_broker = "ELITE TRANSIT"
    
            elif most_used_broker == "RTS":
                most_used_broker = "Reliable Transportation Soiutions"
    
            elif most_used_broker == "spotinc":
                most_used_broker = "SPOT"
    
            elif most_used_broker == "emergemarket":
                most_used_broker = "EMERGET ECH LLC" 
    
            elif most_used_broker == "R&R FREIGHT":
                most_used_broker = "R&R Freight Logistics, LLC"
    
            elif most_used_broker == "Packer Transponallun":
                most_used_broker = "Packer Transportation & Logistics"
    
            elif most_used_broker == "SP1 Logistics":
                most_used_broker = "SPI Logistics"
    
            elif most_used_broker == "American Transport Group":
                most_used_broker = "American Transport Group, LLC"        

        else:
            print("RC don't identified")

        # Wait for 1 seconds
        time.sleep(1)
        # Delete the file
        os.remove(file_name)

    else:
        print('No files found in the folder')

    return 'Success'
def get_access_token(bucket_name, file_name):
    bucket = storage.bucket(bucket_name)
    blob = bucket.blob(file_name)
    access_token = blob.generate_signed_url(expiration=datetime.timedelta(minutes=15))

    return access_token
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
