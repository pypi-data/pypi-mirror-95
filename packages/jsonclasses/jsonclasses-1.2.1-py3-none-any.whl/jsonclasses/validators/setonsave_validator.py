"""module for setonsave validator."""
from typing import Callable, Any
from inspect import signature
from .validator import Validator
from ..contexts import TransformingContext


class SetOnSaveValidator(Validator):
    """Setonsave validator updates or sets value on save."""

    def __init__(self, setter: Callable) -> None:
        self.setter = setter

    def serialize(self, context: TransformingContext) -> Any:
        params_len = len(signature(self.setter).parameters)
        if params_len == 1:
            return self.setter(context.value)
        return self.setter()
