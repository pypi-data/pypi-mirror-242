# flytrap-py
parser

## How to use
```python3
from typing import Dict, Union
from flytrap import IParser, attempt, choice, digit, lazy, many1, spaces, split_by, string, token, until

type Json =  Union[str, int, bool, None, list[Json], Dict[str, Json]]

def ignore_spaces[O](p: IParser[str, O]) -> IParser[str, O]:
    return attempt(spaces()).with_(p)

def jstring() -> IParser[str, Json]:
    """
    support only simple string
    """
    return ignore_spaces(token('"').with_(until(token('"'))).skip(token('"')).map(str))

def jnumber() -> IParser[str, Json]:
    """
    support only simple number
    """
    def _inner(values: list[str]):
        return int("".join(values))
    return ignore_spaces(many1(digit()).map(_inner))

def jboolean() -> IParser[str, Json]:
    return ignore_spaces(choice(
            string("true").map(lambda _: True),
            string("false").map(lambda _: False)
            ))

def jnull() -> IParser[str, Json]:
    return ignore_spaces(string("null").map(lambda _: None))

def jarray() -> IParser[str, Json]:
    def _inner(v: list[Json] | None)->Json:
        if v is None: return list([])
        else:         return list(v)

    return ignore_spaces(token("[")).with_(
                attempt(split_by(jvalue(), ignore_spaces(token(","))))
            ).skip(ignore_spaces(token("]"))).map(_inner)

def jobject() -> IParser[str, Json]:
    def _inner(values: list[tuple[Json, Json]] | None)->Json:
        result = {}

        if values is None:
            return result
        else:
            for (key, value) in values:
                result[key] = value

        return result

    return ignore_spaces(token("{")).with_(
            attempt(split_by(
                jstring().skip(ignore_spaces(token(":"))).and_(jvalue()),
                ignore_spaces(token(","))
            ))
        ).skip(ignore_spaces(token("}"))).map(_inner)

def jvalue() -> IParser[str, Json]:
    return choice(
                                jstring(),
                                jnumber(),
                                jboolean(),
                                jnull(),
                                lazy(jarray),
                                lazy(jobject)
                                )

def parser(src: str) -> Json:
    (j, _) = jvalue().parse(src)
    return j
```
