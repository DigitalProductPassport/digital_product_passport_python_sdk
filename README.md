# Solidity Python SDK

## Overview

The **Solidity Python SDK** is a Python library designed for interacting with Digital Product Passport smart contracts. It provides an easy-to-use interface for deploying and interacting with smart contracts on the Ethereum blockchain.

[Read about the project](https://www.web3digitalproductpassport.com/)

## Features

- **Load Contracts**: Load and interact with pre-deployed smart contracts.
- **Deploy Contracts**: Deploy new smart contracts to the Ethereum blockchain.
- **Set and Get Product Details**: Set and retrieve detailed product information from smart contracts.
- **Authorize Entities**: Authorize entities for specific roles in the smart contract.
- **Support for IPFS**: Integrate with IPFS for storing and retrieving product-related documents.

## Installation

To install the SDK, you can use pip:

```bash
pip install -i https://test.pypi.org/simple/ solidity-python-sdk
```

or 

```bash
pip install solidity-python-sdk
```

## Usage

Here's a quick start guide to help you get started with the SDK:

### Basic Usage

```python
from solidity_python_sdk.main import DigitalProductPassportSDK

sdk = DigitalProductPassportSDK()
```

### Deploy a Contract

```python
from solidity_python_sdk.main import ProductPassport

account_address = "0xYourEthereumAddress"
passport = ProductPassport(sdk)

contract_address = passport.deploy(account_address)
print(f"Contract deployed at address: {contract_address}")
```

### Authorize an Entity

```python
entity_address = "0xEntityAddress"
role = "manufacturer"

tx_receipt = passport.authorize_entity(contract_address, entity_address, role)
print(f"Entity authorized. Transaction receipt: {tx_receipt}")
```

### Set Product Details

```python
product_details = {
    "uid": "UID123",
    "gtin": "GTIN123",
    "taricCode": "TARIC123",
    "manufacturerInfo": "Manufacturer info",
    "consumerInfo": "Consumer info",
    "endOfLifeInfo": "End of life info"
}

tx_receipt = passport.set_product(contract_address, "123456", product_details)
print(f"Transaction receipt: {tx_receipt}")
```

### Get Product Details

```python
product_data_retrieved = passport.get_product(contract_address, "123456")
print(f"Retrieved product data: {product_data_retrieved}")
```

### Set Product Data

```python
product_data = {
    "description": "Product description",
    "manuals": ["QmWDYhFAaT89spcqbKYboyCm6mkYSxKJaWUuS18Akmw96t"],
    "specifications": ["QmWDYhFAaT89spcqbKYboyCm6mkYSxKJaWUuS18Akmw96t"],
    "batchNumber": "Batch123",
    "productionDate": "2024-07-19",
    "expiryDate": "2025-07-19",
    "certifications": "Certifications info",
    "warrantyInfo": "Warranty info",
    "materialComposition": "Material info",
    "complianceInfo": "Compliance info"
}

tx_receipt = passport.set_product_data(contract_address, 123456, product_data)
print(f"Transaction receipt: {tx_receipt}")
```

### Get Product Data

```python
product_data_retrieved = passport.get_product_data(contract_address, 123456)
print(f"Retrieved product data: {product_data_retrieved}")
```

## Documentation

The documentation for the SDK is available in the `docs` directory. You can view the documentation in Markdown format or convert it to other formats if needed.

## Contributing

We welcome contributions to improve the SDK! Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch for your changes.
3. Make your changes and write tests.
4. Submit a pull request with a clear description of your changes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contact

For any questions or support, please contact:

- **Author**: Luthiano Trarbach
- **Email**: luthiano.trarbach@proton.me
