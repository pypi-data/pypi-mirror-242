from collections.abc import Sequence
from flytrap.many1_parser import many1
from .parser import IParser
from .parser_exception import ParserException

class ManyParser[E, O](IParser[E, list[O]]):
    """
    p = many(digit())

    p.parse("123")
    >> ["1", "2", "3"]

    p.parse("")
    >> []
    """

    _many1: IParser[E, list[O]]

    def __init__(self, p: IParser[E, O]) -> None:
        self._many1 = many1(p)

    def parse(self, s: Sequence[E]) -> tuple[list[O], Sequence[E]]:
        try:
            (v, stream) = self._many1.parse(s)
            return (v, stream)
        except ParserException:
            return ([], s)


def many[E, O](p: IParser[E, O])-> IParser[E, list[O]]:
    return ManyParser[E, O](p)
