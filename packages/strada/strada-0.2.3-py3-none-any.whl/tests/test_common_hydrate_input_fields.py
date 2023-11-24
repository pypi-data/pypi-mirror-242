import unittest
import json
from unittest.mock import patch
from strada.common import hydrate_input_fields


class TestHydrateInputFields(unittest.TestCase):
    def test_hydrate_simple_values(self):
        input_schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "number"},
                "is_active": {"type": "boolean"},
            },
        }
        form_data_json_str = (
            '{"name": "{{name}}", "age": "{{age}}", "is_active": "{{is_active}}"}'
        )
        kwargs = {"name": "John", "age": 30, "is_active": "true"}
        expected_result = {"name": "John", "age": "30", "is_active": "true"}
        result = hydrate_input_fields(input_schema, form_data_json_str, **kwargs)
        self.assertEqual(result, expected_result)

    def test_hydrate_array_values(self):
        input_schema = {"type": "object", "properties": {"tags": {"type": "array"}}}
        form_data_json_str = '{"tags": "{{tags}}"}'
        kwargs = {"tags": "one,two,three"}
        expected_result = {"tags": json.dumps(["one", "two", "three"])}
        result = hydrate_input_fields(input_schema, form_data_json_str, **kwargs)
        self.assertEqual(result, expected_result)

    def test_hydrate_object_values(self):
        input_schema = {"type": "object", "properties": {"config": {"type": "object"}}}
        form_data_json_str = '{"config": "{{config}}"}'
        kwargs = {"config": '{"key1": "value1", "key2": "value2"}'}
        expected_result = {"config": '{"key1": "value1", "key2": "value2"}'}
        result = hydrate_input_fields(input_schema, form_data_json_str, **kwargs)
        self.assertEqual(result, expected_result)

    def test_hydrate_deeply_nested_structure(self):
        input_schema = {
            "type": "object",
            "properties": {
                "user": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "preferences": {
                            "type": "object",
                            "properties": {"notifications": {"type": "boolean"}},
                        },
                    },
                }
            },
        }
        form_data_json_str = '{"user": {"name": "{{name}}", "preferences": {"notifications": "{{notifications}}"}}}'
        kwargs = {"name": "Jane", "notifications": "false"}
        expected_result = {
            "user": {"name": "Jane", "preferences": {"notifications": "false"}}
        }
        result = hydrate_input_fields(input_schema, form_data_json_str, **kwargs)
        self.assertEqual(result, expected_result)

    def test_invalid_type_raises_exception(self):
        input_schema = {
            "type": "object",
            "properties": {"some_field": {"type": "unknown"}},
        }
        form_data_json_str = '{"some_field": "{{some_field}}"}'
        kwargs = {"some_field": "some_value"}
        with self.assertRaises(NotImplementedError):
            hydrate_input_fields(input_schema, form_data_json_str, **kwargs)

    def test_missing_placeholder_in_kwargs(self):
        input_schema = {"type": "object", "properties": {"name": {"type": "string"}}}
        form_data_json_str = '{"name": "{{name}}"}'
        kwargs = {}
        expected_result = {
            "name": "{{name}}"
        }  # Placeholder not replaced because it's not in kwargs
        result = hydrate_input_fields(input_schema, form_data_json_str, **kwargs)
        self.assertEqual(result, expected_result)


if __name__ == "__main__":
    unittest.main()
