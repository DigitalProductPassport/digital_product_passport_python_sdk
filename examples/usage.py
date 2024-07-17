from dpp_sdk.main import DigitalProductPassportSDK

sdk = DigitalProductPassportSDK()

product_details_path = 'path_to_product_details.json'
with open(product_details_path, 'r') as f:
    product_details = json.load(f)

existing_contract_address = 'existing_contract_address_here'
product_id = 1
passport = sdk.interact_with_existing_contract(existing_contract_address, product_id)
print(json.dumps(passport, indent=2))
