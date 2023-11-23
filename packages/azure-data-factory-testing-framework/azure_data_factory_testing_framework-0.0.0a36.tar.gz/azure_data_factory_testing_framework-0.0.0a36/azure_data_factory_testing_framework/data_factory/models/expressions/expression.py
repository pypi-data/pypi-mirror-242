from typing import Union

from azure_data_factory_testing_framework.data_factory.generated.models import Expression
from azure_data_factory_testing_framework.functions.function_parser import parse_expression
from azure_data_factory_testing_framework.state import PipelineRunState


class Expression:
    def __init__(self) -> None:
        """Expression."""
        self.evaluated: Union[str, int, bool, float] = None

    def evaluate(self: Expression, state: PipelineRunState) -> Union[str, int, bool, float]:
        """Evaluates the expression by replacing all parameters and variables with their values and then evaluating the expression.

        Args:
            state: The state to use for evaluating the expression.
        """
        self.evaluated = parse_expression(self.value).evaluate(state)
        return self.evaluated
