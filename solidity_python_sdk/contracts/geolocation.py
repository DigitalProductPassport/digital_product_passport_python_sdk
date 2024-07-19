import json
import logging
import os
from web3 import Web3
from solidity_python_sdk import utils


class Geolocation:
    def __init__(self, sdk):
        self.web3 = sdk.web3
        self.account = sdk.account
        self.contract = sdk.contracts['Geolocation']
        self.logger = logging.getLogger(__name__) 

    def add_geolocation(self, contract_address, batch_id, latitude, longitude):
        contract = self.web3.eth.contract(address=contract_address, abi=self.contract['abi'])
        tx_hash = contract.functions.addGeolocation(batch_id, latitude, longitude).transact({'from': self.account.address})
        tx_receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
        return tx_receipt

    def get_geolocation(self, contract_address, batch_id):
        contract = self.web3.eth.contract(address=contract_address, abi=self.contract['abi'])
        return contract.functions.getGeolocation(batch_id)().call()
