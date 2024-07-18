import logging
import json
from web3 import Web3
from dotenv import load_dotenv
import os
from dpp_sdk.contracts.product_passport import ProductPassport
from dpp_sdk.contracts.geolocation import Geolocation
from dpp_sdk.contracts.batch import Batch
from dpp_sdk.resources import ABI

class DigitalProductPassportSDK:
    """
    SDK for interacting with Digital Product Passport smart contracts.
    """

    def __init__(self, provider_url=None, private_key=None):
        """
        Initializes the SDK with a provider URL and private key.
        """
        logging.basicConfig(level=logging.DEBUG)
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
        self.contracts = self.load_all_contracts()
        self.product_passport = ProductPassport(self.web3, self.account, self.contracts['ProductPassport'])
        self.batch = Batch(self.web3, self.account, self.contracts["Batch"])
        self.geolocation = Geolocation(self.web3, self.account, self.contracts["Geolocation"])

        logging.info("DigitalProductPassportSDK initialized successfully.")

    def load_all_contracts(self):
        contracts = {}
        abi_folder_path = os.path.dirname(ABI.__file__)
        for filename in os.listdir(abi_folder_path):
            file_path = os.path.join(abi_folder_path, filename)
            if os.path.isdir(file_path) and filename.endswith('.sol'):
                contract_name = os.path.splitext(filename)[0]
                contract_path = os.path.join(file_path, f"{contract_name}.json")
                contracts[contract_name] = self.load_contract(contract_path)
        return contracts

    def load_contract(self, contract_path):
        with open(contract_path) as file:
            contract_interface = json.load(file)
        return {
            "abi": contract_interface['abi'],
            "bytecode": contract_interface['bytecode']
        }
