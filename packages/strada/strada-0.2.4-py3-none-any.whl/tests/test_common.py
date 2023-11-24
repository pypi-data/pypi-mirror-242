import unittest
import json
from unittest.mock import patch
from strada.common import (
    fill_path_params,
    hydrate_input_fields,
    build_input_schema_from_strada_param_definitions,
    validate_http_input,
)
from strada.exception import StradaValidationException


class TestCommon(unittest.TestCase):
    def test_fill_path_params(self):
        url = "http://example.com/resource/{id}"
        params = {"id": "123"}
        expected_url = "http://example.com/resource/123"
        self.assertEqual(fill_path_params(url, params), expected_url)

    def test_hydrate_input_fields(self):
        input_schema = {
            "type": "object",
            "properties": {"name": {"type": "string"}, "age": {"type": "number"}},
        }
        form_data_json_str = '{"name": "John", "age": "{{age}}"}'
        hydrated_data = hydrate_input_fields(input_schema, form_data_json_str, age=30)
        expected_data = {"name": "John", "age": "30"}
        self.assertEqual(hydrated_data, expected_data)

    def test_build_input_schema(self):
        param_definitions_str = json.dumps(
            [
                {"paramName": "name", "paramType": "string", "defaultValue": "Doe"},
                {"paramName": "age", "paramType": "number", "defaultValue": 30},
            ]
        )
        schema = build_input_schema_from_strada_param_definitions(param_definitions_str)
        expected_schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string", "default": "Doe"},
                "age": {"type": "number", "default": 30},
            },
            "required": ["name", "age"],
        }
        self.assertEqual(schema, expected_schema)

    def test_validate_http_input(self):
        schema = {
            "type": "object",
            "properties": {"name": {"type": "string"}, "age": {"type": "number"}},
            "required": ["name"],
        }
        valid_input = {"name": "John", "age": 30}
        invalid_input = {"age": "thirty"}
        invalid_number_input = {"name": "John", "age": "thirty"}

        # Test valid input
        result, message = validate_http_input(schema, **valid_input)
        self.assertTrue(result)

        # Test invalid input
        with self.assertRaises(StradaValidationException) as context:
            validate_http_input(schema, **invalid_input)
        exception = context.exception
        self.assertEqual(exception.schema, schema)
        self.assertEqual(exception.data, invalid_input)
        self.assertIn("required property", str(exception))

        # Test invalid number input
        with self.assertRaises(StradaValidationException) as context:
            validate_http_input(schema, **invalid_number_input)
        exception = context.exception
        self.assertEqual(exception.schema, schema)
        self.assertEqual(exception.data, invalid_number_input)
        self.assertIn("is not of type 'number'", str(exception))


if __name__ == "__main__":
    unittest.main()
