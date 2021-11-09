# Believe
A python package for json validation. Useful for unit test.

# Installation
```
pip install believe
```

# Sample usage
```
import believe as B
import time

# String Match
assert B.AnyStr() == "any_str"
assert B.AnyIntStr() == "123"
assert B.AnyUUID() == "732c0743-2638-47d5-902d-0daa3080348b"
assert B.AnySHA1() == "b130c4b97d0640eaf3f45f7360a5b4dbbf561f58"
assert B.AnyIPV4() == "1.2.3.4"
assert B.AnyJsonStr({"foo": "bar"}) == '{"foo": "bar"}'
assert B.AnyUrl("https://foo.com/bar?p1=1&p2=2") == "https://foo.com:443/bar?p2=2&p1=1"

# Number Match
assert B.AnyInt(min_value=1) == 1 # X >= 1
assert B.AnyInt(max_value=10) == 10 # X <= 10
assert B.AnyInt(min_value=1, max_value=10) == 5 # 1 <= X <= 10
assert B.AnyFloat(min_value=1.0, max_value=10.0) == 5.0 # 1.0 <= X <= 10.0
assert B.Almost(time.time()) == time.time() # Allow some time gap

# List Match
assert B.OneOf("one", "two") == "one"
assert B.AnyOrder([1, 2, 3]) == [2, 1, 3]
assert B.ListOf({"type": B.OneOf("A", "B")}) == [{"type": "A"}, {"type": "B"}, {"type": "A"}]

# Dict Match
assert B.Dict({"name": B.AnyStr()}) == {"name": "ken"}
assert B.Dict({"name": B.AnyStr(), "value": B.Optional(B.AnyStr())}) == {"name": "ken"}
assert B.Dict({"name": B.AnyStr(), "value": B.Optional(B.AnyStr())}) == {"name": "ken", "value": "nek"}
assert B.DictOf(B.AnyUUID(), B.OneOf("ok", "fail")) == {"732c0743-2638-47d5-902d-0daa3080348b": "ok",
                                                        "5cfd50ba-c3d3-4fb7-b2fe-e9a6e039ad29": "fail"}

# Other Match
assert B.Nullable(B.AnyStr()) == None # Allow None
assert B.Any(bytes) == b'123' # only check type
assert B.Not(B.OneOf("A")) == "B"

# validate with error exception
validator = B.Dict({"name": B.AnyInt()})
B.validate(validator, {"name": "ken"})  # believe.error.ValidateError: [e_path=$.name] 'ken' != AnyInt()
```
