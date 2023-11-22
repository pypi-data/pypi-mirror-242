from collections.abc import Sequence
from .parser import IParser
from .parser_exception import ParserException

class Many1Parser[E, O](IParser[E, list[O]]):
    """
    p = many1(digit())

    p.parse("123")
    >> ["1", "2", "3"]

    p.parse("")
    >> raise ParserException
    """

    _p: IParser[E, O]

    def __init__(self, p: IParser[E, O]) -> None:
        self._p = p

    def _inner_parse(self, s: Sequence[E]) -> tuple[list[O], Sequence[E]]:
        """
        ignore exception
        """
        try:
            (v, stream) = self._p.parse(s)
        except ParserException:
            return ([], s)
        else:
            (v1, stream2) = self._inner_parse(stream)
            return ([v] + v1, stream2)

    def parse(self, s: Sequence[E]) -> tuple[list[O], Sequence[E]]:
        (v, stream) = self._p.parse(s)
        (v1, stream2) = self._inner_parse(stream)
        return ([v] + v1, stream2)


def many1[E, O](p: IParser[E, O])-> IParser[E, list[O]]:
    return Many1Parser[E, O](p)
