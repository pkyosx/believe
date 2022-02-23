import json
import unittest
import uuid
import os


import believe as B

class BaseClass:
    def gen_sha1(self):
        return os.urandom(20).hex()

    def fail_validate_with(self, v1, v2, xss_unsafe_message, xss_safe_message=""):
        try:
            B.validate(v1, v2)
            assert not "should fail"
        except B.ValidateError as e:
            assert e.xss_safe_message() == xss_safe_message
            assert e.xss_unsafe_message() == xss_unsafe_message
            assert str(e) == xss_unsafe_message


class TestNumberMatcher(BaseClass):
    def test_number_matcher__Almost_int(self):
        assert "Almost(1)" == str(B.Almost(1))
        assert 1 == B.Almost(0)
        assert 1 == B.Almost(2)
        assert 1 == B.Almost(3)
        assert 1 != B.Almost(5)
        assert None != B.Almost(0)

        self.fail_validate_with(10, B.Almost(1),
                                "[e_msg=not_in_range] 10 != Almost(1)",
                                "[e_msg=not_in_range]")
        self.fail_validate_with(10, B.Almost(1, ts_range=2),
                                "[e_msg=not_in_range] 10 != Almost(1, ts_range=2)",
                                "[e_msg=not_in_range]")

    def test_number_matcher__Almost_float(self):
        assert "Almost(1.1)" == str(B.Almost(1.1))
        assert 1.1 == B.Almost(0)
        assert 1.1 == B.Almost(2)
        assert 1.1 == B.Almost(3)
        assert 1.1 != B.Almost(5)

        self.fail_validate_with(10, B.Almost(1.1),
                                "[e_msg=not_in_range] 10 != Almost(1.1)",
                                "[e_msg=not_in_range]")
        self.fail_validate_with(10, B.Almost(1.1, ts_range=2.2),
                                "[e_msg=not_in_range] 10 != Almost(1.1, ts_range=2.2)",
                                "[e_msg=not_in_range]")

    def test_number_matcher__AnyInt(self):
        assert "AnyInt(min_value=1, max_value=2)" == str(B.AnyInt(min_value=1, max_value=2))
        assert 1 == B.AnyInt(min_value=1, max_value=2)
        assert 2 == B.AnyInt(min_value=1, max_value=2)
        assert 0 != B.AnyInt(min_value=1, max_value=2)
        assert 3 != B.AnyInt(min_value=1, max_value=2)
        assert None != B.AnyInt(min_value=1, max_value=2)
        assert "None" != B.AnyInt(min_value=1, max_value=2)

        self.fail_validate_with(3, B.AnyInt(min_value=1, max_value=2),
                                "[e_msg=value_too_large: 3 > 2] 3 != AnyInt(min_value=1, max_value=2)",
                                "[e_msg=value_too_large: 3 > 2]")
        self.fail_validate_with(0, B.AnyInt(min_value=1, max_value=2),
                                "[e_msg=value_too_small: 0 < 1] 0 != AnyInt(min_value=1, max_value=2)",
                                "[e_msg=value_too_small: 0 < 1]")

    def test_number_matcher__AnyFloat(self):
        assert "AnyFloat(min_value=1.0, max_value=2.0)" ==  str(B.AnyFloat(min_value=1.0, max_value=2.0))
        assert 1.0 == B.AnyFloat(min_value=1.0, max_value=2.0)
        assert 2.0 == B.AnyFloat(min_value=1.0, max_value=2.0)
        assert 0.0 != B.AnyFloat(min_value=1.0, max_value=2.0)
        assert 3.0 != B.AnyFloat(min_value=1.0, max_value=2.0)
        assert None != B.AnyFloat(min_value=1.0, max_value=2.0)
        assert "None" != B.AnyFloat(min_value=1.0, max_value=2.0)

        self.fail_validate_with(3.0, B.AnyFloat(min_value=1.0, max_value=2.0),
                                "[e_msg=value_too_large: 3.0 > 2.0] 3.0 != AnyFloat(min_value=1.0, max_value=2.0)",
                                "[e_msg=value_too_large: 3.0 > 2.0]")
        self.fail_validate_with(0.0, B.AnyFloat(min_value=1.0, max_value=2.0),
                                "[e_msg=value_too_small: 0.0 < 1.0] 0.0 != AnyFloat(min_value=1.0, max_value=2.0)",
                                "[e_msg=value_too_small: 0.0 < 1.0]")

class TestStrMatcher(BaseClass):

    def test_str_matcher__AnyIPV4(self):
        assert "AnyIPV4()" == str(B.AnyIPV4())
        assert '192.168.1.1' ==  B.AnyIPV4()
        assert '127.0.0' != B.AnyIPV4()
        assert '0.0.0.x' != B.AnyIPV4()
        assert "256.1.1.1" != B.AnyIPV4()
        assert 12345 != B.AnyIPV4()

        self.fail_validate_with(12345, B.AnyIPV4(),
                                "[e_msg=invalid_ipv4] 12345 != AnyIPV4()",
                                "[e_msg=invalid_ipv4]")

    def test_str_matcher__AnySHA1(self):
        assert "AnySHA1()" ==  str(B.AnySHA1())
        assert self.gen_sha1() == B.AnySHA1()
        assert '123' != B.AnySHA1()
        assert 123 != B.AnySHA1()
        assert "Z" + self.gen_sha1()[1:] != B.AnySHA1()

        self.fail_validate_with('123', B.AnySHA1(),
                                "[e_msg=invalid_sha1] '123' != AnySHA1()",
                                "[e_msg=invalid_sha1]")

    def test_str_matcher__AnyUUID(self):
        assert "AnyUUID()" == str(B.AnyUUID())
        assert str(uuid.uuid4()) == B.AnyUUID()
        assert None != B.AnyUUID()
        assert 10 != B.AnyUUID()
        assert "abc" != B.AnyUUID()

        self.fail_validate_with(10, B.AnyUUID(),
                                "[e_msg=invalid_uuid] 10 != AnyUUID()",
                                "[e_msg=invalid_uuid]")

    def test_str_matcher__AnyIntStr(self):
        assert "AnyIntStr()" == str(B.AnyIntStr())
        assert str(1) == B.AnyIntStr()
        assert None != B.AnyIntStr()
        assert 10 != B.AnyIntStr()
        assert 'invalid' !=  B.AnyIntStr()

        self.fail_validate_with(10, B.AnyIntStr(),
                                "[e_msg=not_string] 10 != AnyIntStr()",
                                "[e_msg=not_string]")
        self.fail_validate_with("NotInt", B.AnyIntStr(),
                                "[e_msg=not_int_string] 'NotInt' != AnyIntStr()",
                                "[e_msg=not_int_string]")

    def test_str_matcher__AnyStr(self):
        assert "AnyStr()" == str(B.AnyStr())
        assert "AnyStr(min_len=1, max_len=2)" == str(B.AnyStr(min_len=1, max_len=2))
        assert str(uuid.uuid4()) == B.AnyStr()
        assert None != B.AnyStr()
        assert 10 != B.AnyStr()
        assert "123" != B.AnyStr(min_len=4)
        assert "123" != B.AnyStr(max_len=2)

        self.fail_validate_with(10, B.AnyStr(), "[e_msg=not_string] 10 != AnyStr()", "[e_msg=not_string]")
        self.fail_validate_with("123", B.AnyStr(min_len=4),
                                "[e_msg=string_too_short: 3 < 4] '123' != AnyStr(min_len=4)",
                                "[e_msg=string_too_short: 3 < 4]")
        self.fail_validate_with("123", B.AnyStr(max_len=2),
                                "[e_msg=string_too_long: 3 > 2] '123' != AnyStr(max_len=2)",
                                "[e_msg=string_too_long: 3 > 2]")

    def test_str_matcher__AnyJsonStr(self):
        assert "AnyJsonStr({})" == str(B.AnyJsonStr({}))
        assert '{"foo": "bar", "bar": "foo"}' == B.AnyJsonStr({"foo": "bar", "bar": "foo"})

        self.fail_validate_with(b"{}", B.AnyJsonStr({}),
                               "[e_msg=not_string] b'{}' != AnyJsonStr({})",
                               "[e_msg=not_string]")
        self.fail_validate_with("{", B.AnyJsonStr({}),
                               "[e_msg=not_json_string] '{' != AnyJsonStr({})",
                               "[e_msg=not_json_string]")
        self.fail_validate_with("[]", B.AnyJsonStr({}),
                               "[e_msg=mismatch_json_string] '[]' != AnyJsonStr({})",
                               "[e_msg=mismatch_json_string]")

    def test_str_matcher__AnyJsonStr(self):
        assert "AnyJsonStr({})" == str(B.AnyJsonStr({}))
        assert '{"foo": "bar", "bar": "foo"}' == B.AnyJsonStr({"foo": "bar", "bar": "foo"})

        self.fail_validate_with(b"{}", B.AnyJsonStr({}),
                               "[e_msg=not_string] b'{}' != AnyJsonStr({})",
                               "[e_msg=not_string]")
        self.fail_validate_with("{", B.AnyJsonStr({}),
                               "[e_msg=not_json_string] '{' != AnyJsonStr({})",
                               "[e_msg=not_json_string]")
        self.fail_validate_with("[]", B.AnyJsonStr({}),
                               "[e_msg=mismatch_json_string] '[]' != AnyJsonStr({})",
                               "[e_msg=mismatch_json_string]")

    def test_str_matcher__AnyUrl(self):
        assert "AnyUrl(https://example.com)" == str(B.AnyUrl("https://example.com"))
        assert "https://example.com" == B.AnyUrl("https://example.com")

        # test default port
        assert "https://example.com:443" == B.AnyUrl("https://example.com")
        assert "http://example.com:80" == B.AnyUrl("http://example.com")

        # test query
        assert "https://example.com/path?q1=1&q2=2" == B.AnyUrl("https://example.com/path?q2=2&q1=1")

        self.fail_validate_with(b"https://example.com", B.AnyUrl("https://example.com"),
                               "[e_msg=not_string] b'https://example.com' != AnyUrl(https://example.com)",
                               "[e_msg=not_string]")

        self.fail_validate_with("http://example.com", B.AnyUrl("https://example.com"),
                               "[e_msg=mismatch_scheme] 'http://example.com' != AnyUrl(https://example.com)",
                               "[e_msg=mismatch_scheme]")

        self.fail_validate_with("https://user@example.com", B.AnyUrl("https://example.com"),
                               "[e_msg=mismatch_username] 'https://user@example.com' != AnyUrl(https://example.com)",
                               "[e_msg=mismatch_username]")

        self.fail_validate_with("https://user:pass@example.com", B.AnyUrl("https://user@example.com"),
                               "[e_msg=mismatch_password] 'https://user:pass@example.com' != AnyUrl(https://user@example.com)",
                               "[e_msg=mismatch_password]")

        self.fail_validate_with("https://foo.com", B.AnyUrl("https://example.com"),
                               "[e_msg=mismatch_hostname] 'https://foo.com' != AnyUrl(https://example.com)",
                               "[e_msg=mismatch_hostname]")

        self.fail_validate_with("https://example.com:8888", B.AnyUrl("https://example.com"),
                               "[e_msg=mismatch_port] 'https://example.com:8888' != AnyUrl(https://example.com)",
                               "[e_msg=mismatch_port]")

        self.fail_validate_with("https://example.com/abc", B.AnyUrl("https://example.com/def"),
                               "[e_msg=mismatch_path] 'https://example.com/abc' != AnyUrl(https://example.com/def)",
                               "[e_msg=mismatch_path]")

        self.fail_validate_with("https://example.com/foo?bar=1", B.AnyUrl("https://example.com/foo?bar=2"),
                               "[e_msg=mismatch_query] 'https://example.com/foo?bar=1' != AnyUrl(https://example.com/foo?bar=2)",
                               "[e_msg=mismatch_query]")


class TestListMatcher(BaseClass):

    def test_list_matcher__OneOf(self):
        assert "OneOf(1, 2, 3)" == str(B.OneOf(1, 2, 3))
        assert 1 == B.OneOf(1, 2, 3)
        assert 4 != B.OneOf(1, 2, 3)

        self.fail_validate_with(4, B.OneOf([2, 1, 3]),
                                "[e_msg=invalid_argument] 4 != OneOf([2, 1, 3])",
                                "[e_msg=invalid_argument]")

    def test_list_matcher__AnyOrder(self):
        assert "AnyOrder([2, 1, 1])" == str(B.AnyOrder([2, 1, 1]))
        assert [1, 1, 2] == B.AnyOrder([2, 1, 1])
        assert [1, 2, 3] == B.AnyOrder([2, 1, 3])
        assert [1, 2] != B.AnyOrder([2, 1, 3])
        assert [1, 2, 3] != B.AnyOrder([2, 1])

        self.fail_validate_with([1, 2], B.AnyOrder([2, 1, 3]),
                                "[e_msg=different_length] [1, 2] != AnyOrder([2, 1, 3])",
                                "[e_msg=different_length]")

    def test_list_matcher__ListOf(self):
        assert "ListOf(1)" == str(B.ListOf(1))
        assert [] == B.ListOf(1)
        assert [1, 1, 1] == B.ListOf(1)
        assert [1, 2, 3] != B.ListOf(1)
        assert [] == B.ListOf(1)
        assert () != B.ListOf(1)
        assert "aaa" != B.ListOf("a")
        assert ["a", "a"] == B.ListOf("a")

        self.fail_validate_with([1, 2, 3], B.ListOf(1),
                                "[e_path=$.1] 2 != 1",
                                "[e_path=$.1]")

        # dict
        assert [{"name": "123"}, {"name": "456"}] == B.ListOf({"name": B.Any(str)})
        assert [{"name": "123"}, {"name": "456", "type": "789"}] != B.ListOf({"name": B.Any(str)})

        self.fail_validate_with([{}], B.ListOf({"name": B.Any(str)}),
                                "[e_path=$.0] {} != {'name': Any(str)}",
                                "[e_path=$.0]")

        # n_item
        assert ["a", "a"] != B.ListOf("a", n_item=1)
        assert ["a", "a"] == B.ListOf("a", n_item=2)

        self.fail_validate_with([1], B.ListOf(1, n_item=2),
                                "[e_msg=mismatch_item_count: 1 != 2] [1] != ListOf(1, n_item=2)",
                                "[e_msg=mismatch_item_count: 1 != 2]")

        # min_item
        assert [] != B.ListOf("a", min_item=1)
        assert ["a"] == B.ListOf("a", min_item=1)
        assert ["a", "a"] == B.ListOf("a", min_item=1)

        self.fail_validate_with([1], B.ListOf(1, min_item=2),
                                "[e_msg=too_few_items: 1 < 2] [1] != ListOf(1, min_item=2)",
                                "[e_msg=too_few_items: 1 < 2]")

        # max_item
        assert [] == B.ListOf("a", max_item=1)
        assert ["a"] == B.ListOf("a", max_item=1)
        assert ["a", "a"] != B.ListOf("a", max_item=1)

        self.fail_validate_with([1], B.ListOf(1, max_item=0),
                                "[e_msg=too_many_items: 1 > 0] [1] != ListOf(1, max_item=0)",
                                "[e_msg=too_many_items: 1 > 0]")

class TestDictMatcher(BaseClass):

    def test_dict_matcher__Dict(self):
        exp_dict = B.Dict({"req1": 1,
                           "req2": 2,
                           "opt1": B.Optional(1),
                           "opt2": B.Optional(2)})

        assert "Dict({'req1': 1, 'req2': 2, 'opt1': Optional(1), 'opt2': Optional(2)})" == str(exp_dict)

        assert exp_dict == {"req1": 1, "req2": 2, "opt1": 1, "opt2": 2}
        assert exp_dict == {"req1": 1, "req2": 2, "opt1": 1}
        assert exp_dict == {"req1": 1, "req2": 2, "opt2": 2}
        assert exp_dict == {"req1": 1, "req2": 2}

        assert exp_dict != None
        assert exp_dict != {"req1": 1}
        assert exp_dict != {"req1": 1, "opt1": 1}
        assert exp_dict != {"req1": 1, "req2": 2, "opt3": 3}
        assert exp_dict != {"req1": 1, "req2": 2, "req3": 3}

        self.fail_validate_with({}, B.Dict({"req1": 1}),
                                "[e_msg=missing_required_field: req1] {} != Dict({'req1': 1})",
                                "[e_msg=missing_required_field: req1]")

        self.fail_validate_with({"req1": 1}, B.Dict({}),
                                "[e_msg=unknown_field] [e_unsafe_msg=unknown_field: req1] {'req1': 1} != Dict({})",
                                "[e_msg=unknown_field]",
                                )

        self.fail_validate_with({"req1": {}}, B.Dict({"req1": {"req11": 1}}),
                                "[e_path=$.req1] {} != {'req11': 1}",
                                "[e_path=$.req1]")

    def test_dict_matcher__DictOf(self):
        exp_dict = B.DictOf(B.AnyStr(), B.AnyStr())

        assert "DictOf(AnyStr(), AnyStr())" == str(exp_dict)

        assert exp_dict == {"1": "1"}
        assert exp_dict == {}
        assert exp_dict != {"1": 1}

        self.fail_validate_with({}, B.DictOf(B.AnyStr(), B.AnyStr(), n_item=1),
                                "[e_msg=mismatch_item_count: 0 != 1] {} != DictOf(AnyStr(), AnyStr(), n_item=1)",
                                "[e_msg=mismatch_item_count: 0 != 1]")

        self.fail_validate_with({}, B.DictOf(B.AnyStr(), B.AnyStr(), min_item=1),
                                "[e_msg=too_few_items: 0 < 1] {} != DictOf(AnyStr(), AnyStr(), min_item=1)",
                                "[e_msg=too_few_items: 0 < 1]")

        self.fail_validate_with({"1": "1", "2": "2"}, B.DictOf(B.AnyStr(), B.AnyStr(), max_item=1),
                                "[e_msg=too_many_items: 2 > 1] {'1': '1', '2': '2'} != DictOf(AnyStr(), AnyStr(), max_item=1)",
                                "[e_msg=too_many_items: 2 > 1]")

        self.fail_validate_with({"req1": 1}, B.DictOf(B.AnyStr(), B.AnyStr()),
                                "[e_path=$.req1] [e_msg=not_string] 1 != AnyStr()",
                                "[e_path=$.req1] [e_msg=not_string]",
                                )

        self.fail_validate_with({1: "req1"}, B.DictOf(B.AnyStr(), B.AnyStr()),
                                "[e_path=$.1] [e_msg=not_string] 1 != AnyStr()",
                                "[e_path=$.1] [e_msg=not_string]",
                                )

        self.fail_validate_with([], B.DictOf(B.AnyStr(), B.AnyStr()),
                                "[e_msg=not_dict] [] != DictOf(AnyStr(), AnyStr())",
                                "[e_msg=not_dict]")


class TestOtherMatcher(BaseClass):

    def test_other_matcher__Any(self):
        assert 'Any()' == str(B.Any())
        assert 'Any(str)' == str(B.Any(str))
        assert 'Any(str, bytes)' == str(B.Any(str, bytes))
        assert '1' == B.Any(str)
        assert 1 == B.Any(int)
        assert None != B.Any(str)
        assert '1' != B.Any(int)
        assert None == B.Any()

        self.fail_validate_with('1', B.Any(int),
                                "[e_msg=invalid_param] '1' != Any(int)",
                                "[e_msg=invalid_param]")

    def test_other_matcher__Not(self):
        assert 'Not(1)' == str(B.Not(1))
        assert 1 == B.Not(0)
        assert 0 != B.Not(0)

        self.fail_validate_with(0, B.Not(0),
                                "[e_msg=invalid_param] 0 != Not(0)",
                                "[e_msg=invalid_param]")

    def test_other_matcher__Nullable(self):
        assert 'Nullable(1)' == str(B.Nullable(1))
        assert 1 == B.Nullable(1)
        assert None == B.Nullable(1)
        assert 2 != B.Nullable(1)

        self.fail_validate_with(2, B.Nullable(1),
                                "[e_msg=invalid_param] 2 != Nullable(1)",
                                "[e_msg=invalid_param]")

    def test_BelieveMixin__complex(self):
        exp_dict = B.Dict({
            "company_info": B.Optional(
                B.ListOf(
                    B.Dict({
                        "attr": B.Dict({
                            "name": B.Any(str),
                            "id": B.Any(int)
                        })
                    })
                )
            )
        })

        self.fail_validate_with({"company_info": [{"attr": {"name": 123, "id": 123}}]}, exp_dict,
                                "[e_path=$.company_info.0.attr.name] [e_msg=invalid_param] 123 != Any(str)",
                                "[e_path=$.company_info.0.attr.name] [e_msg=invalid_param]")
        self.fail_validate_with({"company_info": [{"attr": {"name": "name"}}]}, exp_dict,
                                "[e_path=$.company_info.0.attr] [e_msg=missing_required_field: id] {'name': 'name'} != Dict({'name': Any(str), 'id': Any(int)})",
                                "[e_path=$.company_info.0.attr] [e_msg=missing_required_field: id]")
