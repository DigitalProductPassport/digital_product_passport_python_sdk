import json
from solidity_python_sdk.main import DigitalProductPassportSDK

def deploy_and_set_product(details_file_path):
    # Initialize the SDK
    sdk = DigitalProductPassportSDK()

    # Load the details from the JSON file
    with open('details.json', 'r') as f:
        product_details = json.load(f)

    # Extract necessary details from the JSON data
    product_id = product_details.get("productId")
    if not product_id:
        raise ValueError("Product ID not found in JSON file")

    # Deploy the contract
    account_address = sdk.account.address  # or fetch it from the details if needed
    contract_address = sdk.product_passport.deploy(account_address)
    
    # Print the address of the deployed contract
    print(f"Contract deployed at address: {contract_address}")

    # Set product details on the deployed contract
    tx_receipt = sdk.product_passport.set_product_data(contract_address, product_id, product_details)
    
    if tx_receipt["status"] == 1:
        print("Product details set successfully.")
    else:
        print("Failed to set product details.")
    
    return contract_address
