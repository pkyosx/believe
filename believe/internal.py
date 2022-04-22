import abc
import inspect
from typing import Any
from .error import ValidateError


# We use Ellipsis to differentiate if caller assign non-default value for kwargs
NO_CHECK = USE_DEFAULT = Ellipsis


class BelieveBase(abc.ABC):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.__arg_str = self.__init_arg_str(*args, **kwargs)

    def __ne__(self, rhs: Any) -> bool:
        return not self.__eq__(rhs)

    def __eq__(self, rhs: Any) -> bool:
        try:
            self.validate(rhs)
            return True
        except ValidateError:
            return False

    def __str__(self) -> str:
        return "%s(%s)" % (self.__class__.__name__, self.__arg_str)

    def __repr__(self) -> str:
        return self.__str__()

    def __to_str(self, val: Any) -> str:
        if inspect.isclass(val) and hasattr(val, "__name__"):
            return val.__name__
        else:
            return str(val)

    def __init_arg_str(self, *args: Any, **kwargs: Any) -> str:
        list_of_arg = list(args)
        for k, v in kwargs.items():
            if v != Ellipsis:  # only show overwritten kwargs
                list_of_arg.append("%s=%s" % (k, v))
        return ", ".join([self.__to_str(i) for i in list_of_arg])

    def raise_validate_error(self, rhs: Any, **kwargs: Any) -> None:
        raise ValidateError(self, rhs, **kwargs)

    @abc.abstractmethod
    def validate(self, rhs: Any, e_path: str = "") -> None:
        raise NotImplemented()


def validate(v1: Any, v2: Any, e_path: str = "") -> None:
    if isinstance(v1, BelieveBase):
        v1.validate(v2, e_path=e_path)
    elif isinstance(v2, BelieveBase):
        v2.validate(v1, e_path=e_path)
    elif v1 != v2:
        raise ValidateError(v1, v2, e_path=e_path)
