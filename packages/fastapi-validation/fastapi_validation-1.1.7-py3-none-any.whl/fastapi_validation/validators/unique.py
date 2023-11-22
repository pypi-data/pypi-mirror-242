from typing import Any, Optional

from fastapi_exception import DuplicateError, throw_validation_with_exception
from pydantic import ValidationInfo

from ..constants.validator_constant import VALIDATOR_UNIQUE
from ..types.custom_condition_type import CustomCondition
from .exist import Exists


# TODO: Extend request body to support custom exclude
class Unique(Exists):
    __name__ = VALIDATOR_UNIQUE

    def __init__(
        self,
        table,
        column: Any,
        case_insensitive: bool = False,
        customs: Optional[list[CustomCondition]] = [],
    ):
        super().__init__(table, column, case_insensitive, customs)

    def __call__(self, values: Optional[Any], info: ValidationInfo) -> Optional[Any]:
        if not values:
            return values

        is_list = isinstance(values, list)
        if not is_list:
            values = [values]

        for value in values:
            criterion = self.exist_validator.init_criterion(value)
            self.exist_validator.build_custom_criterion(criterion, info.data)

            if self.exist_validator.validate(*criterion):
                throw_validation_with_exception(DuplicateError(property=self.column, loc=('body', info.field_name)))

        return values if is_list else values[0]
