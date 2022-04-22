from typing import Any, List

from .internal import BelieveBase
from .internal import validate
from .internal import NO_CHECK


class OneOf(BelieveBase):
    def __init__(self, *candidates: Any) -> None:
        super().__init__(*candidates)
        self.__candidates = candidates

    def validate(self, rhs: Any, e_path: str = "") -> None:
        for i in self.__candidates:
            if i == rhs:
                return
        self.raise_validate_error(rhs, e_path=e_path, e_msg="invalid_argument")


class AnyOrder(BelieveBase):
    def __init__(self, list_obj: List) -> None:
        assert isinstance(list_obj, list)

        super().__init__(list_obj)
        self.__list_obj = list_obj

    def validate(self, rhs: List[Any], e_path: str = "") -> None:
        if not isinstance(rhs, list):
            self.raise_validate_error(rhs, e_path=e_path)
        if len(rhs) != len(self.__list_obj):
            self.raise_validate_error(rhs, e_path=e_path, e_msg="different_length")
        list_obj = self.__list_obj[:]
        for idx, i in enumerate(rhs):
            if not i in list_obj:
                self.raise_validate_error(
                    rhs, e_path=e_path, e_msg=f"item_not_found_at_index: {idx}"
                )
            list_obj.remove(i)


class ListOf(BelieveBase):
    def __init__(
        self,
        one_item: Any,
        n_item: int = NO_CHECK,
        min_item: int = NO_CHECK,
        max_item: int = NO_CHECK,
    ) -> None:
        assert n_item == NO_CHECK or isinstance(n_item, int)
        assert min_item == NO_CHECK or isinstance(min_item, int)
        assert max_item == NO_CHECK or isinstance(max_item, int)

        super().__init__(one_item, n_item=n_item, min_item=min_item, max_item=max_item)

        self.__one_item = one_item
        self.__n_item = n_item
        self.__min_item = min_item
        self.__max_item = max_item

    def validate(self, rhs: List, e_path: str = "") -> None:
        if not isinstance(rhs, list):
            self.raise_validate_error(rhs, e_path=e_path, e_msg="not_list")
        if self.__n_item != NO_CHECK:
            if not len(rhs) == self.__n_item:
                self.raise_validate_error(
                    rhs,
                    e_path=e_path,
                    e_msg=f"mismatch_item_count: {len(rhs)} != {self.__n_item}",
                )
        if self.__min_item != NO_CHECK:
            if len(rhs) < self.__min_item:
                self.raise_validate_error(
                    rhs,
                    e_path=e_path,
                    e_msg=f"too_few_items: {len(rhs)} < {self.__min_item}",
                )
        if self.__max_item != NO_CHECK:
            if len(rhs) > self.__max_item:
                self.raise_validate_error(
                    rhs,
                    e_path=e_path,
                    e_msg=f"too_many_items: {len(rhs)} > {self.__max_item}",
                )
        for idx, val in enumerate(rhs):
            validate(self.__one_item, val, "%s.%s" % (e_path, str(idx)))
