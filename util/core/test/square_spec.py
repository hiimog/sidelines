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