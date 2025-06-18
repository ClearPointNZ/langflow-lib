from langflow.custom import Component
from langflow.io import Output, StrInput
from langflow.schema import Data


class EchoComponent(Component):
    display_name = "Echo Component"
    description = "This component echoes back the input it receives again."
    icon = "sparkles"
    name = "EchoComponent"

    inputs = [
        StrInput(name="str_to_echo", display_name="String to echo"),
    ]

    outputs = [
        Output(name="echoed_str", display_name="Echoed String", method="echo_str")
    ]

    def echo_str(self) -> Data:
        data = Data(value=f"{self.str_to_echo} echoed back")
        self.status = data
        return data
