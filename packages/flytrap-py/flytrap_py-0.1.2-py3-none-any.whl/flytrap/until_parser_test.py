from .string_parser import StringParser
from .until_parser import UntilParser

class TestUntilParser:
    def test_ok(self):
        p = UntilParser(StringParser("world"))
        (value, stream) = p.parse("helloworld")
        assert value == ("hello")
        assert stream == "world"
