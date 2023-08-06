"""module for readonly validator."""
from ..fields import FieldDescription
from .validator import Validator


class PrimaryValidator(Validator):
    """Primary validator marks a field as the primary key."""

    def define(self, fdesc: FieldDescription) -> None:
        fdesc.primary = True
