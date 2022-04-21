from typing import Any, List


class ValidateError(Exception):
    def __init__(self, v1: Any, v2: Any, **kwargs: Any) -> None:
        self.v1 = repr(v1)
        self.v2 = repr(v2)
        self.kwargs = kwargs

    def kwargs_to_string(self, fields: List[str], with_v2: bool) -> str:
        result = []
        for k in fields:
            if self.kwargs.get(k):
                if k == "e_path":
                    result.append(f"[{k}=${self.kwargs[k]}]")
                else:
                    result.append(f"[{k}={self.kwargs[k]}]")
        if with_v2:
            result.append(f"{self.v2} != {self.v1}")
        return " ".join(result)

    def xss_unsafe_message(self) -> str:
        return self.kwargs_to_string(["e_path", "e_msg", "e_unsafe_msg"], True)

    def xss_safe_message(self) -> str:
        return self.kwargs_to_string(["e_path", "e_msg"], False)

    def __str__(self) -> str:
        return self.xss_unsafe_message()
