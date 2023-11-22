from .digit_parser import DigitParser
from .skip_parser import SkipParser

class TestSkipParser:
    def test_ok(self):
        p = SkipParser(DigitParser(), DigitParser())
        (value, stream) = p.parse("123hi")
        assert value == "1"
        assert stream == "3hi"
