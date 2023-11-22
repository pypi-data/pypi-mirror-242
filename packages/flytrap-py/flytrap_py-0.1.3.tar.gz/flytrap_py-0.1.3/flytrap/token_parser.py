from collections.abc import Sequence
from .parser import IParser
from .parser_exception import ParserException

class TokenParser[E](IParser[E, E]):
    _target: E

    def __init__(self, t: E) -> None:
        self._target = t

    def parse(self, stream: Sequence[E]) -> tuple[E, Sequence[E]]:
        if len(stream) <= 0:
            raise ParserException(expect=str(self._target), actual="EOF")
        else:
            v = stream[0]
            if v == self._target:
                return (self._target, stream[1:])
            else:
                raise ParserException(expect=str(self._target), actual=str(v))


def token[E](t: E) -> IParser[E, E]:
    return TokenParser(t)
