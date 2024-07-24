from nicegui import ui
from web3 import Web3
from solidity_python_sdk.main import DigitalProductPassportSDK
import logging

# Initialize the SDK and ProductPassport class
passport = DigitalProductPassportSDK()

# UI components
ui.label('Ethos - Digital Product Passport').style('font-weight: bold; font-size: 30px;')

with ui.row():
    with ui.column().style('margin: 50px;'):
        product_contract_address_input = ui.input('Product Contract Address', placeholder='0x014e6Be5cE6CE4cba1F9be826a6Da3A0af04447D')
        product_id_input = ui.input('Product ID (Numeric)', placeholder='Enter numeric product ID, use 1')
        ui.button('Get Product Details', on_click=lambda: get_product_details(product_contract_address_input.value, product_id_input.value))

    with ui.column().style('margin: 50px;'):
        batch_contract_address_input = ui.input('Batch Contract Address', placeholder='0x014e6Be5cE6CE4cba1F9be826a6Da3A0af04447D')
        batch_id_input = ui.input('Batch ID (Numeric)', placeholder='Enter numeric batch ID, use 1')
        ui.button('Get Batch Details', on_click=lambda: get_batch_details(batch_contract_address_input.value, batch_id_input.value))

# Product Details Section
with ui.column().style('padding: 50px;'):
    ui.label('Product Details').style('font-weight: bold; font-size: 20px;')
    product_details_output = ui.label('Product Details will be displayed here')
    manuals_output = ui.label('Manuals will be displayed here')
    specifications_output = ui.label('Specifications will be displayed here')

# Batch Details Section
with ui.column().style('padding: 50px;'):
    ui.label('Batch Details').style('font-weight: bold; font-size: 20px;')
    batch_details_output = ui.label('Batch Details will be displayed here')
    leaflet_map = ui.leaflet(center=(0, 0), zoom=2)

def get_product_details(product_contract_address, product_id):
    try:
        if not Web3.is_address(product_contract_address):
            product_details_output.set_text("Error: Invalid product contract address.")
            return

        try:
            product_id_int = int(product_id)
        except ValueError:
            product_details_output.set_text("Error: Product ID must be a numeric value.")
            return

        # Fetch product details using ProductPassport class
        product_data_retrieved = passport.product_passport.get_product(product_contract_address, product_id_int)
        product_specs = passport.product_passport.get_product_data(product_contract_address, product_id)

        # Debugging log to check structure of retrieved data
        print("Product Data Retrieved:", product_data_retrieved)
        print("Product Specifications Retrieved:", product_specs)
        
        # Unpacking product details
        uid, gtin, taric_code, manufacturer_info, consumer_info, end_of_life_info = product_data_retrieved[:6]


        details = (
            f"UID: {uid}\n"
            f"GTIN: {gtin}\n"
            f"Taric Code: {taric_code}\n"
            f"Manufacturer Info: {manufacturer_info}\n"
            f"Consumer Info: {consumer_info}\n"
            f"End of Life Info: {end_of_life_info}"
        )
        product_details_output.set_text(details)

        # Plot product specifications data if any (example plot)
        plot_product_specifications(product_specs)

    except ValueError as e:
        product_details_output.set_text(f"Input Error: {str(e)}")
    except Exception as e:
        product_details_output.set_text(f"Error: {str(e)}")
        logging.error(f"Failed to retrieve product details: {e}")

def get_batch_details(batch_contract_address, batch_id):
    try:
        if not Web3.is_address(batch_contract_address):
            batch_details_output.set_text("Error: Invalid batch contract address.")
            return

        try:
            batch_id_int = int(batch_id)
        except ValueError:
            batch_details_output.set_text("Error: Batch ID must be a numeric value.")
            return

        # Fetch batch details using the passport SDK
        batch_details = passport.batch.get_batch(batch_contract_address, batch_id_int)
        
        # Debugging log to check structure of retrieved data
        print("Batch Data Retrieved:", batch_details)
        
        # Display batch details safely
        batch_info = {
            'Batch Number': batch_details[0] if len(batch_details) > 0 else 'N/A',
            'Production Date': batch_details[1] if len(batch_details) > 1 else 'N/A',
            'Expiry Date': batch_details[2] if len(batch_details) > 2 else 'N/A',
            'Quantity': batch_details[3] if len(batch_details) > 3 else 'N/A'
        }
        
        batch_details_output.set_text(
            '\n'.join(f"{key}: {value}" for key, value in batch_info.items())
        )

        # Fetch and plot geolocations
        batch_geolocations = passport.geolocation.get_geolocation(batch_contract_address, batch_id)
        plot_geolocations(batch_geolocations)

    except ValueError as e:
        batch_details_output.set_text(f"Input Error: {str(e)}")
    except Exception as e:
        batch_details_output.set_text(f"Error: {str(e)}")
        logging.error(f"Failed to retrieve batch details: {e}")

def plot_geolocations(geolocations):
    leaflet_map.clear_layers()
    if not geolocations:
        leaflet_map.marker([0, 0], "No geolocations available.")
        return

    for loc in geolocations:
        leaflet_map.marker([float(loc['latitude']), float(loc['longitude'])], tooltip=loc.get('additionalInfo', 'No description'))

    if geolocations:
        first_location = geolocations[0]
        leaflet_map.set_center([float(first_location['latitude']), float(first_location['longitude'])])
        leaflet_map.set_zoom(5)

def plot_product_specifications(specs):
    print("Plotting product specifications:", specs)

ui.run()
