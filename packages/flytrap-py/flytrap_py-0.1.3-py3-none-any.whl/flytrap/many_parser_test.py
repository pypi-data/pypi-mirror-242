from .digit_parser import DigitParser
from .many_parser import ManyParser

class TestManyParser:
    def test_ok(self):
        p = ManyParser(DigitParser())
        (value, stream) = p.parse("123hi")
        assert value == ["1","2","3"]
        assert stream == "hi"

    def test_nothing(self):
        p = ManyParser(DigitParser())
        (value, stream) = p.parse("hi")
        assert value == []
        assert stream == "hi"

