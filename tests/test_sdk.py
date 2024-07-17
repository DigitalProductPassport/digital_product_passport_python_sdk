import json
import pytest
from web3 import Web3
from dpp_sdk.main import DigitalProductPassportSDK

@pytest.fixture
def sdk():
    return DigitalProductPassportSDK()

def test_load_abi(sdk):
    abi = sdk.load_abi("ProductPassport.sol/ProductPassport.json")
    assert isinstance(abi, list)

def test_deploy_contract(sdk):
    abi = sdk.product_passport_abi
    bytecode = "0x608060405234801561001057600080fd5b506040516101f83803806101f88339818101604052602081101561003357600080fd5b505160005560d0806100486000396000f3fe608060405260043610601f5760003560e01c80632e64cec1146024575b600080fd5b603660048036036020811015603857600080fd5b81019080803590602001909291905050506045565b005b6000548156fea2646970667358221220b85b891f31762c5cbec45f3e6234ff6b86ef89f82f5d9d5c2bdf506ef03bbeb664736f6c63430007040033"
    contract_address = sdk.deploy_contract(abi, bytecode)
    assert Web3.isAddress(contract_address)

def test_create_product_passport(sdk):
    contract_address = "0xe4D526e461Fb26B27Eeb142344B06Bf4c4688297"
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
    contract_address = "0xe4D526e461Fb26B27Eeb142344B06Bf4c4688297"
    product_id = 1
    product_passport = sdk.interact_with_existing_contract(contract_address, product_id)
    assert product_passport["productId"] == product_id
