import json
import typing
from .internal import BelieveBase
from .internal import validate
from .internal import no_check

class Dict(BelieveBase):
    def __init__(self, dict_obj: typing.Dict):
        assert isinstance(dict_obj, dict)

        super().__init__(dict_obj)
        self.__dict_obj = dict_obj

    def validate(self, rhs, e_path=""):
        if not isinstance(rhs, dict):
            self.raise_validate_error(rhs, e_path=e_path, e_msg="not_dict")

        # validate required field
        for k, v in self.__dict_obj.items():
            if not isinstance(v, Optional):
                if k not in rhs:
                    self.raise_validate_error(rhs, e_path=e_path, e_msg=f'missing_required_field: {k}')

        # validate field value
        for k, v in rhs.items():
            if k in self.__dict_obj:
                validate(self.__dict_obj[k], v, "%s.%s" % (e_path, k))
            else:
                self.raise_validate_error(rhs, e_path=e_path, e_msg="unknown_field", e_unsafe_msg=f'unknown_field: {k}')


class DictOf(BelieveBase):
    def __init__(self, key: typing.Any, value: typing.Any, n_item: int = no_check, min_item: int = no_check, max_item: int = no_check):
        assert n_item == no_check or isinstance(n_item, int)
        assert min_item == no_check or isinstance(min_item, int)
        assert max_item == no_check or isinstance(max_item, int)

        super().__init__(key, value, n_item=n_item, min_item=min_item, max_item=max_item)
        self.__key = key
        self.__value = value
        self.__n_item = n_item
        self.__min_item = min_item
        self.__max_item = max_item

    def validate(self, rhs, e_path=""):
        if not isinstance(rhs, dict):
            self.raise_validate_error(rhs, e_path=e_path, e_msg="not_dict")
        if self.__n_item != no_check:
            if not len(rhs) == self.__n_item:
                self.raise_validate_error(rhs, e_path=e_path, e_msg=f'mismatch_item_count: {len(rhs)} != {self.__n_item}')
        if self.__min_item != no_check:
            if len(rhs) < self.__min_item:
                self.raise_validate_error(rhs, e_path=e_path, e_msg=f'too_few_items: {len(rhs)} < {self.__min_item}')
        if self.__max_item != no_check:
            if len(rhs) > self.__max_item:
                self.raise_validate_error(rhs, e_path=e_path, e_msg=f'too_many_items: {len(rhs)} > {self.__max_item}')
        for k, v in rhs.items():
            validate(self.__key, k, "%s.%s" % (e_path, k))
            validate(self.__value, v, "%s.%s" % (e_path, k))

class Optional(BelieveBase):
    def __init__(self, value: typing.Any):
        super().__init__(value)
        self.__value = value

    def validate(self, rhs: typing.Any, e_path: str = ""):
        validate(rhs, self.__value, e_path=e_path)
