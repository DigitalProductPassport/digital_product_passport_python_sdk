import json
import pytest
from web3 import Web3
from dpp_sdk.main import DigitalProductPassportSDK

@pytest.fixture
def sdk():
    return DigitalProductPassportSDK()

def test_load_contract(sdk):
    contract = sdk.load_contract("ProductPassport.sol/ProductPassport.json")
    assert "abi" in contract
    assert "bytecode" in contract

def test_deploy_contract(sdk):
    contract = sdk.product_passport_contract
    contract_address = sdk.deploy_contract(contract)
    assert Web3.isAddress(contract_address)

def test_create_product_passport(sdk):
    contract_address = sdk.deploy_contract(sdk.product_passport_contract)
    product_details = {
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
    tx_receipt = sdk.create_product_passport(contract_address, product_details)
    assert tx_receipt["status"] == 1

def test_interact_with_existing_contract(sdk):
    contract_address = sdk.deploy_contract(sdk.product_passport_contract, sdk.account.address)
    product_id = 1
    product_passport = sdk.interact_with_existing_contract(contract_address, product_id)
    assert product_passport["productId"] == product_id

def test_create_batch(sdk):
    passport_contract_address = sdk.deploy_contract(sdk.product_passport_contract, sdk.account.address)
    contract_address = sdk.deploy_contract(sdk.batch_contract, passport_contract_address, sdk.account.address)
    batch_details = {
        "batchId": 1,
        "batchNumber": "BRG-2023-001",
        "productionDate": "2023-06-20",
        "expiryDate": "2023-12-31",
        "quantity": 1000
    }
    tx_receipt = sdk.create_batch(contract_address, batch_details)
    assert tx_receipt["status"] == 1

def test_interact_with_existing_batch(sdk):
    passport_contract_address = sdk.deploy_contract(sdk.product_passport_contract, sdk.account.address)
    contract_address = sdk.deploy_contract(sdk.batch_contract, passport_contract_address, sdk.account.address)
    batch_id = 1
    batch_details = sdk.interact_with_existing_batch(contract_address, batch_id)
    assert batch_details["batchId"] == batch_id
