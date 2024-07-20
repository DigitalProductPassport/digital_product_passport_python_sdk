# ProductPassport Module Documentation

## Overview

The `ProductPassport` class provides an interface for interacting with the `ProductPassport` smart contract. This class allows for the deployment of the contract, setting and retrieving product information, and authorizing entities to interact with the contract.

## Class: `ProductPassport`

### Attributes

- **`sdk`** (`DigitalProductPassportSDK`): The SDK instance used for blockchain interactions.
- **`web3`** (`Web3`): The Web3 instance for interacting with the Ethereum blockchain.
- **`account`** (`Account`): The Ethereum account used for transactions.
- **`gwei_bid`** (`int`): Gas price in gwei.
- **`contract`** (`dict`): ABI and bytecode of the `ProductPassport` contract.
- **`product_details_contract`** (`dict`): ABI of the `ProductDetails` contract.
- **`logger`** (`Logger`): Logger instance for logging information and debug messages.

### Methods

#### `__init__(self, sdk)`

Initializes the `ProductPassport` class with the provided SDK instance.

- **Args**:
  - `sdk` (`DigitalProductPassportSDK`): The SDK instance for blockchain interactions.

- **Raises**:
  - `ValueError`: If the 'ProductPassport' contract is not found in the SDK contracts.

#### `deploy(self, initial_owner=None)`

Deploys the `ProductPassport` contract to the blockchain.

- **Args**:
  - `initial_owner` (`str`, optional): The address of the initial owner of the contract. Defaults to the deployer's address.

- **Returns**:
  - `str`: The address of the deployed contract.

- **Raises**:
  - `ValueError`: If the deployment fails.

#### `set_product(self, contract_address, product_id, product_details)`

Sets the product details in the `ProductPassport` contract.

- **Args**:
  - `contract_address` (`str`): The address of the deployed `ProductPassport` contract.
  - `product_id` (`str`): The unique identifier for the product.
  - `product_details` (`dict`): A dictionary containing the product details with keys such as:
    - `"uid"`
    - `"gtin"`
    - `"taricCode"`
    - `"manufacturerInfo"`
    - `"consumerInfo"`
    - `"endOfLifeInfo"`

- **Returns**:
  - `dict`: The transaction receipt containing details of the transaction.

- **Raises**:
  - `ValueError`: If the transaction fails.

#### `get_product(self, contract_address, product_id)`

Retrieves the product details from the `ProductPassport` contract.

- **Args**:
  - `contract_address` (`str`): The address of the deployed `ProductPassport` contract.
  - `product_id` (`str`): The unique identifier for the product.

- **Returns**:
  - `dict`: The product details retrieved from the contract.

- **Raises**:
  - `ValueError`: If the product cannot be retrieved.

#### `set_product_data(self, contract_address, product_id, product_data)`

Sets the product data in the `ProductPassport` contract.

- **Args**:
  - `contract_address` (`str`): The address of the deployed `ProductPassport` contract.
  - `product_id` (`int`): The unique identifier for the product.
  - `product_data` (`dict`): A dictionary containing product data with keys such as:
    - `"description"`
    - `"manuals"`
    - `"specifications"`
    - `"batchNumber"`
    - `"productionDate"`
    - `"expiryDate"`
    - `"certifications"`
    - `"warrantyInfo"`
    - `"materialComposition"`
    - `"complianceInfo"`

- **Returns**:
  - `dict`: The transaction receipt containing details of the transaction.

- **Raises**:
  - `ValueError`: If the transaction fails.

#### `get_product_data(self, contract_address, product_id)`

Retrieves the product data from the `ProductPassport` contract.

- **Args**:
  - `contract_address` (`str`): The address of the deployed `ProductPassport` contract.
  - `product_id` (`int`): The unique identifier for the product.

- **Returns**:
  - `dict`: The product data retrieved from the contract.

- **Raises**:
  - `ValueError`: If the product data cannot be retrieved.

#### `authorize_entity(self, contract_address, entity_address)`

Authorizes an entity to interact with the `ProductPassport` contract.

- **Args**:
  - `contract_address` (`str`): The address of the `ProductPassport` contract.
  - `entity_address` (`str`): The address of the entity to authorize.

- **Returns**:
  - `dict`: The transaction receipt containing details of the transaction.

- **Raises**:
  - `ValueError`: If the transaction fails.

## Dependencies

This module depends on:

- `solidity_python_sdk`: For contract utilities.
- `web3`: For Ethereum blockchain interactions.
- `logging`: For logging information and debug messages.

## Example Usage

Here’s a brief example of how to use the `ProductPassport` class:

```python
from solidity_python_sdk import DigitalProductPassportSDK
from solidity_python_sdk.product_passport import ProductPassport

# Initialize SDK
sdk = DigitalProductPassportSDK(provider_url="https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID",
                                private_key="YOUR_PRIVATE_KEY")

# Create ProductPassport instance
product_passport = ProductPassport(sdk)

# Deploy ProductPassport contract
contract_address = product_passport.deploy()

# Set product details
product_details = {
    "uid": "1234567890",
    "gtin": "0123456789012",
    "taricCode": "1234",
    "manufacturerInfo": "Example Manufacturer",
    "consumerInfo": "Consumer Information",
    "endOfLifeInfo": "End of Life Information"
}
tx_receipt = product_passport.set_product(contract_address, "product_id_1", product_details)

# Get product details
product = product_passport.get_product(contract_address, "product_id_1")
print(product)
```
