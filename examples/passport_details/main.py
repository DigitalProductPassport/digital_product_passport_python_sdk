from nicegui import ui
from web3 import Web3
from solidity_python_sdk.main import DigitalProductPassportSDK, ProductPassport

"""
In this demo example, we are using NiceGUI to deploy a quick page and 
show the Digital Product Passport contracts in action.
NiceGUI has very easy-to-follow documentation that can be found here:
https://nicegui.io
"""

# Initialize the SDK
sdk = DigitalProductPassportSDK()
passport = ProductPassport(sdk)

# Define UI components
ui.label('Digital Product Passport Demo')
contract_address_input = ui.input('Contract Address', placeholder='Enter contract address')
product_id_input = ui.input('Product ID (Numeric)', placeholder='Enter numeric product ID')
ui.button('Get Product Details', on_click=lambda: get_product_details(contract_address_input.value, product_id_input.value))

# Display product details and map
product_details_output = ui.label('Product Details will be displayed here')
leaflet_map = ui.leaflet(center=(0, 0), zoom=2)

# Function to get product details
def get_product_details(contract_address, product_id):
    try:
        # Ensure the contract address is valid
        if not Web3.is_address(contract_address):
            product_details_output.set_text("Error: Invalid contract address.")
            return

        # Convert product_id to integer
        try:
            product_id_int = int(product_id)
        except ValueError:
            product_details_output.set_text("Error: Product ID must be a numeric value.")
            return

        # Retrieve product details
        product_data_retrieved = passport.get_product(contract_address, product_id_int)

        # Display product details
        details = (
            f"UID: {product_data_retrieved[0]}\n"
            f"GTIN: {product_data_retrieved[1]}\n"
            f"Taric Code: {product_data_retrieved[2]}\n"
            f"Manufacturer Info: {product_data_retrieved[3]}\n"
            f"Consumer Info: {product_data_retrieved[4]}\n"
            f"End of Life Info: {product_data_retrieved[5]}"
        )
        product_details_output.set_text(details)
        
        # Fetch batch geolocations and plot them
        batch_geolocations = product_data_retrieved.get('geolocations', [])
        plot_geolocations(batch_geolocations)
        
    except Exception as e:
        product_details_output.set_text(f"Error: {str(e)}")

# Function to plot geolocations on the map
def plot_geolocations(geolocations):
    leaflet_map.clear_layers()
    if not geolocations:
        leaflet_map.marker([0, 0], "No geolocations available.")
        return

    for loc in geolocations:
        leaflet_map.marker([loc['latitude'], loc['longitude']], tooltip=loc.get('description', 'No description'))
    
    if geolocations:
        first_location = geolocations[0]
        leaflet_map.set_center([first_location['latitude'], first_location['longitude']])
        leaflet_map.set_zoom(5)


ui.run()
