import pytest
from flytrap.parser_exception import ParserException
from .string_parser import StringParser
from .until_parser import UntilParser

class TestUntilParser:
    def test_ok(self):
        p = UntilParser(StringParser("world"))
        (value, stream) = p.parse("helloworld")
        assert value == ("hello")
        assert stream == "world"

    def test_raise(self):
        p = UntilParser(StringParser("world"))
        e = ParserException(expect="world", actual="")
        with pytest.raises(ParserException, match=e.msg()):
             p.parse("hellohello")

    def test_raise_nothing(self):
        p = UntilParser(StringParser("world"))
        e = ParserException(expect="world", actual="")
        with pytest.raises(ParserException, match=e.msg()):
             p.parse("")



