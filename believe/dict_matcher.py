import json
from .internal import BelieveBase
from .internal import validate


class Dict(BelieveBase):
    def initialize(self, dict_obj):
        self.dict_obj = dict_obj
        assert isinstance(dict_obj, dict)

    def validate(self, rhs, e_path=""):
        if not isinstance(rhs, dict):
            self.raise_validate_error(rhs, e_path=e_path, e_msg="not_dict")

        # validate required field
        for k, v in self.dict_obj.items():
            if not isinstance(v, Optional):
                if k not in rhs:
                    self.raise_validate_error(rhs, e_path=e_path, e_msg=f'missing_required_field: {k}')

        # validate field value
        for k, v in rhs.items():
            if k in self.dict_obj:
                validate(self.dict_obj[k], v, "%s.%s" % (e_path, k))
            else:
                self.raise_validate_error(rhs, e_path=e_path, e_msg="unknown_field", e_unsafe_msg=f'unknown_field: {k}')

class DictStr(Dict):
    def validate(self, rhs, e_path=""):
        try:
            rhs_dict = json.loads(rhs)
        except:
            self.raise_validate_error(rhs, e_path=e_path, e_msg="not_dict_string")
        super().validate(rhs_dict, e_path)

class DictOf(BelieveBase):
    def initialize(self, key, value, n_item=None, min_item=None, max_item=None):
        self.key = key
        self.value = value
        self.n_item = n_item
        self.min_item = min_item
        self.max_item = max_item

    def validate(self, rhs, e_path=""):
        if not isinstance(rhs, dict):
            self.raise_validate_error(rhs, e_path=e_path, e_msg="not_dict")
        if self.n_item is not None:
            if not len(rhs) == self.n_item:
                self.raise_validate_error(rhs, e_path=e_path, e_msg=f'mismatch_item_count: {len(rhs)} != {self.n_item}')
        if self.min_item is not None:
            if len(rhs) < self.min_item:
                self.raise_validate_error(rhs, e_path=e_path, e_msg=f'too_few_items: {len(rhs)} < {self.min_item}')
        if self.max_item is not None:
            if len(rhs) > self.max_item:
                self.raise_validate_error(rhs, e_path=e_path, e_msg=f'too_many_items: {len(rhs)} > {self.max_item}')
        for k, v in rhs.items():
            validate(self.key, k, "%s.%s" % (e_path, k))
            validate(self.value, v, "%s.%s" % (e_path, k))

class Optional(BelieveBase):
    def initialize(self, value):
        self.value = value

    def validate(self, rhs, e_path=""):
        validate(rhs, self.value, e_path=e_path)
