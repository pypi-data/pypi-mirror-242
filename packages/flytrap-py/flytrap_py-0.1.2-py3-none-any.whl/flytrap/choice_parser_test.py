from .choice_parser import ChoiceParser
from .string_parser import StringParser

class TestChoiceParser:
    def test_ok(self):
        p = ChoiceParser(
                StringParser("hello1"),
                StringParser("hello2"),
                StringParser("hello3"),
                StringParser("hellow")
                )
        (value, stream) = p.parse("helloworld")
        assert value == "hellow"
        assert stream == "orld"
