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

    dummy = SQ()
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
            sq = SQ(value)
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
            SQ(value)


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
        Case("0 - a1 - 0,0 - black", SQ(c.A1),
             Props("a1", c.A1, 0, 0, 1, "a", False, True, 1 << c.A1, f"{1 << c.A1:063b}")),
        Case("8 - a2 - 1,0 - white", SQ(c.A2),
             Props("a2", c.A2, 1, 0, 2, "a", True, False, 1 << c.A2, f"{1 << c.A2:063b}")),
        Case("63 - h8 - 7,8 - black", SQ(c.H8),
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
        Case("a1 promote for black", SQ(0), (False, True, True)),
        Case("e8 promote for white", SQ(c.E8), (True, False, True)),
        Case("f5 promote for neither", SQ(c.F5), (False, False, False)),
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
        Case("Not equal None", SQ(0), None, False),
        Case("Squares equal", SQ(42), SQ(42), True),
        Case("Squares not equal", SQ(42), SQ(24), False),
        Case("ints equal", SQ(42), 42, True),
        Case("ints not equal", SQ(42), 24, False),
        Case("algebraic equal", SQ(42), "c6", True),
        Case("algebraic not equal", SQ(42), "a3", False),
        Case("Never equal to bool", SQ(0), False, False),
        Case("Never equal to dict", SQ(0), dict(), False),
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
        Case("mixed list a1 e4 g7", [s.all[0], "e4", c.BB_G7], (c.BB_A1 | c.BB_E4 | c.BB_G7)),
    ]

    for name, value, want in cases:
        try:
            ss = SS(value)
        except:
            pytest.fail(f"SquareSet construction failed for case \"{name}\"")
        assert ss.value == want, name


def squareset_should_enumerate_squares():
    @dc.dataclass
    class Case:
        name: str
        sut: SS
        want: Set[Square]

        def __iter__(self):
            return iter([self.name, self.sut, self.want])

    cases = [
        Case("Empty squareset", SS(0), set([])),
        Case("Single square", SS("a1"), {SQ("a1")}),
        Case("Several squares", SS("a1,a2,a3,a4"), set([s.all[i] for i in range(4)])),
        Case("All squares", SS(c.BB_ALL), set(s.all)),
    ]


def squareset_should_offer_basic_set_operations():
    @dc.dataclass
    class Case:
        name: str
        sut: Callable[[], SS]
        want: SS

        def __iter__(self):
            return iter([self.name, self.sut, self.want])

    cases = [
        Case("0 inverse", lambda: SS(0).inverse, ss.all),
        Case("all inverse", lambda: ss.all.inverse, ss.none),
        Case("random inverse", lambda: SS(c.BB_A1 | c.BB_F5 | c.BB_A7).inverse,
             SS(c.BB_ALL & ~(c.BB_A1 | c.BB_F5 | c.BB_A7))),
        Case("union all none", lambda: ss.all.union(ss.none), ss.all),
        Case("union typical", lambda: SS("a1,g3,f8").union("b4,g3,a1,g8"), SS("a1,b4,f8,g3,g8")),
        Case("union self", lambda: SS("a1,b3,f4").union(SS("a1,b3,f4")), SS("a1,b3,f4")),
        Case("intersection all none", lambda: ss.all.intersect(ss.none), ss.none),
        Case("intersection all, all", lambda: ss.all.intersect(ss.all), ss.all),
        Case("intersection typical", lambda: SS("f3,g8,f2").intersect("f8,f2"), SS("f2")),
        Case("intersection disjoint", lambda: SS("a1,b3").intersect("f3,f8"), ss.none),
        Case("intersection self", lambda: SS("a1,b2").intersect("a1,b2"), SS("a1,b2")),
        Case("difference all none", lambda: ss.all.difference(ss.none), ss.all),
        Case("difference all all", lambda: ss.all.difference(ss.all), ss.none),
        Case("difference none all", lambda: ss.none.difference(ss.all), ss.none),
        Case("difference typical", lambda: SS("a1,f4,c3,c2").difference("c2,f4,g8"), SS("a1,c3")),
        Case("difference superset", lambda: SS("a3,b3,g3").difference("a3,c5,b3,b7,b8,g3"), ss.none),
    ]

    for name, sut, want in cases:
        assert sut().__eq__(want), name



def squareset_should_offer_subset_methods():
    @dc.dataclass
    class Case:
        name: str
        sut: Callable[[], bool]

        def __iter__(self):
            return iter([self.name, self.sut])

    cases = [
        Case("white starting pawns is subset of all white starting",
             lambda: ss.white.starting.pawns.is_subset_of(ss.white.starting.all)),
        Case("white starting pawns is proper subset of all white starting",
             lambda: ss.white.starting.pawns.is_proper_subset_of(ss.white.starting .all)),
        Case("all black starting is superset of black rooks",
             lambda: ss.black.starting.all.is_superset_of(ss.black.starting.rooks)),
        Case("starting pawns is proper superset of rank 7",
             lambda: ss.starting.pawns.is_proper_superset_of(ss.rank.r7)),
        Case("white starting has subset white starting", lambda: ss.white.starting.all.has_subset(ss.white.starting.all)),
        Case("white starting does not have proper subset white starting",
             lambda: not ss.white.starting.all.has_proper_subset(ss.white.starting.all)),
        Case("starting white has superset starting all", lambda: ss.white.starting.all.has_superset(ss.starting.all))
    ]

    for name, sut in cases:
        assert sut(), name
