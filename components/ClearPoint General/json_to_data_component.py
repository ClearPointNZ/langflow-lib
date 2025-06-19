from langflow.custom import Component
from langflow.io import Output, MultilineInput
from langflow.schema import Data
import json


class JsonStringToDataComponent(Component):
    display_name = "JSON to Data"
    description = "This component converts a JSON string to a Data object."
    icon = "file-json"
    name = "JsonStringToData"

    inputs = [
        MultilineInput(name="json_string", display_name="JSON string"),
    ]

    outputs = [
        Output(name="json_as_data", display_name="JSON as Data", method="convert_json_to_data")
    ]

    def convert_json_to_data(self) -> Data:
        data = Data(data=json.loads(self.json_string))
        self.status = data
        return data
