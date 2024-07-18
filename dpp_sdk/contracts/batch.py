import json
import logging
import os
from web3 import Web3


class Batch:
    def __init__(self, web3: Web3, account, contract):
        self.web3 = web3
        self.account = account
        self.contract = contract
        self.logger = logging.getLogger(__name__) 

    def deploy(self, product_passport_address):
        self.logger.info(f"Deploying Batch contract from {self.account.address}")
        Contract = self.web3.eth.contract(abi=self.contract["abi"], bytecode=self.contract["bytecode"])
        tx_hash = Contract.constructor(product_passport_address).transact({'from': self.account.address})
        tx_receipt = self.web3.eth.waitForTransactionReceipt(tx_hash)
        contract_address = tx_receipt.contractAddress
        self.logger.info(f"Batch contract deployed at address: {contract_address}")
        return contract_address

    def create_batch(self, contract_address, batch_details):
        contract = self.web3.eth.contract(address=contract_address, abi=self.contracts['Batch']['abi'])
        tx_hash = contract.functions.createBatch(
            batch_details["batchId"],
            batch_details["batchNumber"],
            batch_details["productionDate"],
            batch_details["expiryDate"],
            batch_details["quantity"]
        ).transact({'from': self.account.address})
        tx_receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
        return tx_receipt

    def get_batch(self, contract_address, batch_id):
        contract = self.web3.eth.contract(address=contract_address, abi=self.contracts['Batch']['abi'])
        return contract.functions.getBatch(batch_id).call()
