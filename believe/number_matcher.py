from .internal import BelieveBase


class Almost(BelieveBase):
    def initialize(self, ts, ts_range=3):
        assert isinstance(ts, (int, float))
        assert isinstance(ts_range, (int, float))

        self.ts = ts
        self.ts_range = ts_range

    def validate(self, rhs, e_path=""):
        if not isinstance(rhs, (int, float)):
            self.raise_validate_error(rhs, e_path=e_path, e_msg=f'not_int_or_float')
        if not self.ts - self.ts_range <= rhs <= self.ts + self.ts_range:
            self.raise_validate_error(rhs, e_path=e_path, e_msg=f'not_in_range')

class AnyNumber(BelieveBase):
    def initialize(self, value_type, min_value=None, max_value=None):
        assert value_type in (int, float)
        assert min_value is None or isinstance(min_value, value_type)
        assert max_value is None or isinstance(max_value, value_type)
        self.min_value = min_value
        self.max_value = max_value
        self.value_type = value_type

    def validate(self, rhs, e_path=""):
        if not isinstance(rhs, self.value_type):
            self.raise_validate_error(rhs, e_path=e_path)
        if self.min_value is not None and self.min_value > rhs:
            self.raise_validate_error(rhs, e_path=e_path, e_msg=f'value_too_small: {rhs} < {self.min_value}')
        if self.max_value is not None and self.max_value < rhs:
            self.raise_validate_error(rhs, e_path=e_path, e_msg=f'value_too_large: {rhs} > {self.max_value}')

class AnyInt(AnyNumber):
    def initialize(self, min_value=None, max_value=None):
        super().initialize(value_type=int, min_value=min_value, max_value=max_value)

class AnyFloat(AnyNumber):
    def initialize(self, min_value=None, max_value=None):
        super().initialize(value_type=float, min_value=min_value, max_value=max_value)