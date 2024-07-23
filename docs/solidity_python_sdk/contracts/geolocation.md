# Geolocation Module Documentation

## Overview

The `Geolocation` class provides an interface for interacting with the `Geolocation` smart contract. This class allows for adding geolocation information for specific batches and retrieving such information from the blockchain.

## Class: `Geolocation`

### Attributes

- **`web3`** (`Web3`): The Web3 instance used for blockchain interactions.
- **`account`** (`Account`): The Ethereum account used for transactions.
- **`contract`** (`dict`): ABI and bytecode of the `Geolocation` contract.
- **`logger`** (`Logger`): Logger instance for logging information and debug messages.

### Methods

#### `__init__(self, sdk)`

Initializes the `Geolocation` class with the provided SDK instance.

- **Args**:
  - `sdk` (`DigitalProductPassportSDK`): The SDK instance used for blockchain interactions.

#### `add_geolocation(self, contract_address, batch_id, latitude, longitude)`

Adds geolocation information for a specific batch in the `Geolocation` contract.

- **Args**:
  - `contract_address` (`str`): The address of the deployed `Geolocation` contract.
  - `batch_id` (`str`): The unique identifier for the batch.
  - `latitude` (`float`): The latitude of the geolocation.
  - `longitude` (`float`): The longitude of the geolocation.

- **Returns**:
  - `dict`: The transaction receipt containing details of the transaction.

#### `get_geolocation(self, contract_address, batch_id)`

Retrieves the geolocation information for a specific batch from the `Geolocation` contract.

- **Args**:
  - `contract_address` (`str`): The address of the deployed `Geolocation` contract.
  - `batch_id` (`str`): The unique identifier for the batch.

- **Returns**:
  - `tuple`: A tuple containing the latitude and longitude of the geolocation.

## Dependencies

This module depends on:

- `web3`: For Ethereum blockchain interactions.
- `logging`: For logging information and debug messages.
- `solidity_python_sdk`: For contract utilities.

## Example Usage

Here’s a brief example of how to use the `Geolocation` class:

```python
from solidity_python_sdk import DigitalProductPassportSDK
from solidity_python_sdk.geolocation import Geolocation

# Initialize SDK
sdk = DigitalProductPassportSDK(provider_url="https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID",
                                private_key="YOUR_PRIVATE_KEY")

# Create Geolocation instance
geolocation = Geolocation(sdk)

# Add geolocation to a batch
contract_address = "0xYourGeolocationContractAddress"
batch_id = "batch123"
latitude = 37.7749
longitude = -122.4194
tx_receipt = geolocation.add_geolocation(contract_address, batch_id, latitude, longitude)

# Get geolocation of a batch
geolocation_info = geolocation.get_geolocation(contract_address, batch_id)
print(geolocation_info)
```