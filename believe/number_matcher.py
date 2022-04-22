from typing import Union

from .internal import BelieveBase, NO_CHECK, USE_DEFAULT


class Almost(BelieveBase):
    def __init__(
        self, ts: Union[int, float], ts_range: Union[int, float] = USE_DEFAULT
    ) -> None:
        assert isinstance(ts, (int, float))
        assert ts_range == USE_DEFAULT or isinstance(ts_range, (int, float))
        super().__init__(ts, ts_range=ts_range)
        self.__ts = ts
        if ts_range == USE_DEFAULT:
            ts_range = 3
        self.__ts_range = ts_range

    def validate(self, rhs: Union[int, float], e_path: str = ""):
        if not isinstance(rhs, (int, float)):
            self.raise_validate_error(rhs, e_path=e_path, e_msg=f"not_int_or_float")
        if not self.__ts - self.__ts_range <= rhs <= self.__ts + self.__ts_range:
            self.raise_validate_error(rhs, e_path=e_path, e_msg=f"not_in_range")


class AnyInt(BelieveBase):
    def __init__(self, min_value: int = NO_CHECK, max_value: int = NO_CHECK) -> None:
        assert min_value == NO_CHECK or isinstance(min_value, int)
        assert max_value == NO_CHECK or isinstance(max_value, int)
        super().__init__(min_value=min_value, max_value=max_value)
        self.__min_value = min_value
        self.__max_value = max_value

    def validate(self, rhs: int, e_path: str = ""):
        if not isinstance(rhs, int):
            self.raise_validate_error(rhs, e_path=e_path)
        if self.__min_value != NO_CHECK and self.__min_value > rhs:
            self.raise_validate_error(
                rhs, e_path=e_path, e_msg=f"value_too_small: {rhs} < {self.__min_value}"
            )
        if self.__max_value != NO_CHECK and self.__max_value < rhs:
            self.raise_validate_error(
                rhs, e_path=e_path, e_msg=f"value_too_large: {rhs} > {self.__max_value}"
            )


class AnyFloat(BelieveBase):
    def __init__(
        self, min_value: float = NO_CHECK, max_value: float = NO_CHECK
    ) -> None:
        assert min_value == NO_CHECK or isinstance(min_value, float)
        assert max_value == NO_CHECK or isinstance(max_value, float)
        super().__init__(min_value=min_value, max_value=max_value)
        self.__min_value = min_value
        self.__max_value = max_value

    def validate(self, rhs: float, e_path: str = ""):
        if not isinstance(rhs, float):
            self.raise_validate_error(rhs, e_path=e_path)
        if self.__min_value != NO_CHECK and self.__min_value > rhs:
            self.raise_validate_error(
                rhs, e_path=e_path, e_msg=f"value_too_small: {rhs} < {self.__min_value}"
            )
        if self.__max_value != NO_CHECK and self.__max_value < rhs:
            self.raise_validate_error(
                rhs, e_path=e_path, e_msg=f"value_too_large: {rhs} > {self.__max_value}"
            )
