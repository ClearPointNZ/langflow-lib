from langflow.custom import Component
from langflow.io import  DropdownInput, IntInput, Output, DataInput, StrInput
from langflow.schema.message import Data
from evalidate import Expr


class DataConditionalRouterComponent(Component):
    display_name = "Data If-Else"
    description = "Routes an Data to a corresponding output based on a boolean expression."
    icon = "split"
    name = "DataConditionalRouter"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__iteration_updated = False

    inputs = [
        DataInput(
            name="input_data",
            display_name="Input",
            info="The primary text input for the operation.",
            required=True,
        ),
        StrInput(
            name="eval_expression",
            display_name="Eval Expression",
            info="The boolean expression to eval the input data against.",
            required=True,
        ),
        IntInput(
            name="max_iterations",
            display_name="Max Iterations",
            info="The maximum number of iterations for the conditional router.",
            value=10,
            advanced=True,
        ),
        DropdownInput(
            name="default_route",
            display_name="Default Route",
            options=["true_result", "false_result"],
            info="The default route to take when max iterations are reached.",
            value="false_result",
            advanced=True,
        ),       
    ]

    outputs = [
        Output(display_name="True", name="true_result", method="true_response"),        
        Output(display_name="False", name="false_result", method="false_response"),
    ]

    def _pre_run_setup(self):
        self.__iteration_updated = False

    def iterate_and_stop_once(self, route_to_stop: str):
        if not self.__iteration_updated:
            self.update_ctx({f"{self._id}_iteration": self.ctx.get(f"{self._id}_iteration", 0) + 1})
            self.__iteration_updated = True
            if self.ctx.get(f"{self._id}_iteration", 0) >= self.max_iterations and route_to_stop == self.default_route:
                route_to_stop = "true_result" if route_to_stop == "false_result" else "false_result"
            self.stop(route_to_stop)

    def true_response(self) -> Data:       
        # TODO: Proper error handling. Should check for bool result and handle EvalException
        result = Expr(self.eval_expression).eval(self.input_data.data)

        if result:
            self.status = self.input_data
            self.iterate_and_stop_once("false_result")
            return self.input_data
        self.iterate_and_stop_once("true_result")
        return Data(text="Eval is not true,.")

    def false_response(self) -> Data:
        # TODO: Proper error handling. Should check for bool result and handle EvalException
        result = Expr(self.eval_expression).eval(self.input_data.data)
        
        if not result:
            self.status = self.input_data
            self.iterate_and_stop_once("true_result")
            return self.input_data
        self.iterate_and_stop_once("false_result")
        return Data(text="Eval is not false.")

    