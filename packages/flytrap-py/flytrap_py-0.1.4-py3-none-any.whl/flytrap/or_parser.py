from collections.abc import Sequence
from .parser import IParser
from .parser_exception import ParserException

class OrParser[E, O](IParser[E, O]):
    _p1: IParser[E, O]
    _p2: IParser[E, O]

    def __init__(self, p1: IParser[E, O], p2: IParser[E, O]) -> None:
        self._p1 = p1
        self._p2 = p2

    def parse(self, stream: Sequence[E]) -> tuple[O, Sequence[E]]:
        try:
            return self._p1.parse(stream)
        except ParserException as e1:
            try:
                return self._p2.parse(stream)
            except ParserException as e2:
                raise ParserException.concat(e1, e2)
