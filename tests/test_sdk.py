import pytest
from web3 import Web3
import logging
from solidity_python_sdk.main import DigitalProductPassportSDK, ProductPassport

# Setup logging
logging.basicConfig(level=logging.DEBUG)

@pytest.fixture()
def sdk():
    # Initialize the SDK
    return DigitalProductPassportSDK()

def test_load_contract(sdk):
    contract = sdk.contracts.get('ProductPassport')
    assert contract, "Contract 'ProductPassport' not found"
    assert 'abi' in contract, "ABI not found in 'ProductPassport'"
    assert 'bytecode' in contract, "Bytecode not found in 'ProductPassport'"
    logging.debug("Contract ABI and Bytecode loaded successfully")

def test_deploy_product_passport_contract(sdk):
    passport = ProductPassport(sdk)
    
    # Deploy the contract
    contract_address = passport.deploy(sdk.account.address)
    
    # Verify deployment
    assert Web3.is_address(contract_address), "Invalid contract address"
    logging.debug(f"Contract deployed at address: {contract_address}")

def test_set_and_get_product(sdk):
    passport = ProductPassport(sdk)
    
    # Deploy the contract
    contract_address = passport.deploy(sdk.account.address)
    logging.debug(f"Contract deployed at address: {contract_address}")

    # Authorize the contract with the deployed address
    entity_address = sdk.account.address
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

    # Retrieve and assert product details
    product_data_retrieved = passport.get_product(contract_address, "123456")
    assert product_data_retrieved[0] == "unique_id"
    assert product_data_retrieved[1] == "1234567890123"
    assert product_data_retrieved[2] == "1234"
    assert product_data_retrieved[3] == "Manufacturer XYZ"
    assert product_data_retrieved[4] == "Consumer XYZ"
    assert product_data_retrieved[5] == "Dispose properly"

def test_set_and_get_product_data(sdk):
    passport = ProductPassport(sdk)
    
    # Deploy the contract
    contract_address = passport.deploy(sdk.account.address)
    logging.debug(f"Contract deployed at address: {contract_address}")

    # Authorize the contract with the deployed address
    entity_address = sdk.account.address
    tx_receipt = passport.authorize_entity(contract_address, entity_address)
    logging.debug(f"Authorization transaction receipt: {tx_receipt}")

    # Define product data
    product_data = {
        "productId": 123456,
        "description": "Product description",
        "manuals": ["manual1.pdf"],
        "specifications": ["spec1.pdf"],
        "batchNumber": "123ABC",
        "productionDate": "2023-01-01",
        "expiryDate": "2023-12-31",
        "certifications": "ISO123",
        "warrantyInfo": "1 year",
        "materialComposition": "Materials",
        "complianceInfo": "Complies with regulations",
        "ipfs": "QmWDYhFAaT89spcqbKYboyCm6mkYSxKJaWUuS18Akmw96t"
    }

    # Set product data
    tx_receipt = passport.set_product_data(contract_address, 123456, product_data)
    logging.debug(f"Product data set transaction receipt: {tx_receipt}")

    # Retrieve and assert product data
    product_data_retrieved = passport.get_product_data(contract_address, 123456)
    assert product_data_retrieved[0] == "Product description"
    assert product_data_retrieved[1] == ["manual1.pdf"]
    assert product_data_retrieved[2] == ["spec1.pdf"]
    assert product_data_retrieved[3] == "123ABC"
    assert product_data_retrieved[4] == "2023-01-01"
    assert product_data_retrieved[5] == "2023-12-31"
    assert product_data_retrieved[6] == "ISO123"
    assert product_data_retrieved[7] == "1 year"
    assert product_data_retrieved[8] == "Materials"
    assert product_data_retrieved[9] == "Complies with regulations"
    assert product_data_retrieved[10] == "QmWDYhFAaT89spcqbKYboyCm6mkYSxKJaWUuS18Akmw96t"
