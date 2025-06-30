from langflow.custom import Component
from langflow.io import HandleInput, Output, StrInput
from langflow.schema import Data, DataFrame, Message


class LoggerComponent(Component):
    display_name = "Logger"
    description = "Logs the passed in object and then passes it on unchanged."
    icon = "bug"
    name = "LoggerComponent"

    inputs = [
         StrInput(
            name="log_message",
            display_name="Log Message",
            info="The message to log before the object.",
            required=True,
        ),
        HandleInput(
            name="input_object",
            display_name="Input",
            input_types=["DataFrame", "Data", "Message"],
            info="Accepts either a DataFrame, a Data object or a Message.",
            required=True,
        ),
    ]

    outputs = [
        Output(display_name="Data", name="output_data", method="build_data_output"),
        Output(display_name="DataFrame", name="output_dataframe", method="build_dataframe_output"),
        Output(display_name="Message", name="output_message", method="build_message_output"),
    ]
    
    def _log_object(self):
        log_msg = f"{self.log_message} {self.input_object}"
        self.log(log_msg,"LoggerComponent")
        print(log_msg)
        self.status = self.log_message

    def build_data_output(self) -> Data:
        if not isinstance(self.input_object,Data):
            raise Exception("Input was not a Data object!")
        self._log_object()
        return self.input_object
        
    def build_dataframe_output(self) -> DataFrame:
        if not isinstance(self.input_object,DataFrame):
            raise Exception("Input was not a DataFrame object!")
        self._log_object()
        return self.input_object    
        
    def build_message_output(self) -> Message:
        if not isinstance(self.input_object,Message):
            raise Exception("Input was not a Message object!")
        self._log_object()
        return self.input_object      
