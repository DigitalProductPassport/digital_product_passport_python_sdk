import json
from web3 import Web3
from solidity_python_sdk.main import DigitalProductPassportSDK

# Initialize SDK
passport = DigitalProductPassportSDK()

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

def deploy_product_data():
    # Deploy the contract
    contract_address = passport.product_passport.deploy()
    passport.product_passport.authorize_entity(contract_address, passport.account.address)
    # Set product details
    product_id = product_data['productId']
    passport.product_passport.set_product(contract_address, product_id, product_details)
    
    # Set additional product data
    result = passport.product_passport.set_product_data(contract_address, product_id, product_data)
    
    print(f"Contract Address: {contract_address}")
    print(f"Set Product Result: {result}")

if __name__ == '__main__':
    deploy_product_data()
