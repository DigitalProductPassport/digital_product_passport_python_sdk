import logging
from solidity_python_sdk.utils import utils

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

        Raises:
            KeyError: If the 'Batch' contract is not found in the SDK contracts.
        """
        self.sdk = sdk
        self.web3 = sdk.web3
        self.account = sdk.account
        self.gas = sdk.gas
        self.gwei_bid = sdk.gwei_bid

        if 'Batch' not in sdk.contracts:
            raise KeyError("Contract 'Batch' not found in SDK")

        self.contract = sdk.contracts['Batch']
        self.logger = logging.getLogger(__name__)

    def deploy(self, product_passport_address):
        """
        Deploys the Batch smart contract to the blockchain.

        Args:
            product_passport_address (str): The address of the ProductPassport contract to be used in the Batch contract.

        Returns:
            str: The address of the deployed Batch contract.

        Raises:
            ValueError: If the transaction fails or the contract cannot be deployed.
        """
        self.logger.info(f"Deploying Batch contract from {self.account.address}")
        Contract = self.web3.eth.contract(abi=self.contract["abi"], bytecode=self.contract["bytecode"])
        
        tx = Contract.constructor(product_passport_address, self.account.address).build_transaction({
            'from': self.account.address,
            'nonce': self.web3.eth.get_transaction_count(self.account.address, 'pending'),
            'gas': Contract.constructor(product_passport_address, self.account.address).estimate_gas({'from': self.account.address}),
            'gasPrice': self.web3.to_wei(self.gwei_bid, 'gwei')
        })
        utils.check_funds(self.web3, self.account.address, tx['gas'] * tx['gasPrice'])

        signed_tx = self.web3.eth.account.sign_transaction(tx, self.account.key)
        tx_hash = self.web3.eth.send_raw_transaction(signed_tx.raw_transaction)
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
                "batchId" (int): The unique identifier for the batch.
                "amount" (int): The quantity of items in the batch.
                "assemblingTime" (int): The UNIX timestamp of the assembling time.
                "transportDetails" (str): Details about the transport.
                "ipfsHash" (str): The IPFS hash of the batch metadata.

        Returns:
            dict: The transaction receipt containing details of the transaction.

        Raises:
            ValueError: If the transaction fails or the batch cannot be created.
        """
        contract = self.web3.eth.contract(address=contract_address, abi=self.contract['abi'])

        try:
            tx = contract.functions.setBatchDetails(
                batch_details["batchId"],
                batch_details["amount"],
                batch_details["assemblingTime"],
                batch_details["transportDetails"],
                batch_details["ipfsHash"]
            ).build_transaction({
                'from': self.account.address,
                'nonce': self.web3.eth.get_transaction_count(self.account.address, 'pending'),
                'gas': contract.functions.setBatchDetails(
                    batch_details["batchId"],
                    batch_details["amount"],
                    batch_details["assemblingTime"],
                    batch_details["transportDetails"],
                    batch_details["ipfsHash"]
                ).estimate_gas({'from': self.account.address}),
                'gasPrice': self.web3.to_wei(self.gwei_bid, 'gwei')
            })
            
            signed_tx = self.web3.eth.account.sign_transaction(tx, self.account.key)
            tx_hash = self.web3.eth.send_raw_transaction(signed_tx.raw_transaction)
            tx_receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash, timeout=300)

            self.logger.info(f"Batch created transaction receipt: {tx_receipt}")
            return tx_receipt
        except Exception as e:
            self.logger.error(f"Failed to create batch: {e}")
            raise

    def get_batch(self, contract_address, batch_id):
        """
        Retrieves the batch details from the Batch contract.

        Args:
            contract_address (str): The address of the deployed Batch contract.
            batch_id (int): The unique identifier for the batch.

        Returns:
            dict: The batch details retrieved from the contract.

        Raises:
            ValueError: If the batch cannot be retrieved or if the batch ID is invalid.
        """
        contract = self.web3.eth.contract(address=contract_address, abi=self.contract['abi'])
        try:
            batch = contract.functions.getBatchDetails(batch_id).call()
            self.logger.info(f"Batch retrieved: {batch}")
            return batch
        except Exception as e:
            self.logger.error(f"Failed to retrieve batch: {e}")
            raise
