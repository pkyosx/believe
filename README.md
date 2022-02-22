# Believe
## Motivation
* We often need to compare expected results in our test. It's lousy to check expected result under the following way.

```
import uuid

class TestCases:
    def test_user(self):
        user = {
                    "name": "John",
                    "id": "30e7b1e2-4c80-44c2-8fe5-23bad73ed8f2"
                }
        assert set("name", "id") == set(user.keys())
        assert isinstance(user["name"], str)
        assert 0 < len(user["name"]) < 64
        assert isinstance(user["id"], str)
        uuid.UUID(user["id"])
```

* By using this package, we could compare the value using the following way. It's easier to read and maintain.

```
import believe as B

class TestCases:
    def test_user(self):
        user = {
                    "name": "John",
                    "id": "30e7b1e2-4c80-44c2-8fe5-23bad73ed8f2"
                }
        assert user == {"name": B.AnyStr(min_len=1, max_len=63),
                        "id": B.AnyUUID()}

```

* If you are looking for web framework input validation, I suggest use [FastAPI](https://fastapi.tiangolo.com/). It properly integrate with openapi as well.

## Installation
```
pip install believe
```

## Basic usage
```
import believe as B
import time

# Match any string
assert B.AnyStr() == "any_str"

# Match string length >= 1 and <= 10
assert B.AnyStr(min_len=1, max_len=10) == "a"

# Match any string that can be converted to int
assert B.AnyIntStr() == "123"

# Match any UUID format string
assert B.AnyUUID() == "732c0743-2638-47d5-902d-0daa3080348b"

# Match any sha1 string
assert B.AnySHA1() == "b130c4b97d0640eaf3f45f7360a5b4dbbf561f58"

# Match any IPv4 string
assert B.AnyIPV4() == "1.2.3.4"

# Match integer that is >=1 and <= 10
assert B.AnyInt(min_value=1, max_value=10) == 5

# Match any float that is >= 1.0 and <= 10.0
assert B.AnyFloat(min_value=1.0, max_value=10.0) == 5.0 # 1.0 <= X <= 10.0

# Match if values is "one" or "two"
assert B.OneOf("one", "two") == "one"

# Sometimes we don't care about the order, we can use AnyOrder
assert B.AnyOrder([1, 2, 3]) == [2, 1, 3]

# Sometimes we assign value as timestamp but test cases takes more than 1 sec
# We can use almost to accept a range of values
assert B.Almost(time.time(), ts_range=3) == time.time() # Allow 3 sec gap

# If we allow None or any string
assert B.Nullable(B.AnyStr()) == None
assert B.Nullable(B.AnyStr()) == "123"

# Only check type
assert B.Any(bytes) == b'123'

# Reverse check result, anything but "A" or "B"
assert B.Not(B.OneOf("A", "B")) == "C"

# Match list
assert B.ListOf(B.AnyStr()) == ["A", "B", "C"]
assert B.ListOf(B.AnyStr(), n_item=3) == ["A", "B", "C"]  # exact 3 items
assert B.ListOf(B.AnyStr(), min_item=1) == ["A", "B", "C"]  # >= 1 items
assert B.ListOf(B.AnyStr(), max_item=5) == ["A", "B", "C"]  # <= 5 items
```

## Advance Usage
```
# If we don't want to use json.load('{"foo": "bar"}') == {"foo": "bar"}, we can use the following way
assert B.AnyJsonStr({"foo": "bar"}) == '{"foo": "bar"}'

# We can use AnyUrl to compare the normalized url
# 1. We can compare one with default port and one without, they are identical
assert B.AnyUrl("https://foo.com/") == "https://foo.com:443/"
assert B.AnyUrl("http://foo.com/") == "http://foo.com:80/"
# 2. We can ignore the order in query string
assert B.AnyUrl("https://foo.com/bar?p1=1&p2=2") == "https://foo.com/bar?p2=2&p1=1"

# We can use Dict to compare a dict with Optional field
assert B.Dict({"name": B.AnyStr(), "value": B.Optional(B.AnyStr())}) == {"name": "abc"}
assert B.Dict({"name": B.AnyStr(), "value": B.Optional(B.AnyStr())}) == {"name": "abc", "value": "def"}

# If key is a dynamic value, we can use DictOf(<key_matcher>, <value_matcher>)
# i.e. We want to match a dict with random uuid as key
assert B.DictOf(B.AnyUUID(), B.OneOf("ok", "fail")) == {"732c0743-2638-47d5-902d-0daa3080348b": "ok",
                                                        "5cfd50ba-c3d3-4fb7-b2fe-e9a6e039ad29": "fail"}
```

## Use Validate Function
```
# validate with error exception
import believe as B
validator = B.Dict({"name": B.AnyInt()})

B.validate(validator, {"name": "ken"})  # believe.error.ValidateError: [e_path=$.name] 'ken' != AnyInt()
```

## A Complex Example
```
import believe as B
import time

result_json = {"name": "john",
               "age": 32,
               "download_link": "https://download.server.com/?name=john&id=abc",
               "role": "admin",
               "address": "10.1.2.3",
               "updated_at": int(time.time()),
               "tags": ["admin", "john"]}

exp_result = B.Dict({"name": B.AnyStr(min_len=1, max_len=64),
                     "age": B.AnyInt(min_value=0, max_value=200),
                     "download_link": B.AnyUrl("https://download.server.com/?id=abc&name=john"),
                     "role": B.OneOf("admin", "user"),
                     "address": B.AnyIPV4(),
                     "updated_at": B.Almost(int(time.time())),
                     "tags": B.ListOf(B.AnyStr()),
                     "extra": B.Optional(B.Nullable(B.AnyStr()))})
B.validate(exp_result, result_json)
```
