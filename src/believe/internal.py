from .error import ValidateError
from .error import ImplementationError


class BelieveBase(object):
    def __init__(self, *args, **kwargs):
        self.init_arg_str(*args, **kwargs)
        self.initialize(*args, **kwargs)

    def __ne__(self, rhs):
        return not self.__eq__(rhs)

    def __eq__(self, rhs):
        try:
            self.validate(rhs)
            return True
        except ValidateError:
            return False

    def __str__(self):
        return "%s(%s)" % (self.__class__.__name__, self.__arg_str)

    def __repr__(self):
        return self.__str__()

    def init_arg_str(self, *args, **kwargs):
        list_of_arg = list(args)
        for k, v in kwargs.items():
            list_of_arg.append("%s=%s" % (k, v))
        self.__arg_str = ", ".join([str(i) for i in list_of_arg])

    def raise_validate_error(self, rhs, **kwargs):
        raise ValidateError(self, rhs, **kwargs)

    def validate(self, rhs, e_path=""):
        raise ImplementationError("Need implementation")

    def initialize(self, *args, **kwargs):
        raise ImplementationError("Need implementation")


def validate(v1, v2, e_path=""):
    if hasattr(v1, "validate"):
        v1.validate(v2, e_path=e_path)
    elif hasattr(v2, "validate"):
        v2.validate(v1, e_path=e_path)
    elif v1 != v2:
        raise ValidateError(v1, v2, e_path=e_path)
