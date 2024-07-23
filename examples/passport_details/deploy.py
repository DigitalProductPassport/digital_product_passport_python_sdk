import json
from web3 import Web3
from datetime import datetime
from solidity_python_sdk.main import DigitalProductPassportSDK

# Initialize SDK
sdk = DigitalProductPassportSDK()

# Product details to deploy
product_details = {
    "uid": "BRG-2023-001",
    "gtin": "7894561230123",
    "taricCode": "1905",
    "manufacturerInfo": "Sweet Delights",
    "consumerInfo": "Enjoy your Brigadeiro responsibly! Perfect for parties, celebrations, and gifting.",
    "endOfLifeInfo": "Dispose of the packaging properly. Recycle where facilities exist."
}

# Product data to deploy
product_data = {
    "productId": 1,
    "description": "Brigadeiro Product Passport",
    "manuals": ["QmbnzbFDcmtJhyw5XTLkcnkJMhW86YZg6oc3FsNBeN2r4W"],
    "specifications": ["QmbnzbFDcmtJhyw5XTLkcnkJMhW86YZg6oc3FsNBeN2r4W"],
    "batchNumber": "BRG-2023-001",
    "productionDate": "2023-06-20",
    "expiryDate": "2023-12-31",
    "certifications": "FDA-5678",
    "warrantyInfo": "Not applicable",
    "materialComposition": "Condensed milk, cocoa powder, butter, chocolate sprinkles",
    "complianceInfo": "Compliant with local food safety regulations",
    "ipfs": "QmWDYhFAaT89spcqbKYboyCm6mkYSxKJaWUuS18Akmw96t"
}

def convert_to_unix_timestamp(date_string):
    date_format = "%Y-%m-%d %H:%M:%S"
    dt = datetime.strptime(date_string, date_format)
    return int(dt.timestamp())

def deploy_product_passport():
    product_passport_address = sdk.product_passport.deploy(sdk.account.address)
    sdk.product_passport.authorize_entity(product_passport_address, sdk.account.address)
    
    product_id = product_data['productId']
    sdk.product_passport.set_product(product_passport_address, product_id, product_details)
    
    result = sdk.product_passport.set_product_data(product_passport_address, product_id, product_data)
    
    print(f"ProductPassport Contract Address: {product_passport_address}")
    print(f"Set Product Result: {result}")

    return product_passport_address

def deploy_batch_contract(product_passport_address):
    geolocations = [
        {"id": "1", "latitude": "40.7128", "longitude": "-74.0060", "additionalInfo": "New York City, USA"},
        {"id": "2", "latitude": "34.0522", "longitude": "-118.2437", "additionalInfo": "Los Angeles, USA"},
        {"id": "3", "latitude": "51.5074", "longitude": "-0.1278", "additionalInfo": "London, UK"},
        {"id": "4", "latitude": "35.6895", "longitude": "139.6917", "additionalInfo": "Tokyo, Japan"},
        {"id": "5", "latitude": "-33.8688", "longitude": "151.2093", "additionalInfo": "Sydney, Australia"}
    ]

    batch_address = sdk.batch.deploy(product_passport_address)

    for i, geo in enumerate(geolocations):
        assembling_time = convert_to_unix_timestamp("2023-06-20 12:00:00")
        batch_details = {
            "batchId": i + 1,
            "amount": 100,
            "assemblingTime": assembling_time,
            "transportDetails": f"Shipped via Express {i + 1}",
            "ipfsHash": product_data['ipfs']
        }

        result = sdk.batch.create_batch(batch_address, batch_details)
        print(f"Batch {i+1} Contract Address: {batch_address}")
        print(f"Set Batch {i+1} Result: {result}")

        sdk.geolocation.add_geolocation(batch_address, geo['id'], geo['latitude'], geo['longitude'], geo['additionalInfo'])

    return batch_address

if __name__ == '__main__':
    product_passport_address = deploy_product_passport()
    batch_addresses = deploy_batch_contract(product_passport_address)
    print(f"Deployed Batch Addresses: {batch_addresses}")
