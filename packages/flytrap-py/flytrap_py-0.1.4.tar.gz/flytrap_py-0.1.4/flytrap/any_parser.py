from typing import Sequence
from .parser import IParser
from .parser_exception import ParserException

class AnyParser[E](IParser[E, E]):
    def __init__(self) -> None:
        pass

    def parse(self, stream: Sequence[E]) -> tuple[E, Sequence[E]]:
        if len(stream) > 0:
            return (stream[0], stream[1:])
        else:
            raise ParserException(expect="*", actual="EOF")

def any[E]():
    return AnyParser[E]()
