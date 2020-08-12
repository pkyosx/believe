import unittest
from believe import BelieveMixin

class BelieveTestCase(unittest.TestCase, BelieveMixin):
    def test_believe(self):
        self.assertEquals(self.AnyStr(), "abc")
        self.assertEquals(self.AnyIntStr(), "1")