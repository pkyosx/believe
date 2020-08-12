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


class AnyInt(BelieveBase):
    def initialize(self, min_value=None, max_value=None):
        assert min_value is None or isinstance(min_value, int)
        assert max_value is None or isinstance(max_value, int)

        self.min_value = min_value
        self.max_value = max_value

    def validate(self, rhs, e_path=""):
        if not isinstance(rhs, int):
            self.raise_validate_error(rhs, e_path=e_path)
        if self.min_value is not None and self.min_value > rhs:
            self.raise_validate_error(rhs, e_path=e_path, e_msg=f'value_too_small: {rhs} < {self.min_value}')
        if self.max_value is not None and self.max_value < rhs:
            self.raise_validate_error(rhs, e_path=e_path, e_msg=f'value_too_large: {rhs} > {self.max_value}')
