import abc
import inspect
from typing import Any
from .error import ValidateError


# We use Ellipsis to differentiate if caller assign non-default value for kwargs
NO_CHECK = USE_DEFAULT = Ellipsis

class BelieveBase(abc.ABC):
    def __init__(self, *args: Any, **kwargs: Any):
        self.__arg_str = self.init_arg_str(*args, **kwargs)

    def __ne__(self, rhs: Any):
        return not self.__eq__(rhs)

    def __eq__(self, rhs: Any):
        try:
            self.validate(rhs)
            return True
        except ValidateError:
            return False

    def __str__(self):
        return "%s(%s)" % (self.__class__.__name__, self.__arg_str)

    def __repr__(self):
        return self.__str__()

    def to_str(self, val: Any) -> str:
        if inspect.isclass(val) and hasattr(val, "__name__"):
            return val.__name__
        else:
            return str(val)

    def init_arg_str(self, *args: Any, **kwargs: Any):
        list_of_arg = list(args)
        for k, v in kwargs.items():
            if v != Ellipsis: # only show overwritten kwargs
                list_of_arg.append("%s=%s" % (k, v))
        return ", ".join([self.to_str(i) for i in list_of_arg])

    def raise_validate_error(self, rhs: Any, **kwargs: Any):
        raise ValidateError(self, rhs, **kwargs)

    @abc.abstractmethod
    def validate(self, rhs: Any, e_path: str = ""):
        raise NotImplemented()


def validate(v1: Any, v2: Any, e_path: str = ""):
    if isinstance(v1, BelieveBase):
        v1.validate(v2, e_path=e_path)
    elif isinstance(v2, BelieveBase):
        v2.validate(v1, e_path=e_path)
    elif v1 != v2:
        raise ValidateError(v1, v2, e_path=e_path)
