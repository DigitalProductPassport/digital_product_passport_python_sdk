import json
import logging
import os
from web3 import Web3

class ProductPassport:
    def __init__(self, web3: Web3, account, contract):
        self.web3 = web3
        self.account = account
        self.contract = contract
        self.logger = logging.getLogger(__name__) 


    def deploy(self, initial_owner=None):
        self.logger.info(f"Deploying ProductPassport contract from {self.account.address}")
        Contract = self.web3.eth.contract(abi=self.contract["abi"], bytecode=self.contract["bytecode"])
        tx_hash = Contract.constructor(initial_owner or self.account.address).transact({'from': self.account.address})
        tx_receipt = self.web3.eth.waitForTransactionReceipt(tx_hash)
        contract_address = tx_receipt.contractAddress
        self.logger.info(f"ProductPassport contract deployed at address: {contract_address}")
        return contract_address

    def set_product(self, contract_address, product_id, product_details):
        contract = self.web3.eth.contract(address=contract_address, abi=self.contracts['ProductPassport']['abi'])
        tx_hash = contract.functions.setProduct(
            product_id,
            product_details["uid"],
            product_details["gtin"],
            product_details["taricCode"],
            product_details["manufacturerInfo"],
            product_details["consumerInfo"],
            product_details["endOfLifeInfo"]
        ).transact({'from': self.account.address})
        tx_receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
        return tx_receipt

    def get_product(self, contract_address, product_id):
        contract = self.web3.eth.contract(address=contract_address, abi=self.contracts['ProductPassport']['abi'])
        return contract.functions.getProduct(product_id).call()

    def set_product_data(self, contract_address, product_id, product_data):
        contract = self.web3.eth.contract(address=contract_address, abi=self.contracts['ProductPassport']['abi'])
        tx_hash = contract.functions.setProductData(
            product_id,
            product_data["description"],
            product_data["manuals"],
            product_data["specifications"],
            product_data["batchNumber"],
            product_data["productionDate"],
            product_data["expiryDate"],
            product_data["certifications"],
            product_data["warrantyInfo"],
            product_data["materialComposition"],
            product_data["complianceInfo"]
        ).transact({'from': self.account.address})
        tx_receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
        return tx_receipt

    def get_product_data(self, contract_address, product_id):
        contract = self.web3.eth.contract(address=contract_address, abi=self.contracts['ProductPassport']['abi'])
        return contract.functions.getProductData(product_id).call()
