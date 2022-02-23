from .internal import BelieveBase
from typing import Any, Union

class Nullable(BelieveBase):
    def __init__(self, obj: Any):
        super().__init__(obj)
        self.__obj = obj

    def validate(self, rhs: Any, e_path: str = ""):
        if rhs is None:
            return
        if self.__obj != rhs:
            self.raise_validate_error(rhs, e_path=e_path, e_msg="invalid_param")


class Not(BelieveBase):
    def __init__(self, obj: Any):
        super().__init__(obj)
        self.__obj = obj

    def validate(self, rhs: Any, e_path: str = ""):
        if self.__obj == rhs:
            self.raise_validate_error(rhs, e_path=e_path, e_msg="invalid_param")


class Any(BelieveBase):
    def __init__(self, *type_classes: type):
        for type_class in type_classes:
            assert isinstance(type_class, type)

        super().__init__(*type_classes)
        self.__type_classes = type_classes

    def validate(self, rhs: Any, e_path: str = ""):
        if not self.__type_classes:
            return
        if not isinstance(rhs, self.__type_classes):
            self.raise_validate_error(rhs, e_path=e_path, e_msg="invalid_param")
