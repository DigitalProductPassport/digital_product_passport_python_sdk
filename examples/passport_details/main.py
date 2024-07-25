import os
from nicegui import ui
from web3 import Web3
from solidity_python_sdk.main import DigitalProductPassportSDK
import logging

# Initialize the SDK and ProductPassport class
passport = DigitalProductPassportSDK()
ui.page_title('Demo')
# Custom CSS for styling
ui.add_head_html('''
    <style type="text/tailwindcss">
        @layer components {
            .blue-box {
                @apply bg-blue-300 p-4 text-center shadow-lg rounded-lg text-white;
                min-width: 200px;
                max-width: 400px;
            }
            .leaflet-map {
                width: 70%;
                height: 400px;
            }
        }
    </style>
''')

# UI components
with ui.row().classes('w-full'):
    ui.image("https://www.web3digitalproductpassport.com/img/logo.png").classes('w-[50px]')
    ui.label('Demo - Digital Product Passport').style('color: #6E93D6; font-size: 200%; font-weight: 300')
with ui.row().classes('w-full'):
    with ui.tabs().classes('w-full') as product_tabs:
        product_tab = ui.tab('Product Information').style('color: #6E93D6; font-size: 200%; font-weight: 300')
        batch_tab = ui.tab('Batch').style('color: #6E93D6; font-size: 200%; font-weight: 300')
    with ui.tab_panels(product_tabs, value=product_tab).classes('w-full'):
        with ui.tab_panel(product_tab):
            product_contract_address_input = ui.input('Product Contract Address', placeholder='0x8aB5ee83E093487a613fB58677c478758a29dab4').classes('input-field')
            ui.button('Get Product Details', on_click=lambda: get_product_details(product_contract_address_input.value, 1)).classes('button')
            product_details_output = ui.label(None)
    with ui.tab_panels(product_tabs, value=batch_tab).classes('w-full'):
        with ui.tab_panel(batch_tab):
            batch_contract_address_input = ui.input('Batch Contract Address', placeholder='0x7874c7A4be5F8605446Bc91B18B0661f67cB6A14').classes('input-field')
            batch_id_input = ui.input('Batch ID (Numeric)', placeholder='Enter numeric batch ID, use 1').classes('input-field')
            ui.button('Get Batch Details', on_click=lambda: get_batch_details(batch_contract_address_input.value, batch_id_input.value)).classes('button')
            batch_details_output = ui.label(None)
            leaflet_map = ui.leaflet(center=(0, 0), zoom=2).classes('leaflet-map')

def get_product_details(product_contract_address, product_id):
    try:
        if not Web3.is_address(product_contract_address):
            product_details_output.set_text("Error: Invalid product contract address.").classes('w-full')
            return

        try:
            product_id_int = int(product_id)
        except ValueError:
            product_details_output.set_text("Error: Product ID must be a numeric value.").classes('w-full')
            return

        product_data_retrieved = passport.product_passport.get_product(product_contract_address, product_id_int)
        product_specs = passport.product_passport.get_product_data(product_contract_address, product_id_int)

        print("Product Data Retrieved:", product_data_retrieved)
        print("Product Specifications Retrieved:", product_specs)

        uid, gtin, taric_code, manufacturer_info, consumer_info, end_of_life_info = product_data_retrieved[:6]

        with ui.card().classes('w-full'):
            with ui.grid(columns=2):
                ui.label(f"UID: {uid}").classes('blue-box')
                ui.label(f"GTIN: {gtin}").classes('blue-box')
                ui.label(f"Taric Code: {taric_code}").classes('blue-box')
                ui.label(f"Manufacturer Info: {manufacturer_info}").classes('blue-box')
                ui.label(f"Consumer info: {consumer_info}").classes('blue-box')
                ui.label(f"End of life: {end_of_life_info}").classes('blue-box')
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

        batch_details = passport.batch.get_batch(batch_contract_address, batch_id_int)

        print("Batch Data Retrieved:", batch_details)

        if len(batch_details) > 0:
            quantity, assembling_time, transport_details = batch_details[:3]
            with ui.card().classes('w-full'):
                with ui.grid(columns=2):
                    ui.label(f"Quantity: {quantity}").classes('blue-box')
                    ui.label(f"Assembling Time: {assembling_time}").classes('blue-box')
                    ui.label(f"Transport Details: {transport_details}").classes('blue-box')

        batch_geolocations = passport.geolocation.get_geolocation(batch_contract_address, batch_id)
        plot_geolocations(batch_geolocations)

    except ValueError as e:
        batch_details_output.set_text(f"Input Error: {str(e)}")
    except Exception as e:
        batch_details_output.set_text(f"Error: {str(e)}")
        logging.error(f"Failed to retrieve batch details: {e}")

def plot_geolocations(geolocations):
    leaflet_map.clear_layers()
    rows = []
    if not geolocations:
        leaflet_map.marker([0, 0], "No geolocations available.")
        return
    if len(geolocations) > 3:
        for loc in geolocations:
            try:
                latitude, longitude, additional_info = loc
                leaflet_map.marker(latlng=(latitude, longitude))
                rows.append(
                    {
                        'latitude': latitude, 
                        'longitude': longitude, 
                        'additional_info': additional_info
                    }
                )
            except (TypeError, ValueError) as e:
                logging.error(f"Failed to plot geolocation: {e}")
    if geolocations:
        first_location = geolocations
        latitude, longitude, additional_info = first_location
        leaflet_map.set_center(center=(latitude, longitude))
        leaflet_map.set_zoom(5)
        rows.append(
                    {
                        'latitude': latitude, 
                        'longitude': longitude, 
                        'additional_info': additional_info
                    }
                )
    columns = [
            {'name': 'latitude', 'label': 'Latitude', 'field': 'latitude', 'required': True, 'align': 'left'},
            {'name': 'longitude', 'label': 'Longitude', 'field': 'longitude', 'required': True, 'align': 'left'},
            {'name': 'additional_info', 'label': 'Additional Info', 'field': 'additional_info', 'required': False, 'align': 'left'}
        ]

    ui.table(columns=columns, rows=rows, row_key='latitude').classes('w-full')    

def get_pinata_url(ipfs_hash):
    pinata_gateway_token = os.getenv('PINATA_GATEWAY_TOKEN')
    pinata_gateway_url = os.getenv('PINATA_GATEWAY_URL')
    return f"https://{pinata_gateway_url}/ipfs/{ipfs_hash}?pinataGatewayToken={pinata_gateway_token}"

def plot_product_specifications(specs):
    description, manuals, specifications, batch_number, production_date, expiry_date, certifications, warranty_info, material_composition, compliance_info = specs
    with ui.card():
        with ui.grid(columns=2):
            ui.label(f"Description: {description}").classes('blue-box')
            ui.label(f"Batch: {batch_number}").classes('blue-box')
            ui.label(f"Production date: {production_date}").classes('blue-box')
            ui.label(f"Expiry date: {expiry_date}").classes('blue-box')
        with ui.grid(columns=2):
            ui.label(f"Certifications: {certifications}").classes('blue-box')
            ui.label(f"Warranty: {warranty_info}").classes('blue-box')
            ui.label(f"Material Composition: {material_composition}").classes('blue-box')
            ui.label(f"Compliance: {compliance_info}").classes('blue-box')
    with ui.tabs().classes('w-full') as tabs:
        tab_manuals = ui.tab('Manuals')
        tab_specifications = ui.tab('Specifications')

    with ui.tab_panels(tabs, value=tab_manuals).classes('w-full'):
        with ui.tab_panel(tab_manuals):
            for each in manuals:
                ipfs = get_pinata_url(each)
                ui.html(f'<embed src="{ipfs}" type="application/pdf" height="100%" width="100%">').classes('w-full')  
        with ui.tab_panel(tab_specifications):
            for each in specifications:
                ipfs = get_pinata_url(each)
                ui.html(f'<embed src="{ipfs}" type="application/pdf" height="100%" width="100%">').classes('w-full')  

ui.run()
