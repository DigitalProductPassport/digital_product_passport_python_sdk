import json
import logging
import os
from web3 import Web3
from eth_account import Account

class Batch:
    def __init__(self, web3: Web3, account, contract):
        """
        Initializes the Batch instance.

        Args:
            web3 (Web3): An instance of the Web3 class.
            account: The account to be used for transactions.
            contract: The contract details including ABI and bytecode.
        """
        self.web3 = web3
        self.account = account
        self.contract = contract
        self.logger = logging.getLogger(__name__)

    def deploy(self, product_passport_address):
        """
        Deploys the Batch contract to the blockchain.
        
        Args:
            product_passport_address (str): The address of the ProductPassport contract.
        
        Returns:
            str: The address of the deployed contract.
        """
        self.logger.info(f"Deploying Batch contract from {self.account.address}")
        Contract = self.web3.eth.contract(abi=self.contract["abi"], bytecode=self.contract["bytecode"])
        tx = Contract.constructor(product_passport_address).build_transaction({
            'from': self.account.address,
            'nonce': self.web3.eth.get_transaction_count(self.account.address),
            'gas': 2000000,
            'gasPrice': self.web3.to_wei('50', 'gwei')
        })
        signed_tx = self.web3.eth.account.sign_transaction(tx, self.account.key)
        tx_hash = self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        tx_receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
        contract_address = tx_receipt.contractAddress

        self.logger.info(f"Batch contract deployed at address: {contract_address}")
        return contract_address

    def create_batch(self, contract_address, batch_details):
        """
        Creates a new batch in the Batch contract.
        
        Args:
            contract_address (str): The address of the deployed contract.
            batch_details (dict): A dictionary containing batch details.
        
        Returns:
            dict: The transaction receipt.
        """
        contract = self.web3.eth.contract(address=contract_address, abi=self.contract['abi'])
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
        """
        Retrieves the batch details from the Batch contract.
        
        Args:
            contract_address (str): The address of the deployed contract.
            batch_id (str): The unique identifier for the batch.
        
        Returns:
            dict: The batch details.
        """
        contract = self.web3.eth.contract(address=contract_address, abi=self.contract['abi'])
        return contract.functions.getBatch(batch_id).call()
