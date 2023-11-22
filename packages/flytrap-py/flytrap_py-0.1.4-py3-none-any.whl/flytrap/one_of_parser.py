from .parser import IParser
from .parser_exception import ParserException

class OneOfParser(IParser[str, str]):
    _target: list[str]

    def __init__(self, targets: str) -> None:
        self._target = []
        for target in targets[:]:
            self._target.append(target)

    def parse(self, stream: str) -> tuple[str, str]:
        if len(stream) <= 0:
            raise ParserException(expect=self._target, actual="EOF")
        else:
            v = stream[0]
            if v in self._target:
                return (v, stream[1:])
            else:
                raise ParserException(expect=self._target, actual=v)

def one_of(v: str):
    return OneOfParser(v)
