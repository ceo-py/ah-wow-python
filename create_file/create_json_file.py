
import json
import os

def create_json_file(file_name: str, data: list):
    if not file_name.endswith('.json'):
        file_name += '.json'

    current_dir = os.getcwd()

    file_path = os.path.join(current_dir, 'data', 'realms', file_name)
    

    with open(file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)

