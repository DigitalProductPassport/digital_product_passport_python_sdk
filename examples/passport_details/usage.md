# Digital Product Passport Demo

This project demonstrates the usage of the `DigitalProductPassportSDK` for managing digital product passports using a web interface built with `NiceGUI`. The demo allows users to input contract addresses and retrieve detailed information about products and batches.

## Prerequisites to run localy

- Python 3.7+
- Web3.py
- NiceGUI
- Solidity Python SDK
- Pinata API keys and secrets
- Pinata Gateway
- Private keys
- Provider

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/DigitalProductPassport/solidity-python-sdk.git
    ```

2. Install the required packages:

    ```bash
    pip install nicegui web3 solidity-python-sdk
    ```

3. Set up environment variables for Pinata:

    ```bash
    export PINATA_GATEWAY_TOKEN=your_pinata_gateway_token
    export PINATA_GATEWAY_URL=your_pinata_gateway_url
    export PROVIDER_URL=the_provider_rpc
    export PRIVATE_KEY=your_private_key
    ```

## Running the Demo

To start the demo application, run the following command:

```bash
python main.py
```

This will start a local web server. Open your browser and navigate to `http://localhost:8080` to view the demo.

You can also use docker-compose

```bash
docker-compose up
```

And use Elastic Beanstalk or Google Cloud run

```bash
eb init -p docker ddp-demo
eb setenv PINATA_GATEWAY_TOKEN=your_pinata_gateway_token PINATA_GATEWAY_URL=your_pinata_gateway_url \
PROVIDER_URL=the_provider_rpc  PRIVATE_KEY=your_private_key
eb deploy
```


## Features

- **Home Page**: Displays the title and logo.
- **Tabs**: Two tabs for "Product Information" and "Batch".
- **Product Information**:
  - Input for Product Contract Address
  - Button to fetch product details
  - Displays detailed product information including UID, GTIN, Taric Code, Manufacturer Info, Consumer Info, End of Life Info
  - Displays product specifications and documents
- **Batch**:
  - Input for Batch Contract Address
  - Input for Batch ID
  - Button to fetch batch details
  - Displays detailed batch information including Quantity, Assembling Time, Transport Details
  - Displays geolocations on a map


## How to use

### Product Information


## Code Overview

### `index()`

Defines the home page layout with title, logo, tabs, and input fields for contract addresses.

### `get_product_details(product_contract_address, product_id)`

Fetches and displays product details based on the provided contract address and product ID.

### `get_batch_details(batch_contract_address, batch_id)`

Fetches and displays batch details based on the provided contract address and batch ID.

### `plot_geolocations(geolocations)`

Plots geolocation data on a map using Leaflet.

### `get_pinata_url(ipfs_hash)`

Generates a URL for Pinata-hosted IPFS content.

### `plot_product_specifications(specs)`

Displays product specifications in a grid layout.

### `plot_product_documents(specs)`

Displays product documents (manuals and specifications) using embedded PDF viewers.

