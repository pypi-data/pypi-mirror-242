from .many1_parser import many1
from .one_of_parser import one_of

def space():
    return one_of(" \t\n\r")

def spaces():
    return many1(space())
