# Batch Module Documentation

## Overview

The `Batch` class provides an interface for interacting with the `Batch` smart contract. This class facilitates the deployment of the contract, creating batches, and retrieving batch details from the blockchain.

## Class: `Batch`

### Attributes

- **`sdk`** (`DigitalProductPassportSDK`): The SDK instance used for blockchain interactions.
- **`web3`** (`Web3`): The Web3 instance for interacting with the Ethereum blockchain.
- **`account`** (`Account`): The Ethereum account used for transactions.
- **`contract`** (`dict`): ABI and bytecode of the `Batch` contract.
- **`gas`** (`int`): Gas limit for transactions.
- **`gwei_bid`** (`int`): Gas price in gwei.
- **`logger`** (`Logger`): Logger instance for logging information and debug messages.

### Methods

#### `__init__(self, sdk)`

Initializes the `Batch` class with the provided SDK instance.

- **Args**:
  - `sdk` (`DigitalProductPassportSDK`): The SDK instance for blockchain interactions.

- **Raises**:
  - `KeyError`: If the 'Batch' contract is not found in the SDK contracts.

#### `deploy(self, product_passport_address)`

Deploys the `Batch` smart contract to the blockchain.

- **Args**:
  - `product_passport_address` (`str`): The address of the `ProductPassport` contract to be used in the `Batch` contract.

- **Returns**:
  - `str`: The address of the deployed `Batch` contract.

- **Raises**:
  - `ValueError`: If the transaction fails or the contract cannot be deployed.

#### `create_batch(self, contract_address, batch_details)`

Creates a new batch in the `Batch` contract.

- **Args**:
  - `contract_address` (`str`): The address of the deployed `Batch` contract.
  - `batch_details` (`dict`): A dictionary containing the batch details with keys such as:
    - `"batchId"` (`str`): The unique identifier for the batch.
    - `"batchNumber"` (`str`): The batch number.
    - `"productionDate"` (`str`): The production date of the batch.
    - `"expiryDate"` (`str`): The expiry date of the batch.
    - `"quantity"` (`int`): The quantity of items in the batch.

- **Returns**:
  - `dict`: The transaction receipt containing details of the transaction.

- **Raises**:
  - `ValueError`: If the transaction fails or the batch cannot be created.

#### `get_batch(self, contract_address, batch_id)`

Retrieves the batch details from the `Batch` contract.

- **Args**:
  - `contract_address` (`str`): The address of the deployed `Batch` contract.
  - `batch_id` (`str`): The unique identifier for the batch.

- **Returns**:
  - `dict`: The batch details retrieved from the contract.

- **Raises**:
  - `ValueError`: If the batch cannot be retrieved or if the batch ID is invalid.

## Dependencies

This module depends on:

- `solidity_python_sdk`: For contract utilities.
- `web3`: For Ethereum blockchain interactions.
- `logging`: For logging information and debug messages.

## Example Usage

Here’s a brief example of how to use the `Batch` class:

```python
from solidity_python_sdk import DigitalProductPassportSDK
from solidity_python_sdk.batch import Batch

# Initialize SDK
sdk = DigitalProductPassportSDK(provider_url="https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID",
                                private_key="YOUR_PRIVATE_KEY")

# Create Batch instance
batch = Batch(sdk)

# Deploy Batch contract
product_passport_address = "0xYourProductPassportContractAddress"
contract_address = batch.deploy(product_passport_address)

# Create a new batch
batch_details = {
    "batchId": "batch123",
    "batchNumber": "B123",
    "productionDate": "2024-07-01",
    "expiryDate": "2025-07-01",
    "quantity": 1000
}
tx_receipt = batch.create_batch(contract_address, batch_details)

# Get batch details
batch_id = "batch123"
batch_info = batch.get_batch(contract_address, batch_id)
print(batch_info)
```
