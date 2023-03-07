import pytest
import dataclasses as dc
import chess as c
from core.square import *


def square_should_be_constructible():
    @dc.dataclass()
    class Case:
        name: str
        value: any
        want: int

    dummy = Square()
    dummy._idx = 42
    cases = [
        Case("None", None, 0),
        Case("int", 42, 42),
        Case("algebraic notation lower", "e4", c.parse_square("e4")),
        Case("algebraic notation upper", "E4", c.parse_square("e4")),
        Case("row and col", (1, 2), c.parse_square("c2")),
        Case("another square", dummy, 42),
    ]
    for case in cases:
        try:
            sq = Square(case.value)
        except:
            pytest.fail(f"'{case.name}' raised unexpectedly", True)
        assert sq.index == case.want, f"'{case.name}' can be used to construct a Square"


def square_should_validate_parameters_to_constructor():
    @dc.dataclass
    class Case:
        name: str
        value: any
        want: str

        def __iter__(self):
            return iter([self.name, self.value, self.want])

    cases = [
        Case("negative int", -1, "int must be 0<=X<=63"),
        Case("int too large", 64, "int must be 0<=X<=63"),
        Case("empty string", "", "algebraic form only"),
        Case("random string", "foo bar biz baz buz", "algebraic form only"),
        Case("illogical algebraic 1", "a0", "algebraic form only"),
        Case("illogical algebraic 2", "s4", "algebraic form only"),
    ]
    for name, value, want in cases:
        with pytest.raises(ValueError, match=want):
            Square(value)


def square_should_expose_accurate_convenience_properties():
    @dc.dataclass
    class Props:
        name: str
        index: int
        row: int
        col: int
        rank: int
        file: str
        white: bool
        black: bool
        mask: int
        smask: str

    @dc.dataclass
    class Case:
        name: str
        square: Square
        want: Props

        def __iter__(self):
            return iter([self.name, self.square, self.want])

    cases = [
        Case("0 - a1 - 0,0 - black", Square(c.A1),
             Props("a1", c.A1, 0, 0, 1, "a", False, True, 1 << c.A1, f"{1 << c.A1:063b}")),
        Case("8 - a2 - 1,0 - white", Square(c.A2),
             Props("a2", c.A2, 1, 0, 2, "a", True, False, 1 << c.A2, f"{1 << c.A2:063b}")),
        Case("63 - h8 - 7,8 - black", Square(c.H8),
             Props("h8", c.H8, 7, 7, 8, "h", False, True, 1 << c.H8, f"{1 << c.H8:063b}")),
    ]

    for name, square, want in cases:
        got = Props(
            square.name,
            square.index,
            square.row,
            square.col,
            square.rank,
            square.file,
            square.white,
            square.black,
            square.mask,
            square.smask,
        )
        assert got == want, name


def square_should_recognize_promotion_squares():
    @dc.dataclass
    class Case:
        name: str
        square: Square
        want: tuple  # (white, black, either)

        def __iter__(self):
            return iter([self.name, self.square, self.want])

    cases = [
        Case("a1 promote for black", Square(0), (False, True, True)),
        Case("e8 promote for white", Square(c.E8), (True, False, True)),
        Case("f5 promote for neither", Square(c.F5), (False, False, False)),
    ]

    for name, square, want in cases:
        got = (
            square.is_promotion(WHITE),
            square.is_promotion(BLACK),
            square.is_promotion(EITHER),
        )
        assert got == want, name


def square_should_have_equality_with_several_types():
    @dc.dataclass
    class Case:
        name: str
        square: Square
        other: any
        want: bool

        def __iter__(self):
            return iter([self.name, self.square, self.other, self.want])

    cases = [
        Case("Not equal None", Square(0), None, False),
        Case("Squares equal", Square(42), Square(42), True),
        Case("Squares not equal", Square(42), Square(24), False),
        Case("ints equal", Square(42), 42, True),
        Case("ints not equal", Square(42), 24, False),
        Case("algebraic equal", Square(42), "c6", True),
        Case("algebraic not equal", Square(42), "a3", False),
        Case("Never equal to bool", Square(0), False, False),
        Case("Never equal to dict", Square(0), dict(), False),
    ]
    for name, square, other, want in cases:
        got = square == other
        assert got == want, name
