


import json
import re
from jsonschema import validate, ValidationError, Draft7Validator


def collect_validation_errors(data, schema):
    validator = Draft7Validator(schema)
    errors = sorted(validator.iter_errors(data), key=lambda e: e.path)
    return errors

def preprocess_data(data,schema):
    def cast_value(value, expected_type):
        if expected_type == "boolean":
            if isinstance(value, str) and value.lower() in ["true", "false"]:
                return value.lower() == "true"
        elif expected_type == "integer":
            if isinstance(value, str) and value.isdigit():
                return int(value)
        return value
    
    def preprocess(data, schema):
        if isinstance(data, dict):
            for key, value in data.items():
                if "properties" in schema and key in schema["properties"]:
                    data[key] = preprocess(data[key], schema["properties"][key])
                elif "type" in schema:
                    data[key] = cast_value(data[key], schema["type"])
        elif isinstance(data, list):
            for i, item in enumerate(data):
                if "items" in schema:
                    data[i] = preprocess(item, schema["items"])
        return data
    
    return preprocess(data, schema)






def validate_json():
    with open("blueprints/cv_schema.json","r") as file:
        schema = json.load(file)

    with open("data_set/expected_cv.json","r") as file:
        data = json.load(file)
    data = preprocess_data(data,schema)
    return collect_validation_errors(data,schema)


if __name__ == "__main__":
    print("\n".join(validate_json()))