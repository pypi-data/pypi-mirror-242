import pytest
from .and_parser import AndParser
from .any_parser import AnyParser
from .parser_exception import ParserException
from .string_parser import StringParser

class TestAndParser:
    def test_ok(self):
        p = AndParser(StringParser("hello"), AnyParser())
        (value, stream) = p.parse("helloworld")
        assert value == ("hello", 'w')
        assert stream == "orld"

    def test_raise(self):
        p = AndParser(StringParser("hello"), AnyParser())
        e = ParserException(expect=["hello"], actual="world")
        with pytest.raises(ParserException, match=e.msg()):
             p.parse("worldhello")

