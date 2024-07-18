# Solidity Python SDK

## Overview

The **Solidity Python SDK** is a Python library designed for interacting with Digital Product Passport smart contracts. It provides an easy-to-use interface for deploying and interacting with smart contracts on the Ethereum blockchain.

## Features

- **Load Contracts**: Load and interact with pre-deployed smart contracts.
- **Deploy Contracts**: Deploy new smart contracts to the Ethereum blockchain.
- **Set and Get Product Details**: Set and retrieve detailed product information from smart contracts.
- **Support for IPFS**: Integrate with IPFS for storing and retrieving product-related documents.

## Installation

To install the SDK, you can use pip:



```bash
pip install -i https://test.pypi.org/simple/ solidity-python-sdk==0.1.1
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
account_address = "0xYourEthereumAddress"
contract_address = sdk.product_passport.deploy(account_address)
print(f"Contract deployed at address: {contract_address}")
```

### Set Product Details

```python
product_details = {
    "productId": 1,
    "description": "Brigadeiro Product Passport",
    "manuals": ["QmbnzbFDcmtJhyw5XTLkcnkJMhW86YZg6oc3FsNBeN2r4W"],
    "specifications": ["QmbnzbFDcmtJhyw5XTLkcnkJMhW86YZg6oc3FsNBeN2r4W"],
    "batchNumber": "BRG-2023-001",
    "productionDate": "2023-06-20",
    "expiryDate": "2023-12-31",
    "certifications": "FDA-5678",
    "warrantyInfo": "Not applicable",
    "materialComposition": "Condensed milk, cocoa powder, butter, chocolate sprinkles",
    "complianceInfo": "Compliant with local food safety regulations",
    "ipfs": "QmWDYhFAaT89spcqbKYboyCm6mkYSxKJaWUuS18Akmw96t"
}

tx_receipt = sdk.product_passport.set_product_data(contract_address, 1, product_details)
print(f"Transaction receipt: {tx_receipt}")

```

### Get  Product Details

```python
product_data_retrieved = sdk.product_passport.get_product_data(contract_address, 1)
print(f"Retrieved product data: {product_data_retrieved}")


```

## Documentation
The documentation for the SDK is available in the docs directory. You can view the documentation in Markdown format or convert it to other formats if needed.

## Contributing
We welcome contributions to improve the SDK! Please follow these steps to contribute:

## Fork the repository.
Create a new branch for your changes.
Make your changes and write tests.
Submit a pull request with a clear description of your changes.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Contact
For any questions or support, please contact:

Author: Luthiano Trarbach
Email: luthiano.trarbach@proton.me