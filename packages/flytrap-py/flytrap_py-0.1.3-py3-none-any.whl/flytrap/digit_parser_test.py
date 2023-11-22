import pytest
from .digit_parser import DigitParser, _digit
from .parser_exception import ParserException

class TestDigitParser:
    p = DigitParser()

    def test_ok(self):
        (value, stream) = self.p.parse("123hi")
        assert value == '1'
        assert stream == "23hi"

    def test_raise(self):
        e = ParserException(expect=_digit, actual="h")
        with pytest.raises(ParserException, match=e.msg()):
             self.p.parse("hi")

    def test_raise_nothing(self):
        e = ParserException(expect=_digit, actual="EOF")
        with pytest.raises(ParserException, match=e.msg()):
             self.p.parse("")



