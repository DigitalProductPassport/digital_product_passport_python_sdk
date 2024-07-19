import logging
from solidity_python_sdk import utils

class Batch:
    """
    Interface for interacting with the Batch smart contract.

    Attributes:
        sdk (DigitalProductPassportSDK): The SDK instance for interacting with the blockchain.
        web3 (Web3): Web3 instance for blockchain interactions.
        account (Account): Ethereum account used for transactions.
        contract (dict): ABI and bytecode of the Batch contract.
        gas (int): Gas limit for transactions.
        gwei_bid (int): Gas price in gwei.
        logger (Logger): Logger instance for logging information and debug messages.
    """

    def __init__(self, sdk):
        """
        Initializes the Batch class with the provided SDK instance.

        Args:
            sdk (DigitalProductPassportSDK): The SDK instance for blockchain interactions.
        """
        self.sdk = sdk
        self.web3 = sdk.web3
        self.account = sdk.account
        self.contract = sdk.contracts['Batch']
        self.gas = sdk.gas
        self.gwei_bid = sdk.gwei_bid
        self.logger = logging.getLogger(__name__)

    def deploy(self, product_passport_address):
        """
        Deploys the Batch smart contract to the blockchain.

        Args:
            product_passport_address (str): The address of the ProductPassport contract to be used in the Batch contract.

        Returns:
            str: The address of the deployed Batch contract.
        """
        self.logger.info(f"Deploying Batch contract from {self.account.address}")
        Contract = self.web3.eth.contract(abi=self.contract["abi"], bytecode=self.contract["bytecode"])
        
        tx = Contract.constructor(product_passport_address).build_transaction({
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

        self.logger.info(f"Batch contract deployed at address: {contract_address}")
        return contract_address

    def create_batch(self, contract_address, batch_details):
        """
        Creates a new batch in the Batch contract.

        Args:
            contract_address (str): The address of the deployed Batch contract.
            batch_details (dict): A dictionary containing the batch details with keys such as:
                "batchId", "batchNumber", "productionDate", "expiryDate", "quantity".

        Returns:
            dict: The transaction receipt containing details of the transaction.
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
            contract_address (str): The address of the deployed Batch contract.
            batch_id (str): The unique identifier for the batch.

        Returns:
            dict: The batch details retrieved from the contract.
        """
        contract = self.web3.eth.contract(address=contract_address, abi=self.contract['abi'])
        return contract.functions.getBatch(batch_id)().call()
