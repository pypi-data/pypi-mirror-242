import pytest

from .digit_parser import DigitParser
from .many1_parser import Many1Parser
from .parser_exception import ParserException

class TestMany1Parser:
    def test_ok(self):
        p = Many1Parser(DigitParser())
        (value, stream) = p.parse("12hi")
        assert value == ["1","2"]
        assert stream == "hi"

    def test_nothing(self):
        p = Many1Parser(DigitParser())
        with pytest.raises(ParserException):
             p.parse("hi")

