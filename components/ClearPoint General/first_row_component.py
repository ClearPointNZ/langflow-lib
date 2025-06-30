from langflow.custom import Component
from langflow.io import DataFrameInput, Output
from langflow.schema import Data


class FirstRowComponent(Component):
    display_name = "First row"
    description = "Takes the first row of a Dataframe and converts it to a Data object"   
    icon = "list-start"
    name = "FirstRowComponent"

    inputs = [
        DataFrameInput(
            name="input_dataframe",
            display_name="Dataframe",
            info="This is the input DataFrame"
        ),
    ]

    outputs = [
        Output(display_name="Data", name="output_data", method="build_output"),
    ]

    def build_output(self) -> Data:
        data = self.input_dataframe.to_data_list()[0] # TODO empty list checking and handling
        self.status = data
        return data
