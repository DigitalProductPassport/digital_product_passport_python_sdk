import json
import logging
import os
from web3 import Web3
from solidity_python_sdk.utils import utils


class Geolocation:
    """
    Interface for interacting with the Geolocation smart contract.

    Attributes:
        web3 (Web3): Web3 instance for blockchain interactions.
        account (Account): Ethereum account used for transactions.
        contract (dict): ABI and bytecode of the Geolocation contract.
        logger (Logger): Logger instance for logging information and debug messages.
    """

    def __init__(self, sdk):
        """
        Initializes the Geolocation class with the provided SDK instance.

        Args:
            sdk (DigitalProductPassportSDK): The SDK instance for blockchain interactions.
        """
        self.web3 = sdk.web3
        self.account = sdk.account
        self.contract = sdk.contracts['Geolocation']
        self.logger = logging.getLogger(__name__)

    def set_geolocation(self, contract_address, batch_id, latitude, longitude):
        """
        Adds geolocation information for a specific batch in the Geolocation contract.

        Args:
            contract_address (str): The address of the deployed Geolocation contract.
            batch_id (string): The unique identifier for the batch.
            latitude (string): The latitude of the geolocation.
            longitude (string): The longitude of the geolocation.

        Returns:
            dict: The transaction receipt containing details of the transaction.
        """
        contract = self.web3.eth.contract(address=contract_address, abi=self.contract['abi'])
        tx_hash = contract.functions.setGeolocation(batch_id, latitude, longitude).transact({'from': self.account.address})
        tx_receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash, timeout=300)
        return tx_receipt

    def get_geolocation(self, contract_address, batch_id):
        """
        Retrieves the geolocation information for a specific batch from the Geolocation contract.

        Args:
            contract_address (str): The address of the deployed Geolocation contract.
            batch_id (str): The unique identifier for the batch.

        Returns:
            tuple: A tuple containing the latitude and longitude of the geolocation.
        """
        contract = self.web3.eth.contract(address=contract_address, abi=self.contract['abi'])
        return contract.functions.getGeolocation(batch_id)().call()
