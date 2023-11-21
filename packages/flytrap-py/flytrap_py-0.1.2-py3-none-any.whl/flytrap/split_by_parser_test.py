import pytest

from flytrap.attempt_parser import attempt
from flytrap.space_parser import spaces
from .digit_parser import digit
from .many1_parser import many1
from .parser_exception import ParserException
from .split_by_parser import split_by
from .string_parser import string
from .token_parser import token

class TestSplitByParser:
    def test_ok(self):
        p = split_by(string("world"), digit())
        (value, stream) = p.parse("world1world2worldhello")
        assert value == ["world", "world", "world"]
        assert stream == "hello"

    def test_ok2(self):
        p = split_by(digit(), many1(attempt(spaces()).skip(token(",")).and_(attempt(spaces()))))
        (value, stream) = p.parse("1,   2   ,3   hi")
        assert value == ["1", "2", "3"]
        assert stream == "   hi"

    def test_not_devide(self):
        p = split_by(string("world"), digit())
        with pytest.raises(ParserException):
             p.parse("world1world2world3")

