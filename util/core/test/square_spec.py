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

        def __iter__(self):
            return iter([self.name, self.value, self.want])

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
    for name, value, want in cases:
        try:
            sq = Square(value)
        except:
            pytest.fail(f"Square construction failed for case \"{name}\"")
        assert sq.index == want, name


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
        sut: Square
        want: Props

        def __iter__(self):
            return iter([self.name, self.sut, self.want])

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
        sut: Square
        want: tuple  # (white, black, either)

        def __iter__(self):
            return iter([self.name, self.sut, self.want])

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
        sut: Square
        other: any
        want: bool

        def __iter__(self):
            return iter([self.name, self.sut, self.other, self.want])

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


def squareset_should_be_constructible():
    @dc.dataclass
    class Case:
        name: str
        value: any
        want: int

        def __iter__(self):
            return iter([self.name, self.value, self.want])

    cases = [
        Case("int", 42, 42),
        Case("zero case", 0, 0),
        Case("a1", "a1", 0x1),
        Case("e4 e5", ["e4", "d5"], (c.BB_E4 | c.BB_D5)),
        Case("Comma separated list", "a1,e4", (c.BB_A1 | c.BB_E4)),
        Case("mixed list a1 e4 g7", [s_all[0], "e4", c.BB_G7], (c.BB_A1 | c.BB_E4 | c.BB_G7)),
    ]

    for name, value, want in cases:
        try:
            ss = SquareSet(value)
        except:
            pytest.fail(f"SquareSet construction failed for case \"{name}\"")
        assert ss.value == want, name


def squareset_should_enumerate_squares():
    @dc.dataclass
    class Case:
        name: str
        sut: SquareSet
        want: Set[Square]

        def __iter__(self):
            return iter([self.name, self.sut, self.want])

    cases = [
        Case("Empty squareset", SquareSet(0), set([])),
        Case("Single square", SquareSet("a1"), {Square("a1")}),
        Case("Several squares", SquareSet("a1,a2,a3,a4"), set([s_all[i] for i in range(4)])),
        Case("All squares", SquareSet(c.BB_ALL), set(s_all)),
    ]

    for name, squareset, want in cases:
        pass


def squareset_should_offer_basic_set_operations():
    @dc.dataclass
    class Case:
        name: str
        sut: SquareSet | Callable[SquareSet]
        want: SquareSet

        def __iter__(self):
            return iter([self.name, self.sut, self.want])

    cases = [
        Case("0 inverse", lambda _: SquareSet(0).inverse(), ss_all),
        Case("all inverse", lambda _: ss_all.inverse(), ss_empty),
        Case("random inverse", lambda _: SquareSet(c.BB_A1 | c.BB_F5 | c.BB_A7).inverse(),
             SquareSet(c.BB_ALL & ~(c.BB_A1 | c.BB_F5 | c.BB_A7))),
        Case("union all none", lambda _: ss_all.union(ss_empty), ss_all),
        Case("union typical", lambda _: SquareSet("a1,g3,f8").union("b4,g3,a1,g8"), SquareSet("a1,b4,f8,g3,g8")),
        Case("union self", lambda _: SquareSet("a1,b3,f4").union(SquareSet("a1,b3,f4")), SquareSet("a1,b3,f4")),
        Case("intersection all none", lambda _: ss_all.intersect(ss_empty), ss_empty),
        Case("intersection all, all", lambda _: ss_all.intersect(ss_all), ss_all),
        Case("intersection typical", lambda _: SquareSet("f3,g8,f2").intersect("f8,f2"), SquareSet("f2")),
        Case("intersection disjoint", lambda _:SquareSet("a1,b3").intersect("f3f8"), ss_empty),
        Case("intersection self", lambda _: SquareSet("a1,b2").intersect("a1,b2"), SquareSet("a1,b2")),
        Case("difference all none", lambda _: ss_all.difference(ss_empty), ss_all),
        Case("difference all all", lambda _: ss_all.difference(ss_all), ss_empty),
        Case("difference none all", lambda _: ss_empty.difference(ss_all), ss_empty),
        Case("difference typical", lambda _: SquareSet("a1,f4,c3,c2").difference("c2,f4,g8"), SquareSet("a1,c3")),
        Case("difference superset", lambda _: SquareSet("a3,b3,g3").difference("a3,c5,b3,b7,b8,g3"), ss_empty),
    ]

def squareset_should_offer_set_subtest_methods():
    @dc.dataclass
    class Case:
        name: str
        sut: Callable[bool]
        want: bool

    cases = [
        Case("all is subset none", lambda _: ss_all.is_subset(ss_empty), True),
        Case("none is subset all", lambda _:ss_empty.is_subset(ss_all), False),
    ]
