import dataclasses
import dataclasses as dc
from core.square import *
import pytest

class TestSquare():
    def should_be_constructable_from(self):
        @dc.dataclass
        class Case:
            name: str
            value: any
            want: int
        dummy = Square(0)
        dummy._idx = 8
        test_data = [
            Case("None", None, 0),
            Case("a1", "a1", 0),
            Case("63", 63, 63),
            Case("Square", dummy, 8)
        ]
        for t in test_data:

            s = Square(t.value)
            should(s.index).to.be(t.want, msg=t.name)

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

class TestSquareSet:
    def should_be_creatable_from(self):
        @dataclasses.dataclass
        class Case:
            name: str
            values: any
            want: int

        dummy_square_set = SquareSet()
        dummy_square_set._value = 42

        test_data = [
            Case("No parameters", None, 0),
            Case("Single square", squares[0], 0b1),
            Case("List of squares", squares[0:3], 0b111),
            Case("SquareSet", dummy_square_set, 42),
            Case("int", 42, 42),
            Case("Mix of types", [squareLookup["a1"], 2], 0b11)
        ]

        for t in test_data:
            _ = (lambda _: SquareSet(t.values) | should.does_not.raises(msg=t.name))
            sut = SquareSet(t.values)
            should(sut.value).be.equal.to(t.want, msg=t.name)
