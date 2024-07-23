import json
from pinatapy import PinataPy
import os

class PinataUtility:
    def __init__(self, api_key, secret_api_key):
        self.pinata = PinataPy(api_key, secret_api_key)

    def pin_file(self, file_path):
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"The file {file_path} does not exist.")
        with open(file_path, 'rb') as file:
            response = self.pinata.pin_file_to_ipfs(file)
        return response

    def pin_json(self, json_data):
        response = self.pinata.pin_json_to_ipfs(json_data)
        return response

    def pin_files_from_config(self, config_path):
        with open(config_path, 'r') as config_file:
            config_data = json.load(config_file)

        pinned_data = {}

        for key, value in config_data.items():
            if isinstance(value, list):
                pinned_data[key] = []
                for doc_path in value:
                    try:
                        response = self.pin_file(doc_path)
                        pinned_data[key].append(response["IpfsHash"])
                    except Exception as e:
                        print(f"Failed to pin {doc_path}: {e}")
            elif isinstance(value, str) and os.path.isfile(value):
                try:
                    response = self.pin_file(value)
                    pinned_data[key] = response["IpfsHash"]
                except Exception as e:
                    print(f"Failed to pin {value}: {e}")
            else:
                pinned_data[key] = value

        return pinned_data

