""" Schema to Python converter """
import random
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

from openapi_tester.constants import OPENAPI_PYTHON_MAPPING
from openapi_tester.utils import combine_sub_schemas


class SchemaToPythonConverter:
    """
    This class is used both by the DocumentationError format method and the various test suites.
    """

    result: Any
    faker: Any = None

    def __init__(self, schema: dict, with_faker: bool = False):
        if with_faker:
            # We are importing faker here to ensure this remains a dev dependency
            from faker import Faker

            Faker.seed(0)
            self.faker = Faker()
        self.result = self.convert_schema(schema)

    def convert_schema(self, schema: Dict[str, Any]) -> Any:
        schema_type = schema.get("type", "object")
        sample: List[Dict[str, Any]] = []
        if "allOf" in schema:
            return self.convert_schema(combine_sub_schemas(schema["allOf"]))
        if "oneOf" in schema:
            while not sample:
                sample = random.sample(schema["oneOf"], 1)
            return self.convert_schema(sample[0])
        if "anyOf" in schema:
            while not sample:
                sample = random.sample(schema["anyOf"], random.randint(1, len(schema["anyOf"])))
            return self.convert_schema(combine_sub_schemas(sample))
        if schema_type == "array":
            return self.convert_schema_array_to_list(schema)
        if schema_type == "object":
            return self.convert_schema_object_to_dict(schema)
        if self.faker is None:
            return OPENAPI_PYTHON_MAPPING[schema_type]
        return self.schema_type_to_mock_value(schema)

    def schema_type_to_mock_value(self, schema_object: Dict[str, Any]) -> Any:
        faker_handlers = {
            "array": self.faker.pylist,
            "boolean": self.faker.pybool,
            "file": self.faker.pystr,
            "integer": self.faker.pyint,
            "number": self.faker.pyfloat,
            "object": self.faker.pydict,
            "string": self.faker.pystr,
        }
        schema_format: str = schema_object.get("format", "")
        schema_type: str = schema_object.get("type", "")
        minimum: Optional[Union[int, float]] = schema_object.get("minimum")
        maximum: Optional[Union[int, float]] = schema_object.get("maximum")
        enum: Optional[list] = schema_object.get("enum")
        if enum:
            return enum[0]
        if schema_format and schema_type == "string":
            if schema_format == "date":
                return datetime.now().date().isoformat()
            if schema_format == "date-time":
                return datetime.now().isoformat()
            if schema_format == "byte":
                return self.faker.pystr().encode("utf-8")
        if schema_type in ["integer", "number"] and (minimum is not None or maximum is not None):
            if minimum is not None:
                minimum += 1 if schema_object.get("excludeMinimum") else 0
            if maximum is not None:
                maximum -= 1 if schema_object.get("excludeMaximum") else 0
            if minimum is not None or maximum is not None:
                minimum = minimum or 0
                maximum = maximum or minimum * 2
                if schema_type == "integer":
                    return self.faker.pyint(minimum, maximum)
                return random.uniform(minimum, maximum)
        return faker_handlers[schema_type]()

    def convert_schema_object_to_dict(self, schema_object: dict) -> Dict[str, Any]:
        properties = schema_object.get("properties", {})
        parsed_schema: Dict[str, Any] = {}
        for key, value in properties.items():
            parsed_schema[key] = self.convert_schema(value)
        return parsed_schema

    def convert_schema_array_to_list(self, schema_array: Any) -> List[Any]:
        parsed_items: List[Any] = []
        raw_items = schema_array.get("items", {})
        min_items = schema_array.get("minItems", 1)
        max_items = schema_array.get("maxItems", 1)
        while len(parsed_items) < min_items or len(parsed_items) < max_items:
            parsed_items.append(self.convert_schema(raw_items))
        return parsed_items
