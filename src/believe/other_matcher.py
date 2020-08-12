from .internal import MatcherBase


class Nullable(MatcherBase):
    def initialize(self, obj):
        self.obj = obj

    def validate(self, rhs, e_path=""):
        if rhs is None:
            return
        if self.obj != rhs:
            self.raise_validate_error(rhs, e_path=e_path, e_msg="invalid_param")


class Not(MatcherBase):
    def initialize(self, obj):
        self.obj = obj

    def validate(self, rhs, e_path=""):
        if self.obj == rhs:
            self.raise_validate_error(rhs, e_path=e_path, e_msg="invalid_param")


class Any(MatcherBase):
    def initialize(self, *type_classes):
        self.type_classes = type_classes
        self.init_arg_str(*[i.__name__ for i in type_classes])

    def validate(self, rhs, e_path=""):
        if not self.type_classes:
            return
        if not isinstance(rhs, self.type_classes):
            self.raise_validate_error(rhs, e_path=e_path, e_msg="invalid_param")
