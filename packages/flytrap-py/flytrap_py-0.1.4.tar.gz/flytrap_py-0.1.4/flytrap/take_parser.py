from collections.abc import Sequence
from .parser import IParser
from .parser_exception import ParserException

class TakeParser[E](IParser[E, Sequence[E]]):
    _length: int

    def __init__(self, n: int) -> None:
        self._length = n

    def parse(self, stream: str) -> tuple[str, str]:
        if len(stream) >= self._length:
            return (stream[:self._length], stream[self._length:])
        else:
            raise ParserException(
                expect='*'*self._length,
                actual=stream[:self._length]
            )


def take[E](n: int):
    return TakeParser[E](n)
