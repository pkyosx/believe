import uuid

from .internal import MatcherBase


class AnyStr(MatcherBase):
    def initialize(self, min_len=None, max_len=None):
        self.min_len = min_len
        self.max_len = max_len

    def validate(self, rhs, e_path=""):
        if not isinstance(rhs, str):
            self.raise_validate_error(rhs, e_path=e_path, e_msg="not_string")
        if self.min_len is not None and len(rhs) < self.min_len:
            self.raise_validate_error(rhs, e_path=e_path, e_msg=f'string_too_short: {len(rhs)} < {self.min_len}')
        if self.max_len is not None and len(rhs) > self.max_len:
            self.raise_validate_error(rhs, e_path=e_path, e_msg=f'string_too_long: {len(rhs)} > {self.max_len}')


class AnyIntStr(MatcherBase):
    def initialize(self):
        pass

    def validate(self, rhs, e_path=""):
        if not isinstance(rhs, str):
            self.raise_validate_error(rhs, e_path=e_path, e_msg="not_string")

        try:
            int(rhs)
        except ValueError:
            self.raise_validate_error(rhs, e_path=e_path, e_msg="not_int_string")


class AnyUUID(MatcherBase):
    def initialize(self):
        pass

    def validate(self, rhs, e_path=""):
        if not isinstance(rhs, str) or len(rhs) != 36:
            self.raise_validate_error(rhs, e_path=e_path, e_msg="invalid_uuid")
        try:
            uuid.UUID(rhs)
        except (TypeError, ValueError):
            self.raise_validate_error(rhs, e_path=e_path, e_msg="invalid_uuid")


class AnyIPV4(MatcherBase):
    def initialize(self):
        pass

    def validate(self, rhs, e_path=""):
        if not isinstance(rhs, str):
            self.raise_validate_error(rhs, e_path=e_path, e_msg="invalid_ipv4")
        tokens = rhs.split('.')
        if len(tokens) != 4:
            self.raise_validate_error(rhs, e_path=e_path, e_msg="invalid_ipv4")
        for token in tokens:
            try:
                token = int(token)
            except ValueError:
                self.raise_validate_error(rhs, e_path=e_path, e_msg="invalid_ipv4")
            if not 0 <= token < 256:
                self.raise_validate_error(rhs, e_path=e_path, e_msg="invalid_ipv4")


class AnySHA1(MatcherBase):
    def initialize(self):
        pass

    def validate(self, rhs, e_path=""):
        if not isinstance(rhs, str):
            self.raise_validate_error(rhs, e_path=e_path, e_msg="invalid_sha1")
        if len(rhs) != 40:
            self.raise_validate_error(rhs, e_path=e_path, e_msg="invalid_sha1")
        try:
            int(rhs, 16)
        except ValueError:
            self.raise_validate_error(rhs, e_path=e_path, e_msg="invalid_sha1")
