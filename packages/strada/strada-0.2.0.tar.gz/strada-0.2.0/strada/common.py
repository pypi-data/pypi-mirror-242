import json
from exception import StradaValidationException
import jsonschema
import re


def fill_path_params(url, path_params):
    for key, value in path_params.items():
        url = url.replace("{" + key + "}", value)

    return url


def hydrate_input_fields(input_schema, formDataJsonStr, **kwargs):
    loaded_form_data = json.loads(formDataJsonStr)

    def process_value(value, schema):
        if isinstance(value, dict):
            return {
                k: process_value(v, schema["properties"][k])
                for k, v in value.items()
                if k in schema["properties"]
            }
        elif isinstance(value, list):
            return [process_value(item, schema["items"]) for item in value]
        elif isinstance(value, str):
            return replace_placeholders(value, schema)
        else:
            return value

    def find_schema_for_key(key, schema):
        if "." in key:
            top_key, rest_of_key = key.split(".", 1)
            if "properties" in schema and top_key in schema["properties"]:
                return find_schema_for_key(rest_of_key, schema["properties"][top_key])
        return schema

    def replace_placeholders(value, schema):
        placeholders = re.findall(r"\{\{(.*?)\}\}", value)
        for key in placeholders:
            if key in kwargs:
                specific_schema = find_schema_for_key(key, schema)
                if "type" in specific_schema:
                    key_type = specific_schema["type"]
                    value = value.replace(
                        "{{" + key + "}}", convert_value(kwargs[key], key_type)
                    )
        return value

    def convert_value(value, keyType):
        if keyType == "number":
            return str(int(value))
        elif keyType == "boolean":
            return str(value.lower() in ["true", "1", "yes"]).lower()
        elif keyType == "array":
            # Assuming the value is a comma-separated string
            return json.dumps(value.split(","))
        elif keyType == "object":
            # Assuming the value is a JSON string
            return value
        elif keyType == "string":
            return value
        else:
            raise NotImplementedError(f"Type '{keyType}' not handled")

    return process_value(loaded_form_data, input_schema)


def build_input_schema_from_strada_param_definitions(param_definitions_json_str):
    # Create an empty JSON schema object
    json_schema = {"type": "object", "properties": {}, "required": []}

    param_definitions = json.loads(param_definitions_json_str)
    for param_definition in param_definitions:
        param_name = param_definition["paramName"]
        param_type = param_definition["paramType"]

        # Create a property definition for the parameter
        property_definition = {"type": param_type}

        # If the parameter has a defaultValue, add it to the schema
        if param_definition["defaultValue"]:
            property_definition["default"] = param_definition["defaultValue"]

        # Add the property definition to the JSON schema
        json_schema["properties"][param_name] = property_definition

        json_schema["required"].append(param_name)

    return json_schema


def validate_http_input(inputSchema, **kwargs):
    """
    Validate HTTP input data against a JSON schema.

    Args:
        inputSchema (dict): JSON schema representing the expected structure of the input data.
        **kwargs: Arbitrary keyword arguments representing the input data.

    Returns:
        bool: True if the input data adheres to the schema, False otherwise.
        str: A message indicating the validation result.

    Example usage:
        schema = {
            "type": "object",
            "properties": {
                "param1": {"type": "string"},
                "param2": {"type": "number"}
            },
            "required": ["param1"]
        }
        result, message = validate_http_input(schema, param1="Hello", param2=42)

    """
    if (kwargs is None) or (len(kwargs) == 0):
        return True, "No input data provided."

    # Convert the input schema to a JSON string
    input_schema_str = json.dumps(inputSchema)

    # Parse the JSON schema
    schema = json.loads(input_schema_str)

    # Validate the input data against the schema
    try:
        jsonschema.validate(instance=kwargs, schema=schema)
        return True, "Input data adheres to the schema."
    except jsonschema.exceptions.ValidationError as e:
        raise StradaValidationException(str(e), schema=inputSchema, data=kwargs)
