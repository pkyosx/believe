import uuid
import json
from typing import Dict, List, Union
from urllib.parse import urlparse

from .internal import BelieveBase, NO_CHECK


class AnyStr(BelieveBase):
    def __init__(self, min_len: int = NO_CHECK, max_len: int = NO_CHECK) -> None:
        assert min_len == NO_CHECK or isinstance(min_len, int)
        assert max_len == NO_CHECK or isinstance(max_len, int)

        super().__init__(min_len=min_len, max_len=max_len)
        self.__min_len = min_len
        self.__max_len = max_len

    def validate(self, rhs: str, e_path: str = "") -> None:
        if not isinstance(rhs, str):
            self.raise_validate_error(rhs, e_path=e_path, e_msg="not_string")
        if self.__min_len != NO_CHECK and len(rhs) < self.__min_len:
            self.raise_validate_error(
                rhs,
                e_path=e_path,
                e_msg=f"string_too_short: {len(rhs)} < {self.__min_len}",
            )
        if self.__max_len != NO_CHECK and len(rhs) > self.__max_len:
            self.raise_validate_error(
                rhs,
                e_path=e_path,
                e_msg=f"string_too_long: {len(rhs)} > {self.__max_len}",
            )


class AnyIntStr(BelieveBase):
    def validate(self, rhs: str, e_path: str = "") -> None:
        if not isinstance(rhs, str):
            self.raise_validate_error(rhs, e_path=e_path, e_msg="not_string")

        try:
            int(rhs)
        except ValueError:
            self.raise_validate_error(rhs, e_path=e_path, e_msg="not_int_string")


class AnyUUID(BelieveBase):
    def validate(self, rhs: str, e_path: str = "") -> None:
        if not isinstance(rhs, str) or len(rhs) != 36:
            self.raise_validate_error(rhs, e_path=e_path, e_msg="invalid_uuid")
        try:
            uuid.UUID(rhs)
        except (TypeError, ValueError):
            self.raise_validate_error(rhs, e_path=e_path, e_msg="invalid_uuid")


class AnyIPV4(BelieveBase):
    def validate(self, rhs: str, e_path: str = "") -> None:
        if not isinstance(rhs, str):
            self.raise_validate_error(rhs, e_path=e_path, e_msg="invalid_ipv4")
        tokens = rhs.split(".")
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
    def validate(self, rhs: str, e_path: str = "") -> None:
        if not isinstance(rhs, str):
            self.raise_validate_error(rhs, e_path=e_path, e_msg="invalid_sha1")
        if len(rhs) != 40:
            self.raise_validate_error(rhs, e_path=e_path, e_msg="invalid_sha1")
        try:
            int(rhs, 16)
        except ValueError:
            self.raise_validate_error(rhs, e_path=e_path, e_msg="invalid_sha1")


class AnyJsonStr(BelieveBase):
    def __init__(self, json_obj: Union[Dict, List]) -> None:
        assert isinstance(json_obj, (dict, list))
        super().__init__(json_obj)
        self.__json_obj = json_obj

    def validate(self, rhs: str, e_path: str = "") -> None:
        if not isinstance(rhs, str):
            self.raise_validate_error(rhs, e_path=e_path, e_msg="not_string")
        try:
            obj = json.loads(rhs)
        except:
            self.raise_validate_error(rhs, e_path=e_path, e_msg="not_json_string")
        if obj != self.__json_obj:
            self.raise_validate_error(rhs, e_path=e_path, e_msg="mismatch_json_string")


class AnyUrl(BelieveBase):
    def __init__(self, url: str) -> None:
        super().__init__(url)
        self.__parsed_url = urlparse(url)

    def _normalize_query(self, query: str) -> str:
        return "&".join(sorted(query.split("&")))

    def _default_port(self, scheme: str) -> int:
        if scheme == "http":
            return 80
        elif scheme == "https":
            return 443

    def validate(self, rhs: str, e_path: str = "") -> None:
        if not isinstance(rhs, str):
            self.raise_validate_error(rhs, e_path=e_path, e_msg="not_string")

        o = urlparse(rhs)

        if self.__parsed_url.scheme != o.scheme:
            self.raise_validate_error(rhs, e_path=e_path, e_msg="mismatch_scheme")

        default_port = self._default_port(self.__parsed_url.scheme)

        if self.__parsed_url.username != o.username:
            self.raise_validate_error(rhs, e_path=e_path, e_msg="mismatch_username")

        if self.__parsed_url.password != o.password:
            self.raise_validate_error(rhs, e_path=e_path, e_msg="mismatch_password")

        if self.__parsed_url.hostname != o.hostname:
            self.raise_validate_error(rhs, e_path=e_path, e_msg="mismatch_hostname")

        if (self.__parsed_url.port or default_port) != (o.port or default_port):
            self.raise_validate_error(rhs, e_path=e_path, e_msg="mismatch_port")

        if self.__parsed_url.path != o.path:
            self.raise_validate_error(rhs, e_path=e_path, e_msg="mismatch_path")

        if self._normalize_query(self.__parsed_url.query) != self._normalize_query(
            o.query
        ):
            self.raise_validate_error(rhs, e_path=e_path, e_msg="mismatch_query")
