from collections.abc import Sequence
from typing import Any
from .parser import IParser
from .parser_exception import ParserException

class SplitByParser[E, O](IParser[E, list[O]]):
    """
    example:
    p = split_by(string("world"), digit())
    p.parse("world1world2world")
    >> (["world", "world", "world"], "")

    p.parse("world1world2world3")
    >> raise ParserException
    """
    _split: IParser[E, Any]
    _p: IParser[E, O]

    def __init__(self, p: IParser[E, O], split: IParser[E, Any]) -> None:
        self._p = p
        self._split = split

    def parse(self, s: Sequence[E]) -> tuple[list[O], Sequence[E]]:
        try:
            (value, stream) = self._p.parse(s)
        except ParserException as e:
            raise e
        else:
            try:
                split_result = self._split.parse(stream)
            except ParserException:
                return ([value], stream)
            else:
                child_result = self.parse(split_result[1])
                return ([value] + child_result[0], child_result[1])


def split_by[E, O](p: IParser[E, O], split: IParser[E, Any])-> IParser[E, list[O]]:
    return SplitByParser[E, O](p, split)
