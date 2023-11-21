from .space_parser import space, spaces

class TestSpaceParser:
    def test_ok_space(self):
        assert space().parse(" a") == (" ", "a")

    def test_ok_spaces(self):
        assert spaces().parse(" \ta") == ([" ","\t"], "a")

