import uuid
import json
from urllib.parse import urlparse

from .internal import BelieveBase


class AnyStr(BelieveBase):
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


class AnyIntStr(BelieveBase):
    def initialize(self):
        pass

    def validate(self, rhs, e_path=""):
        if not isinstance(rhs, str):
            self.raise_validate_error(rhs, e_path=e_path, e_msg="not_string")

        try:
            int(rhs)
        except ValueError:
            self.raise_validate_error(rhs, e_path=e_path, e_msg="not_int_string")


class AnyUUID(BelieveBase):
    def initialize(self):
        pass

    def validate(self, rhs, e_path=""):
        if not isinstance(rhs, str) or len(rhs) != 36:
            self.raise_validate_error(rhs, e_path=e_path, e_msg="invalid_uuid")
        try:
            uuid.UUID(rhs)
        except (TypeError, ValueError):
            self.raise_validate_error(rhs, e_path=e_path, e_msg="invalid_uuid")


class AnyIPV4(BelieveBase):
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


class AnySHA1(BelieveBase):
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


class AnyJsonStr(BelieveBase):
    def initialize(self, obj):
        self.obj = obj
    def validate(self, rhs, e_path=""):
        if not isinstance(rhs, str):
            self.raise_validate_error(rhs, e_path=e_path, e_msg="not_string")
        try:
            obj = json.loads(rhs)
        except:
            self.raise_validate_error(rhs, e_path=e_path, e_msg="not_json_string")
        if obj != self.obj:
            self.raise_validate_error(rhs, e_path=e_path, e_msg="mismatch_json_string")


class AnyUrl(BelieveBase):
    def initialize(self, url_str):
        self.url = urlparse(url_str)

    def _normalize_query(self, query):
        return "&".join(sorted(query.split("&")))

    def _default_port(self, scheme):
        if scheme == "http":
            return 80
        elif scheme == "https":
            return 443

    def validate(self, rhs, e_path=""):
        if not isinstance(rhs, str):
            self.raise_validate_error(rhs, e_path=e_path, e_msg="not_string")

        o = urlparse(rhs)

        if self.url.scheme != o.scheme:
            self.raise_validate_error(rhs, e_path=e_path, e_msg="mismatch_scheme")

        default_port = self._default_port(self.url.scheme)

        if self.url.username != o.username:
            self.raise_validate_error(rhs, e_path=e_path, e_msg="mismatch_username")

        if self.url.password != o.password:
            self.raise_validate_error(rhs, e_path=e_path, e_msg="mismatch_password")

        if self.url.hostname != o.hostname:
            self.raise_validate_error(rhs, e_path=e_path, e_msg="mismatch_hostname")

        if (self.url.port or default_port) != (o.port or default_port):
            self.raise_validate_error(rhs, e_path=e_path, e_msg="mismatch_port")

        if self.url.path != o.path:
            self.raise_validate_error(rhs, e_path=e_path, e_msg="mismatch_path")

        if self._normalize_query(self.url.query) != self._normalize_query(o.query):
            self.raise_validate_error(rhs, e_path=e_path, e_msg="mismatch_query")

