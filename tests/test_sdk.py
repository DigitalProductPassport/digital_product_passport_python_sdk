import pytest
from web3 import Web3
import logging
from solidity_python_sdk.main import DigitalProductPassportSDK, ProductPassport

@pytest.fixture()
def sdk():
    logging.basicConfig(level=logging.DEBUG)
    return DigitalProductPassportSDK()

def test_load_contract(sdk):
    contract = sdk.contracts.get('ProductPassport')
    assert contract, "Contract 'ProductPassport' not found"
    assert 'abi' in contract, "ABI not found in 'ProductPassport'"
    assert 'bytecode' in contract, "Bytecode not found in 'ProductPassport'"
    logging.debug("Contract ABI and Bytecode loaded successfully")

def test_deploy_product_passport_contract(sdk):
    passport = ProductPassport(sdk)
    contract_address = passport.deploy(sdk.account.address)
    assert Web3.is_address(contract_address), "Invalid contract address"
    logging.debug(f"Contract deployed at address: {contract_address}")

def test_set_and_get_product(sdk):
    passport = ProductPassport(sdk)
    
    # Deploy the contract
    contract_address = passport.deploy(sdk.account.address)
    logging.debug(f"Contract deployed at address: {contract_address}")

    # Authorize the account
    entity_address = contract_address
    tx_receipt = passport.authorize_entity(contract_address, entity_address)
    logging.debug(f"Authorization transaction receipt: {tx_receipt}")

    # Define product details
    product_details = {
        "uid": "unique_id",
        "gtin": "1234567890123",
        "taricCode": "1234",
        "manufacturerInfo": "Manufacturer XYZ",
        "consumerInfo": "Consumer XYZ",
        "endOfLifeInfo": "Dispose properly"
    }

    # Set product details
    tx_receipt = passport.set_product(contract_address, "123456", product_details)
    logging.debug(f"Product set transaction receipt: {tx_receipt}")

    # Retrieve product details
    product_data_retrieved = passport.get_product(contract_address, "123456")
    assert product_data_retrieved['uid'] == "unique_id"
    assert product_data_retrieved['gtin'] == "1234567890123"
    assert product_data_retrieved['taricCode'] == "1234"
    assert product_data_retrieved['manufacturerInfo'] == "Manufacturer XYZ"
    assert product_data_retrieved['consumerInfo'] == "Consumer XYZ"
    assert product_data_retrieved['endOfLifeInfo'] == "Dispose properly"

def test_set_and_get_product_data(sdk):
    passport = ProductPassport(sdk)
    
    # Deploy the contract
    contract_address = passport.deploy(sdk.account.address)
    logging.debug(f"Contract deployed at address: {contract_address}")

    # Authorize the account
    entity_address = contract_address
    tx_receipt = passport.authorize_entity(contract_address, entity_address)
    logging.debug(f"Authorization transaction receipt: {tx_receipt}")

    # Define product data
    product_data = {
        "description": "Product description",
        "manuals": ["manual1.pdf"],
        "specifications": ["spec1.pdf"],
        "batchNumber": "123ABC",
        "productionDate": "2023-01-01",
        "expiryDate": "2023-12-31",
        "certifications": "ISO123",
        "warrantyInfo": "1 year",
        "materialComposition": "Materials",
        "complianceInfo": "Complies with regulations"
    }

    # Set product data
    tx_receipt = passport.set_product_data(contract_address, 123456, product_data)
    logging.debug(f"Product data set transaction receipt: {tx_receipt}")

    # Retrieve product data
    product_data_retrieved = passport.get_product_data(contract_address, 123456)
    assert product_data_retrieved['description'] == "Product description"
    assert product_data_retrieved['manuals'] == ["manual1.pdf"]
    assert product_data_retrieved['specifications'] == ["spec1.pdf"]
    assert product_data_retrieved['batchNumber'] == "123ABC"
    assert product_data_retrieved['productionDate'] == "2023-01-01"
    assert product_data_retrieved['expiryDate'] == "2023-12-31"
    assert product_data_retrieved['certifications'] == "ISO123"
    assert product_data_retrieved['warrantyInfo'] == "1 year"
    assert product_data_retrieved['materialComposition'] == "Materials"
    assert product_data_retrieved['complianceInfo'] == "Complies with regulations"
