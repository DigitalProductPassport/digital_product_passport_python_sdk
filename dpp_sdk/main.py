import json
import os
from web3 import Web3
from dotenv import load_dotenv
from dpp_sdk.resources import ABI

class DigitalProductPassportSDK:
    """
    SDK for interacting with Digital Product Passport smart contracts.

    Attributes:
        web3 (Web3): Instance of Web3 for interacting with Ethereum blockchain.
        account (LocalAccount): Account instance for signing transactions.
        product_passport_contract (dict): ABI and bytecode for the Product Passport contract.
        batch_contract (dict): ABI and bytecode for the Batch contract.
    """

    def __init__(self, provider_url=None, private_key=None):
        """
        Initialize the SDK with optional provider URL and private key.

        Args:
            provider_url (str, optional): Ethereum provider URL.
            private_key (str, optional): Private key for the Ethereum account.

        Raises:
            ValueError: If private key is not provided.
        """
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
        
        self.product_passport_contract = self.load_contract("ProductPassport.sol/ProductPassport.json")
        self.batch_contract = self.load_contract("Batch.sol/Batch.json")

    def load_contract(self, contract_path):
        """
        Load the contract's ABI and bytecode from the local JSON file.

        Args:
            contract_path (str): Path to the contract JSON file.

        Returns:
            dict: Loaded contract containing ABI and bytecode.
        """
        ABI_PATH = os.path.join(os.path.dirname(ABI.__file__), contract_path)
        with open(ABI_PATH) as file:
            contract_interface = json.load(file)
        return {
            "abi": contract_interface['abi'],
            "bytecode": contract_interface['bytecode']
        }

    def deploy_contract(self, contract):
        """
        Deploy a smart contract to the blockchain.

        Args:
            contract (dict): Contract containing ABI and bytecode.

        Returns:
            str: Address of the deployed contract.
        """
        Contract = self.web3.eth.contract(abi=contract['abi'], bytecode=contract['bytecode'])
        tx_hash = Contract.constructor({'initialOwner' : self.account.address }).transact({'from': self.account.address})
        tx_receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
        return tx_receipt.contractAddress

    def authorize_entity(self, contract_address, entity_address):
        """
        Authorize an entity in the Product Passport contract.

        Args:
            contract_address (str): Address of the Product Passport contract.
            entity_address (str): Address of the entity to authorize.

        Returns:
            dict: Transaction receipt.
        """
        contract = self.web3.eth.contract(address=contract_address, abi=self.product_passport_contract['abi'])
        tx_hash = contract.functions.authorizeEntity(entity_address).transact({'from': self.account.address})
        tx_receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
        return tx_receipt

    def revoke_entity(self, contract_address, entity_address):
        """
        Revoke an entity in the Product Passport contract.

        Args:
            contract_address (str): Address of the Product Passport contract.
            entity_address (str): Address of the entity to revoke.

        Returns:
            dict: Transaction receipt.
        """
        contract = self.web3.eth.contract(address=contract_address, abi=self.product_passport_contract['abi'])
        tx_hash = contract.functions.revokeEntity(entity_address).transact({'from': self.account.address})
        tx_receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
        return tx_receipt

    def set_product(self, contract_address, product_id, product_details):
        """
        Set product details in the Product Passport contract.

        Args:
            contract_address (str): Address of the Product Passport contract.
            product_id (int): ID of the product.
            product_details (dict): Details of the product.

        Returns:
            dict: Transaction receipt.
        """
        contract = self.web3.eth.contract(address=contract_address, abi=self.product_passport_contract['abi'])
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
        """
        Get product details from the Product Passport contract.

        Args:
            contract_address (str): Address of the Product Passport contract.
            product_id (int): ID of the product.

        Returns:
            dict: Product details.
        """
        contract = self.web3.eth.contract(address=contract_address, abi=self.product_passport_contract['abi'])
        product = contract.functions.getProduct(product_id).call()
        return product

    def set_product_data(self, contract_address, product_id, product_data):
        """
        Set product data in the Product Passport contract.

        Args:
            contract_address (str): Address of the Product Passport contract.
            product_id (int): ID of the product.
            product_data (dict): Data of the product.

        Returns:
            dict: Transaction receipt.
        """
        contract = self.web3.eth.contract(address=contract_address, abi=self.product_passport_contract['abi'])
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
        """
        Get product data from the Product Passport contract.

        Args:
            contract_address (str): Address of the Product Passport contract.
            product_id (int): ID of the product.

        Returns:
            dict: Product data.
        """
        contract = self.web3.eth.contract(address=contract_address, abi=self.product_passport_contract['abi'])
        product_data = contract.functions.getProductData(product_id).call()
        return product_data

    def transfer_ownership(self, contract_address, new_owner):
        """
        Transfer ownership of the Product Passport contract.

        Args:
            contract_address (str): Address of the Product Passport contract.
            new_owner (str): Address of the new owner.

        Returns:
            dict: Transaction receipt.
        """
        contract = self.web3.eth.contract(address=contract_address, abi=self.product_passport_contract['abi'])
        tx_hash = contract.functions.transferOwnership(new_owner).transact({'from': self.account.address})
        tx_receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
        return tx_receipt
