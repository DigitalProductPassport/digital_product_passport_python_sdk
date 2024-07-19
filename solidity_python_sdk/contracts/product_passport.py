import logging
from solidity_python_sdk import utils

class ProductPassport:
    def __init__(self, sdk):
        self.sdk = sdk
        self.web3 = sdk.web3
        self.account = sdk.account
        self.gas = sdk.gas
        self.gwei_bid = sdk.gwei_bid

        logging.debug(f"Available contracts: {list(sdk.contracts.keys())}")

        if 'ProductPassport' not in sdk.contracts:
            raise ValueError("Contract 'ProductPassport' not found in SDK")

        self.contract = sdk.contracts['ProductPassport']
        self.product_details_contract = sdk.contracts['ProductDetails']
        self.logger = logging.getLogger(__name__)

    def deploy(self, initial_owner=None):
        self.logger.info(f"Deploying ProductPassport contract from {self.account.address}")
        Contract = self.web3.eth.contract(abi=self.contract["abi"], bytecode=self.contract["bytecode"])

        tx = Contract.constructor(initial_owner or self.account.address).build_transaction({
            'from': self.account.address,
            'nonce': self.web3.eth.get_transaction_count(self.account.address),
            'gas': self.gas,
            'gasPrice': self.web3.to_wei(self.gwei_bid, 'gwei')
        })
        utils.check_funds(self.web3, self.account.address, tx['gas'] * tx['gasPrice'])

        signed_tx = self.web3.eth.account.sign_transaction(tx, self.account.key)
        tx_hash = self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        tx_receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
        contract_address = tx_receipt.contractAddress

        self.logger.info(f"ProductPassport contract deployed at address: {contract_address}")
        return contract_address

    def set_product(self, contract_address, product_id, product_details):
        """
        Sets the product details in the ProductPassport contract.
        
        Args:
            contract_address (str): The address of the deployed contract.
            product_id (str): The unique identifier for the product.
            product_details (dict): A dictionary containing product details.
        
        Returns:
            dict: The transaction receipt.
        """
        contract = self.web3.eth.contract(address=contract_address, abi=self.product_details_contract['abi'])
        tx = contract.functions.setProduct(
            product_id,
            product_details["uid"],
            product_details["gtin"],
            product_details["taricCode"],
            product_details["manufacturerInfo"],
            product_details["consumerInfo"],
            product_details["endOfLifeInfo"]
        ).build_transaction({
            'from': self.account.address,
            'nonce': self.web3.eth.get_transaction_count(self.account.address),
            'gas': self.gas,
            'gasPrice': self.web3.to_wei(self.gwei_bid, 'gwei')
        })

        utils.check_funds(self.web3, self.account.address, tx['gas'] * tx['gasPrice'])

        signed_tx = self.web3.eth.account.sign_transaction(tx, self.account.key)
        tx_hash = self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        tx_receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
        return tx_receipt

    def get_product(self, contract_address, product_id):
        """
        Retrieves the product details from the ProductPassport contract.
        
        Args:
            contract_address (str): The address of the deployed contract.
            product_id (str): The unique identifier for the product.
        
        Returns:
            dict: The product details.
        """
        contract = self.web3.eth.contract(address=contract_address, abi=self.product_details_contract['abi'])
        return contract.functions.getProduct(product_id)().call()

    def set_product_data(self, contract_address, product_id, product_data):
        """
        Sets the product data in the ProductPassport contract.
        
        Args:
            contract_address (str): The address of the deployed contract.
            product_id (int): The unique identifier for the product.
            product_data (dict): A dictionary containing product data.
        
        Returns:
            dict: The transaction receipt.
        """
        contract = self.web3.eth.contract(address=contract_address, abi=self.contract['abi'])
        tx = contract.functions.setProductData(
            int(product_id),
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
        ).build_transaction({
            'from': self.account.address,
            'nonce': self.web3.eth.get_transaction_count(self.account.address),
            'gas': self.gas,
            'gasPrice': self.web3.to_wei(self.gwei_bid, 'gwei')
        })
        utils.check_funds(self.web3, self.account.address, tx['gas'] * tx['gasPrice'])

        signed_tx = self.web3.eth.account.sign_transaction(tx, self.account.key)
        tx_hash = self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        tx_receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
        return tx_receipt

    def get_product_data(self, contract_address, product_id):
        """
        Retrieves the product data from the ProductPassport contract.
        
        Args:
            contract_address (str): The address of the deployed contract.
            product_id (int): The unique identifier for the product.
        
        Returns:
            dict: The product data.
        """
        contract = self.web3.eth.contract(address=contract_address, abi=self.contract['abi'])
        return contract.functions.getProductData(product_id)().call()
