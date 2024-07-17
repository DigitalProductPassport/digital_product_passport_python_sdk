import json
import os
import requests
from web3 import Web3
from dotenv import load_dotenv

class DigitalProductPassportSDK:
    def __init__(self, provider_url=None, private_key=None):
        if provider_url and private_key:
            self.web3 = Web3(Web3.HTTPProvider(provider_url))
            self.account = self.web3.eth.account.from_key(private_key)
        else:
            load_dotenv()
            provider_url = os.getenv("PROVIDER_URL")
            private_key = os.getenv("PRIVATE_KEY")
            self.web3 = Web3(Web3.HTTPProvider(provider_url))
            self.account = self.web3.eth.account.from_key(private_key)
        if private_key is None:
            raise ValueError("Private key must be provided.")
        self.ownership_abi = self.load_abi_from_github("https://raw.githubusercontent.com/DigitalProductPassport/SmartContracts/main/abis/Ownership.json")
        self.product_passport_abi = self.load_abi_from_github("https://raw.githubusercontent.com/DigitalProductPassport/SmartContracts/main/abis/ProductPassport.json")
        self.batch_abi = self.load_abi_from_github("https://raw.githubusercontent.com/DigitalProductPassport/SmartContracts/main/abis/Batch.json")

    def load_abi_from_github(self, url):
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    def deploy_contract(self, abi, bytecode):
        contract = self.web3.eth.contract(abi=abi, bytecode=bytecode)
        tx_hash = contract.constructor().transact({'from': self.account.address})
        tx_receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
        return tx_receipt.contractAddress

    def create_product_passport(self, contract_address, product_details):
        contract = self.web3.eth.contract(address=contract_address, abi=self.product_passport_abi)
        tx_hash = contract.functions.createProductPassport(
            product_details["productId"],
            product_details["description"],
            product_details["manuals"],
            product_details["specifications"],
            product_details["batchNumber"],
            product_details["productionDate"],
            product_details["expiryDate"],
            product_details["certifications"],
            product_details["warrantyInfo"],
            product_details["materialComposition"],
            product_details["complianceInfo"],
            product_details["ipfs"]
        ).transact({'from': self.account.address})
        tx_receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
        return tx_receipt

    def interact_with_existing_contract(self, contract_address, product_id):
        contract = self.web3.eth.contract(address=contract_address, abi=self.product_passport_abi)
        product_passport = contract.functions.getProductPassport(product_id).call()
        return product_passport

    def create_batch(self, contract_address, batch_details):
        contract = self.web3.eth.contract(address=contract_address, abi=self.batch_abi)
        tx_hash = contract.functions.createBatch(
            batch_details["batchId"],
            batch_details["batchNumber"],
            batch_details["productionDate"],
            batch_details["expiryDate"],
            batch_details["quantity"]
        ).transact({'from': self.account.address})
        tx_receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
        return tx_receipt

    def interact_with_existing_batch(self, contract_address, batch_id):
        contract = self.web3.eth.contract(address=contract_address, abi=self.batch_abi)
        batch_details = contract.functions.getBatch(batch_id).call()
        return batch_details
