import json
import unittest
import uuid
import os

from believe import BelieveMixin
from believe import validate
from believe import ValidateError


class BelieveTestCase(unittest.TestCase, BelieveMixin):

    def gen_sha1(self):
        return os.urandom(20).hex()

    def fail_validate_with(self, v1, v2, xss_unsafe_message, xss_safe_message=""):
        try:
            validate(v1, v2)
            self.fail()
        except ValidateError as e:
            print("xss_unsafe_message:", e.xss_unsafe_message())
            print("xss_safe_message:", e.xss_safe_message())
            self.assertEqual(str(e), xss_unsafe_message)
            self.assertEqual(e.xss_unsafe_message(), xss_unsafe_message)
            self.assertEqual(e.xss_safe_message(), xss_safe_message)

    def test_number_matcher__Almost_int(self):
        self.assertEqual("Almost(1)", str(self.Almost(1)))
        self.assertEqual(1, self.Almost(0))
        self.assertEqual(1, self.Almost(2))
        self.assertEqual(1, self.Almost(3))
        self.assertNotEqual(1, self.Almost(5))

        self.fail_validate_with(10, self.Almost(1), "[e_msg=not_in_range] 10 != Almost(1)", "[e_msg=not_in_range]")
        self.fail_validate_with(10, self.Almost(1, ts_range=2),
                                "[e_msg=not_in_range] 10 != Almost(1, ts_range=2)",
                                "[e_msg=not_in_range]")

    def test_number_matcher__Almost_float(self):
        self.assertEqual("Almost(1.1)", str(self.Almost(1.1)))
        self.assertEqual(1.1, self.Almost(0))
        self.assertEqual(1.1, self.Almost(2))
        self.assertEqual(1.1, self.Almost(3))
        self.assertNotEqual(1.1, self.Almost(5))

        self.fail_validate_with(10, self.Almost(1.1), "[e_msg=not_in_range] 10 != Almost(1.1)", "[e_msg=not_in_range]")
        self.fail_validate_with(10, self.Almost(1.1, ts_range=2.2),
                                "[e_msg=not_in_range] 10 != Almost(1.1, ts_range=2.2)",
                                "[e_msg=not_in_range]")

    def test_number_matcher__AnyInt(self):
        self.assertEqual("AnyInt(min_value=1, max_value=2)", str(self.AnyInt(min_value=1, max_value=2)))
        self.assertEqual(1, self.AnyInt(min_value=1, max_value=2))
        self.assertEqual(2, self.AnyInt(min_value=1, max_value=2))
        self.assertNotEqual(0, self.AnyInt(min_value=1, max_value=2))
        self.assertNotEqual(3, self.AnyInt(min_value=1, max_value=2))
        self.assertNotEqual(None, self.AnyInt(min_value=1, max_value=2))
        self.assertNotEqual("None", self.AnyInt(min_value=1, max_value=2))

        self.fail_validate_with(3, self.AnyInt(min_value=1, max_value=2),
                                "[e_msg=value_too_large: 3 > 2] 3 != AnyInt(min_value=1, max_value=2)",
                                "[e_msg=value_too_large: 3 > 2]")
        self.fail_validate_with(0, self.AnyInt(min_value=1, max_value=2),
                                "[e_msg=value_too_small: 0 < 1] 0 != AnyInt(min_value=1, max_value=2)",
                                "[e_msg=value_too_small: 0 < 1]")

    def test_number_matcher__AnyFloat(self):
        self.assertEqual("AnyFloat(min_value=1.0, max_value=2.0)", str(self.AnyFloat(min_value=1.0, max_value=2.0)))
        self.assertEqual(1.0, self.AnyFloat(min_value=1.0, max_value=2.0))
        self.assertEqual(2.0, self.AnyFloat(min_value=1.0, max_value=2.0))
        self.assertNotEqual(0.0, self.AnyFloat(min_value=1.0, max_value=2.0))
        self.assertNotEqual(3.0, self.AnyFloat(min_value=1.0, max_value=2.0))
        self.assertNotEqual(None, self.AnyFloat(min_value=1.0, max_value=2.0))
        self.assertNotEqual("None", self.AnyFloat(min_value=1.0, max_value=2.0))

        self.fail_validate_with(3.0, self.AnyFloat(min_value=1.0, max_value=2.0),
                                "[e_msg=value_too_large: 3.0 > 2.0] 3.0 != AnyFloat(min_value=1.0, max_value=2.0)",
                                "[e_msg=value_too_large: 3.0 > 2.0]")
        self.fail_validate_with(0.0, self.AnyFloat(min_value=1.0, max_value=2.0),
                                "[e_msg=value_too_small: 0.0 < 1.0] 0.0 != AnyFloat(min_value=1.0, max_value=2.0)",
                                "[e_msg=value_too_small: 0.0 < 1.0]")

    def test_str_matcher__AnyIPV4(self):
        self.assertEqual("AnyIPV4()", str(self.AnyIPV4()))
        self.assertEqual('192.168.1.1', self.AnyIPV4())
        self.assertNotEqual('127.0.0', self.AnyIPV4())
        self.assertNotEqual('0.0.0.x', self.AnyIPV4())
        self.assertNotEqual(12345, self.AnyIPV4())

        self.fail_validate_with(12345, self.AnyIPV4(),
                                "[e_msg=invalid_ipv4] 12345 != AnyIPV4()", "[e_msg=invalid_ipv4]")

    def test_str_matcher__AnySHA1(self):
        self.assertEqual("AnySHA1()", str(self.AnySHA1()))
        self.assertEqual(self.gen_sha1(), self.AnySHA1())
        self.assertNotEqual('123', self.AnySHA1())
        self.assertNotEqual(123, self.AnySHA1())

        self.fail_validate_with('123', self.AnySHA1(),
                                "[e_msg=invalid_sha1] '123' != AnySHA1()", "[e_msg=invalid_sha1]")

    def test_str_matcher__AnyUUID(self):
        self.assertEqual("AnyUUID()", str(self.AnyUUID()))
        self.assertEqual(str(uuid.uuid4()), self.AnyUUID())
        self.assertNotEqual(None, self.AnyUUID())
        self.assertNotEqual(10, self.AnyUUID())
        self.assertNotEqual(uuid.uuid4().bytes_le.hex(), self.AnyUUID())

        self.fail_validate_with(10, self.AnyUUID(),
                                "[e_msg=invalid_uuid] 10 != AnyUUID()",
                                "[e_msg=invalid_uuid]")

    def test_str_matcher__AnyIntStr(self):
        self.assertEqual("AnyIntStr()", str(self.AnyIntStr()))
        self.assertEqual(str(1), self.AnyIntStr())
        self.assertNotEqual(None, self.AnyIntStr())
        self.assertNotEqual(10, self.AnyIntStr())
        self.assertNotEqual('invalid', self.AnyIntStr())

        self.fail_validate_with(10, self.AnyIntStr(),
                                "[e_msg=not_string] 10 != AnyIntStr()",
                                "[e_msg=not_string]")
        self.fail_validate_with("NotInt", self.AnyIntStr(),
                                "[e_msg=not_int_string] 'NotInt' != AnyIntStr()",
                                "[e_msg=not_int_string]")

    def test_str_matcher__AnyStr(self):
        self.assertEqual("AnyStr()", str(self.AnyStr()))
        self.assertEqual("AnyStr(min_len=1, max_len=2)", str(self.AnyStr(min_len=1, max_len=2)))
        self.assertEqual(str(uuid.uuid4()), self.AnyStr())
        self.assertNotEqual(None, self.AnyStr())
        self.assertNotEqual(10, self.AnyStr())
        self.assertNotEqual("123", self.AnyStr(min_len=4))
        self.assertNotEqual("123", self.AnyStr(max_len=2))
        self.fail_validate_with(10, self.AnyStr(), "[e_msg=not_string] 10 != AnyStr()", "[e_msg=not_string]")
        self.fail_validate_with("123", self.AnyStr(min_len=4),
                                "[e_msg=string_too_short: 3 < 4] '123' != AnyStr(min_len=4)",
                                "[e_msg=string_too_short: 3 < 4]")
        self.fail_validate_with("123", self.AnyStr(max_len=2),
                                "[e_msg=string_too_long: 3 > 2] '123' != AnyStr(max_len=2)",
                                "[e_msg=string_too_long: 3 > 2]")

    def test_list_matcher__OneOf(self):
        self.assertEqual("OneOf(1, 2, 3)", str(self.OneOf(1, 2, 3)))
        self.assertEqual(1, self.OneOf(1, 2, 3))
        self.assertNotEqual(4, self.OneOf(1, 2, 3))

        self.fail_validate_with(4, self.OneOf([2, 1, 3]),
                                "[e_msg=invalid_argument] 4 != OneOf([2, 1, 3])",
                                "[e_msg=invalid_argument]")

    def test_list_matcher__AnyOrder(self):
        self.assertEqual("AnyOrder([2, 1, 1])", str(self.AnyOrder([2, 1, 1])))
        self.assertEqual([1, 1, 2], self.AnyOrder([2, 1, 1]))
        self.assertEqual([1, 2, 3], self.AnyOrder([2, 1, 3]))
        self.assertNotEqual([1, 2], self.AnyOrder([2, 1, 3]))

        self.fail_validate_with([1, 2], self.AnyOrder([2, 1, 3]),
                                "[e_msg=different_length] [1, 2] != AnyOrder([2, 1, 3])",
                                "[e_msg=different_length]")

    def test_list_matcher__ListOf(self):
        self.assertEqual("ListOf(1)", str(self.ListOf(1)))
        self.assertEqual([], self.ListOf(1))
        self.assertEqual([1, 1, 1], self.ListOf(1))
        self.assertNotEqual([1, 2, 3], self.ListOf(1))
        self.assertEqual([], self.ListOf(1))
        self.assertNotEqual((), self.ListOf(1))
        self.assertNotEqual("aaa", self.ListOf("a"))
        self.assertEqual(["a", "a"], self.ListOf("a"))

        self.fail_validate_with([1, 2, 3], self.ListOf(1),
                                "[e_path=$.1] 2 != 1",
                                "[e_path=$.1]")

        # dict
        self.assertEqual([{"name": "123"}, {"name": "456"}], self.ListOf({"name": self.Any(str)}))
        self.assertNotEqual([{"name": "123"}, {"name": "456", "type": "789"}], self.ListOf({"name": self.Any(str)}))

        self.fail_validate_with([{}], self.ListOf({"name": self.Any(str)}),
                                "[e_path=$.0] {} != {'name': Any(str)}",
                                "[e_path=$.0]")

        # n_item
        self.assertNotEqual(["a", "a"], self.ListOf("a", n_item=1))
        self.assertEqual(["a", "a"], self.ListOf("a", n_item=2))
        self.fail_validate_with([1], self.ListOf(1, n_item=2),
                                "[e_msg=mismatch_item_count: 1 != 2] [1] != ListOf(1, n_item=2)",
                                "[e_msg=mismatch_item_count: 1 != 2]")

        # min_item
        self.assertNotEqual([], self.ListOf("a", min_item=1))
        self.assertEqual(["a"], self.ListOf("a", min_item=1))
        self.assertEqual(["a", "a"], self.ListOf("a", min_item=1))
        self.fail_validate_with([1], self.ListOf(1, min_item=2),
                                "[e_msg=too_few_items: 1 < 2] [1] != ListOf(1, min_item=2)",
                                "[e_msg=too_few_items: 1 < 2]")

        # max_item
        self.assertEqual([], self.ListOf("a", max_item=1))
        self.assertEqual(["a"], self.ListOf("a", max_item=1))
        self.assertNotEqual(["a", "a"], self.ListOf("a", max_item=1))
        self.fail_validate_with([1], self.ListOf(1, max_item=0),
                                "[e_msg=too_many_items: 1 > 0] [1] != ListOf(1, max_item=0)",
                                "[e_msg=too_many_items: 1 > 0]")

    def test_dict_matcher__Dict(self):
        exp_dict = self.Dict({"req1": 1,
                              "req2": 2,
                              "opt1": self.Optional(1),
                              "opt2": self.Optional(2)})

        self.assertEqual("Dict({'req1': 1, 'req2': 2, 'opt1': Optional(1), 'opt2': Optional(2)})", str(exp_dict))

        self.assertEqual(exp_dict, {"req1": 1, "req2": 2, "opt1": 1, "opt2": 2})
        self.assertEqual(exp_dict, {"req1": 1, "req2": 2, "opt1": 1})
        self.assertEqual(exp_dict, {"req1": 1, "req2": 2, "opt2": 2})
        self.assertEqual(exp_dict, {"req1": 1, "req2": 2})

        self.assertNotEqual(exp_dict, {"req1": 1})
        self.assertNotEqual(exp_dict, {"req1": 1, "opt1": 1})
        self.assertNotEqual(exp_dict, {"req1": 1, "req2": 2, "opt3": 3})
        self.assertNotEqual(exp_dict, {"req1": 1, "req2": 2, "req3": 3})

        self.fail_validate_with({}, self.Dict({"req1": 1}),
                                "[e_msg=missing_required_field: req1] {} != Dict({'req1': 1})",
                                "[e_msg=missing_required_field: req1]")

        self.fail_validate_with({"req1": 1}, self.Dict({}),
                                "[e_msg=unknown_field] [e_unsafe_msg=unknown_field: req1] {'req1': 1} != Dict({})",
                                "[e_msg=unknown_field]",
                                )

        self.fail_validate_with({"req1": {}}, self.Dict({"req1": {"req11": 1}}),
                                "[e_path=$.req1] {} != {'req11': 1}",
                                "[e_path=$.req1]")

    def test_dict_matcher__DictStr(self):
        exp_dict = self.DictStr({"req1": 1,
                                 "req2": 2,
                                 "opt1": self.Optional(1),
                                 "opt2": self.Optional(2)})

        self.assertEqual("DictStr({'req1': 1, 'req2': 2, 'opt1': Optional(1), 'opt2': Optional(2)})", str(exp_dict))

        self.assertEqual(exp_dict, '{"req1": 1, "req2": 2, "opt1": 1, "opt2": 2}')
        self.assertEqual(exp_dict, '{"req1": 1, "req2": 2, "opt1": 1}')
        self.assertEqual(exp_dict, '{"req1": 1, "req2": 2, "opt2": 2}')
        self.assertEqual(exp_dict, '{"req1": 1, "req2": 2}')
        self.assertEqual(exp_dict, b'{"req1": 1, "req2": 2}')

        self.assertNotEqual(exp_dict, '{"req1": 1}')
        self.assertNotEqual(exp_dict, '{"req1": 1, "opt1": 1}')
        self.assertNotEqual(exp_dict, '{"req1": 1, "req2": 2, "opt3": 3}')
        self.assertNotEqual(exp_dict, '{"req1": 1, "req2": 2, "req3": 3}')

        self.fail_validate_with({}, self.DictStr({"req1": 1}),
                                "[e_msg=not_dict_string] {} != DictStr({'req1': 1})",
                                "[e_msg=not_dict_string]")

        self.fail_validate_with('{}', self.DictStr({"req1": 1}),
                                "[e_msg=missing_required_field: req1] {} != DictStr({'req1': 1})",
                                "[e_msg=missing_required_field: req1]")

        self.fail_validate_with('{"req1": 1}', self.DictStr({}),
                                "[e_msg=unknown_field] [e_unsafe_msg=unknown_field: req1] {'req1': 1} != DictStr({})",
                                "[e_msg=unknown_field]",
                                )

        self.fail_validate_with('{"req1": {}}', self.DictStr({"req1": {"req11": 1}}),
                                "[e_path=$.req1] {} != {'req11': 1}",
                                "[e_path=$.req1]")

    def test_dict_matcher__DictOf(self):
        exp_dict = self.DictOf(self.AnyStr(), self.AnyStr())

        self.assertEqual("DictOf(AnyStr(), AnyStr())", str(exp_dict))

        self.assertEqual(exp_dict, {"1": "1"})
        self.assertEqual(exp_dict, {})
        self.assertNotEqual(exp_dict, {"1": 1})

        self.fail_validate_with({}, self.DictOf(self.AnyStr(), self.AnyStr(), n_item=1),
                                "[e_msg=mismatch_item_count: 0 != 1] {} != DictOf(AnyStr(), AnyStr(), n_item=1)",
                                "[e_msg=mismatch_item_count: 0 != 1]")

        self.fail_validate_with({}, self.DictOf(self.AnyStr(), self.AnyStr(), min_item=1),
                                "[e_msg=too_few_items: 0 < 1] {} != DictOf(AnyStr(), AnyStr(), min_item=1)",
                                "[e_msg=too_few_items: 0 < 1]")

        self.fail_validate_with({"1": "1", "2": "2"}, self.DictOf(self.AnyStr(), self.AnyStr(), max_item=1),
                                "[e_msg=too_many_items: 2 > 1] {'1': '1', '2': '2'} != DictOf(AnyStr(), AnyStr(), max_item=1)",
                                "[e_msg=too_many_items: 2 > 1]")

        self.fail_validate_with({"req1": 1}, self.DictOf(self.AnyStr(), self.AnyStr()),
                                "[e_path=$.req1] [e_msg=not_string] 1 != AnyStr()",
                                "[e_path=$.req1] [e_msg=not_string]",
                                )

        self.fail_validate_with({1: "req1"}, self.DictOf(self.AnyStr(), self.AnyStr()),
                                "[e_path=$.1] [e_msg=not_string] 1 != AnyStr()",
                                "[e_path=$.1] [e_msg=not_string]",
                                )

        self.fail_validate_with([], self.DictOf(self.AnyStr(), self.AnyStr()),
                                "[e_msg=not_dict] [] != DictOf(AnyStr(), AnyStr())",
                                "[e_msg=not_dict]")

    def test_other_matcher__Any(self):
        self.assertEqual('Any()', str(self.Any()))
        self.assertEqual('Any(str)', str(self.Any(str)))
        self.assertEqual('Any(str, bytes)', str(self.Any(str, bytes)))
        self.assertEqual('1', self.Any(str))
        self.assertEqual(1, self.Any(int))
        self.assertNotEqual(None, self.Any(str))
        self.assertNotEqual('1', self.Any(int))
        self.assertEqual(None, self.Any())

        self.fail_validate_with('1', self.Any(int), "[e_msg=invalid_param] '1' != Any(int)", "[e_msg=invalid_param]")

    def test_other_matcher__Not(self):
        self.assertEqual('Not(1)', str(self.Not(1)))
        self.assertEqual(1, self.Not(0))
        self.assertNotEqual(0, self.Not(0))

        self.fail_validate_with(0, self.Not(0), "[e_msg=invalid_param] 0 != Not(0)", "[e_msg=invalid_param]")

    def test_other_matcher__Nullable(self):
        self.assertEqual('Nullable(1)', str(self.Nullable(1)))
        self.assertEqual(1, self.Nullable(1))
        self.assertEqual(None, self.Nullable(1))
        self.assertNotEqual(2, self.Nullable(1))

        self.fail_validate_with(2, self.Nullable(1), "[e_msg=invalid_param] 2 != Nullable(1)", "[e_msg=invalid_param]")

    def test_BelieveMixin__complex(self):
        exp_dict = self.Dict({
            "company_info": self.Optional(
                self.ListOf(
                    self.Dict({
                        "attr": self.Dict({
                            "name": self.Any(str),
                            "id": self.Any(int)
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
