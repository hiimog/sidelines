import dataclasses as dc
from core.square import *
from grappa import should


class TestSquare:
    def should_get_correct_square_color(self):
        @dc.dataclass
        class Case:
            name: str
            square: Square
            want: bool

        test_data = [
            Case("a1 is black", squareLookup["a1"], False),
            Case("a2 is white", squareLookup["a2"], True),
            Case("b1 is white", squareLookup["b1"], True),
            Case("h8 is black", squareLookup["h8"], False),
            Case("h1 is white", squareLookup["h1"], True),
        ]
        for i, t in enumerate(test_data):
            should(t.square.white).be.equal.to(t.want, msg=t.name)

    def should_calculate_row_and_col(self):
        @dc.dataclass
        class Case:
            name: str
            square: Square
            want: Tuple[int, int]

        test_data = [
            Case("a1 is 0, 0", squareLookup["a1"], (0, 0)),
            Case("a2 is 1, 0", squareLookup["a2"], (1, 0)),
            Case("b1 is 0, 1", squareLookup["b1"], (0, 1)),
            Case("h8 is 7, 7", squareLookup["h8"], (7, 7)),
            Case("h1 is 0, 7", squareLookup["h1"], (0, 7)),
        ]
        for i, t in enumerate(test_data):
            should((t.square.row, t.square.col)).be.equal.to(t.want, msg=t.name)

    def should_calculate_name(self):
        @dc.dataclass
        class Case:
            name: str
            square: Square
            want: str

        test_data = [
            Case("a1", squareLookup["a1"], "a1"),
            Case("e4", squareLookup["e4"], "e4"),
            Case("h8", squareLookup["h8"], "h8"),
        ]
        for i, t in enumerate(test_data):
            should(t.square.name).be.equal.to(t.want, msg=t.name)
