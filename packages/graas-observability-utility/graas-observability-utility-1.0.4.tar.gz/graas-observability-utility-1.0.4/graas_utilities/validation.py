import json
import os
import jsonschema
from jsonschema.exceptions import ValidationError


def validate_json_data(schema_file, data_file):
    # Load the JSON schema from the schema file
    with open(schema_file, "r") as schema_file:
        schema = json.load(schema_file)

    # Load the JSON data from the data file
    with open(data_file, "r") as data_file:
        data = json.load(data_file)

    print(data)
    try:
        jsonschema.validate(data, schema)
        return True  # Data matches the schema
    except ValidationError as e:
        print("Error", e)
        return False  # Data does not match the schema


# file_path = os.path.abspath(__file__)
# base_uri = f"file:{file_path}"
# print(f"\nbase uri = '{base_uri}'\n")
# File paths for the schema and data files
schema_file_path = os.path.join(os.getcwd(), "Onsite_campaigns/Onsite_campaign.json")
data_file_path = os.path.join(
    os.getcwd(), "Data_for_testing/AABCW_Campaign_onsite_lazada.json"
)

if validate_json_data(schema_file_path, data_file_path):
    print("Data matches the schema.")
else:
    print("Data does not match the schema.")
