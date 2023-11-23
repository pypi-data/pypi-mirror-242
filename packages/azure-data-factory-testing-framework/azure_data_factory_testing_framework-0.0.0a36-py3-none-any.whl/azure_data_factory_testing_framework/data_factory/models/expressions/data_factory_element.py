from typing import Generic, TypeVar, Union

from azure_data_factory_testing_framework.data_factory.generated.models import DataFactoryElement
from azure_data_factory_testing_framework.functions import parse_expression
from azure_data_factory_testing_framework.state import RunState

T = TypeVar("T")


class DataFactoryElement(Generic[T]):
    def __init__(self) -> None:
        """DataFactoryElement."""
        self.value: Union[str, int, bool, float] = None

    def evaluate(self: DataFactoryElement, state: RunState) -> Union[str, int, bool, float]:
        self.value = parse_expression(self.expression).evaluate(state)
        return self.value
