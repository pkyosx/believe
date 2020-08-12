from .internal import BelieveBase
from .internal import validate


class OneOf(BelieveBase):
    def initialize(self, *candidates):
        self.candidates = candidates

    def validate(self, rhs, e_path=""):
        for i in self.candidates:
            if i == rhs:
                return
        self.raise_validate_error(rhs, e_path=e_path, e_msg="invalid_argument")


class AnyOrder(BelieveBase):
    def initialize(self, list_obj):
        assert isinstance(list_obj, list)

        self.list_obj = list_obj

    def validate(self, rhs, e_path=""):
        if len(rhs) != len(self.list_obj):
            self.raise_validate_error(rhs, e_path=e_path, e_msg="different_length")
        list_obj = self.list_obj[:]
        for idx, i in enumerate(rhs):
            if not i in list_obj:
                self.raise_validate_error(rhs, e_path=e_path, e_msg=f'item_not_found_at_index: {idx}')
            list_obj.remove(i)


class ListOf(BelieveBase):
    def initialize(self, one_item, n_item=None, min_item=None, max_item=None):
        self.one_item = one_item
        self.n_item = n_item
        self.min_item = min_item
        self.max_item = max_item

    def validate(self, rhs, e_path=""):
        if not isinstance(rhs, list):
            self.raise_validate_error(rhs, e_path=e_path, e_msg="not_list")
        if self.n_item is not None:
            if not len(rhs) == self.n_item:
                self.raise_validate_error(rhs, e_path=e_path, e_msg=f'mismatch_item_count: {len(rhs)} != {self.n_item}')
        if self.min_item is not None:
            if len(rhs) < self.min_item:
                self.raise_validate_error(rhs, e_path=e_path, e_msg=f'too_few_items: {len(rhs)} < {self.min_item}')
        if self.max_item is not None:
            if len(rhs) > self.max_item:
                self.raise_validate_error(rhs, e_path=e_path, e_msg=f'too_many_items: {len(rhs)} > {self.max_item}')
        for idx, val in enumerate(rhs):
            validate(self.one_item, val, "%s.%s" % (e_path, str(idx)))
