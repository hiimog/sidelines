import re
from functools import total_ordering
from typing import *

ALGEBRAIC_REGEX = re.compile("^[a-h][1-8]$", re.I)
BLACK = "black"
EITHER = "either"
WHITE = "white"

SideNames = Literal["white", "black", "either"]

SquareConstructorType = Union[int, str, Tuple[int, int], "Square"]


@total_ordering
class Square:
    def __init__(self, which: SquareConstructorType = None):
        self._idx: int = 0
        if which is None:
            self._idx = 0
            return
        if type(which) == int:
            self._idx = which
            if not self._is_valid():
                raise ValueError("int must be 0<=X<=63")
        elif type(which) == tuple and len(which) == 2:
            row, col = which
            if type(row) != int or type(col) != int:
                raise ValueError("2-tuple can only be for ints")
            self._idx = row * 8 + col
            if not self._is_valid():
                raise ValueError("2-tuple must each have values 0<=X<=7")
        elif type(which) == str:
            which = which.lower()
            if not ALGEBRAIC_REGEX.search(which):
                raise ValueError("algebraic form only")
            row = int(which[1]) - 1
            col = "abcdefgh".index(which[0])
            self._idx = row * 8 + col
        elif type(which) == Square:
            self._idx = which.idx
        else:
            raise ValueError("Unsupported constructor value")

    @property
    def idx(self) -> int:
        return self._idx

    @property
    def row(self):
        return self.idx // 8

    @property
    def col(self):
        return self.idx % 8

    @property
    def row_col(self):
        return self.row, self.col

    @property
    def rank(self):
        return self.row + 1

    @property
    def file(self):
        return "abcdefgh"[self.col]

    @property
    def rank_file(self):
        return self.rank, self.file

    @property
    def row_col_rank_file(self):
        return self.row, self.col, self.rank, self.file

    @property
    def name(self):
        return f"{self.file}{self.rank}"

    @property
    def white(self):
        return (self.row + self.col) % 2 == 1

    @property
    def black(self):
        return not self.white

    @property
    def mask(self) -> int:
        return 1 << self.idx

    @property
    def smask(self):
        return f"{self.mask:064b}"

    def is_promotion(self, side: SideNames = EITHER):
        if side == WHITE:
            return self.row == 7
        if side == BLACK:
            return self.row == 0
        if side == EITHER:
            return self.row == 0 or self.row == 7
        raise ValueError("sides must be white, black, or either")

    def _is_valid(self):
        return 0 <= self.idx <= 63

    def __bytes__(self):
        return bytes(self.idx)

    def __eq__(self, other):
        if other is None:
            return False
        tipe = type(other)
        if tipe == int:
            return self.idx == other
        if tipe == Square:
            return self.idx == other.idx
        if tipe == str:
            return self.name == other.lower()
        return False

    def __hash__(self):
        return self.idx

    def __hex__(self):
        return hex(self.idx)

    def __int__(self):
        return self.idx

    def __lt__(self, other):
        return self.idx < Square(other).idx

    def __repr__(self):
        return f"SQ({self.name})"

    def __str__(self):
        return self.name


SQ = Square

SquareSetConstructorType = Union[int, Iterable, str, Square, "SquareSet"]


class SquareSet:
    def __init__(self, initial: Optional[SquareSetConstructorType] = None):
        self._value = 0
        if initial is None:
            return
        tipe = type(initial)
        if tipe == SquareSet:
            self._value = initial.value
        elif tipe == int:
            self._value = initial
        elif tipe in [tuple, list, set]:
            self._init_from_iter(initial)
        elif tipe == str:
            self._init_from_str(initial)
        elif tipe == Square:
            self._value = initial.mask
        else:
            self._value = Square(initial).mask
        if self._value < 0:
            self._value += 2 ** 64

    @property
    def value(self):
        return self._value

    @property
    def inverse(self):
        return SquareSet(~self.value)

    @property
    def bits(self):
        return f"{self.value:064b}"

    @property
    def count(self):
        return self.value.bit_count()

    def union(self, other: any) -> Self:
        other = SS(other)
        return SquareSet(self.value | other.value)

    def intersect(self, other: any) -> Self:
        other = SS(other)
        return SquareSet(self.value & other.value)

    def difference(self, other: any) -> Self:
        other = SS(other)
        return SquareSet(self.value & ~other.value)

    def is_subset_of(self, other: any):
        other = SS(other)
        return self.value == (self.value & other.value)

    def has_subset(self, other: any):
        other = SS(other)
        return other.value == (self.value & other.value)

    def is_proper_subset_of(self, other: any):
        other = SS(other)
        return self.is_subset_of(other.value) and self.value != other.value

    def has_proper_subset(self, other: any):
        other = SS(other)
        return self.has_subset(other) and self.value != other.value

    def is_superset_of(self, other: any):
        other = SS(other)
        return other.value == (other.value & self.value)

    def has_superset(self, other: any):
        other = SS(other)
        return self.value == (other.value & self.value)

    def is_proper_superset_of(self, other: any):
        other = SS(other)
        return self.is_superset_of(other.value) and self.value != other.value

    def has_proper_superset(self, other: any):
        other = SS(other)
        return self.has_superset(other) and (self.value != other.value)

    def squares(self) -> List[Square]:
        return list(self)

    def _comma_sep_alg(self):
        return ",".join([sq.name for sq in self.squares()])

    def _init_from_iter(self, initial: Iterable) -> None:
        acc = 0
        for i, item in enumerate(initial):
            tipe = type(item)
            if tipe == SquareSet:
                acc |= item.value
            elif tipe == Square:
                acc |= item.mask
            elif tipe == int:
                acc |= item
            else:
                try:
                    acc |= Square(item).mask
                except ValueError:
                    raise ValueError(f"item {i}: \"{item}\" can not be part of a SquareSet")
        self._value = acc

    def _init_from_str(self, initial: str):
        trimmed = [sq.strip() for sq in initial.split(",")]
        self._init_from_iter(trimmed)

    def __add__(self, other: any) -> Self:
        return self.union(SS(other))

    def __and__(self, other: any) -> Self:
        return self.intersect(SS(other))

    def __bool__(self):
        return bool(self.value)

    def __bytes__(self):
        return bytes(self.value)

    def __contains__(self, item):
        return self.is_superset_of(SS(item))

    def __copy__(self):
        return SquareSet(self.value)

    def __eq__(self, other: any):
        return self.value == SS(other).value

    def __format__(self, format_spec):
        if format_spec == "alg":
            return self._comma_sep_alg()
        if format_spec == "b":
            return self.bits
        return self.value.__format__(format_spec)

    def __ge__(self, other):
        return self.is_superset_of(SS(other))

    def __getitem__(self, item: any):
        sq = SQ(item)
        return bool(self.value & sq.mask)

    def __gt__(self, other):
        return self.is_proper_superset_of(SS(other))

    def __hash__(self) -> int:
        return self.value

    def __hex__(self):
        return hex(self.value)

    def __int__(self):
        return self.value

    def __invert__(self):
        return SquareSet(~self.value)

    def __iter__(self):
        for i in range(64):
            if self.value & (1 << i):
                yield Square(i)

    def __le__(self, other: any):
        return self.is_subset_of(SS(other))

    def __len__(self):
        return self.count

    def __lt__(self, other: any):
        return self.is_proper_subset_of(SS(other))

    def __neg__(self):
        return SquareSet(~self.value)

    def __ne__(self, other: any):
        return self.value != SS(other).value

    def __or__(self, other):
        return SquareSet(self.value | other.value)

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return f"SS({self._comma_sep_alg()})"

    def __sub__(self, other):
        return SS(self.value & ~SS(other).value)


SS = SquareSet


def ranks(*args) -> Tuple[Square]:
    res = []
    for i in args:
        for j in range(8 * (i - 1), 8 * i):
            res.append(SQ(j))
    return tuple(res)


def files(s: str) -> Tuple[Square]:
    res = []
    for c in s:
        idx = "abcdefgh".index(c)
        for j in range(idx, 64, 8):
            res.append(SQ(j))
    return tuple(res)


class sq:
    class starting:
        all = ranks(1, 2, 7, 8)
        white = ranks(1, 2)
        black = ranks(7, 8)
        pawns = ranks(2, 7)
        knights = tuple((SQ(s) for s in ["b1", "g1", "b8", "g8"]))
        bishops = tuple((SQ(s) for s in ["c1", "f1", "c8", "f8"]))
        rooks = tuple((SQ(s) for s in ["a1", "h1", "a8", "h8"]))
        queens = tuple((SQ(s) for s in ["d1", "d8"]))
        kings = tuple((SQ(s) for s in ["e1", "e8"]))

    class ranks:
        r1 = ranks(1)
        r2 = ranks(2)
        r3 = ranks(3)
        r4 = ranks(4)
        r5 = ranks(5)
        r6 = ranks(6)
        r7 = ranks(7)
        r8 = ranks(8)

    class files:
        a = files("a")
        b = files("b")
        c = files("c")
        d = files("d")
        e = files("e")
        f = files("f")
        g = files("g")
        h = files("h")

    class white:
        squares = tuple(SQ(i) for i in range(1, 64, 2))

        class castling:
            short_blockable = tuple(SQ(i) for i in ["f1", "g1"])
            short_checkable = tuple(SQ(i) for i in ["e1", "f1", "g1"])
            short_king = SQ("g1")
            short_rook = SQ("f1")
            long_blockable = tuple(SQ(i) for i in ["b1", "c1", "d1"])
            long_checkable = tuple(SQ(i) for i in ["c1", "d1", "e1"])
            long_king = SQ("c1")
            long_rook = SQ("d1")

        class starting:
            all = ranks(1, 2)
            pawns = ranks(2)
            knights = tuple((SQ(s) for s in ["b1", "g1"]))
            bishops = tuple((SQ(s) for s in ["c1", "f1"]))
            rooks = tuple((SQ(s) for s in ["a1", "h1"]))
            queens = tuple((SQ(s) for s in ["d1"]))
            king = SQ("e1")
            promotion = ranks(8)

    class black:
        squares = tuple(SQ(i) for i in range(0, 64, 2))

        class castling:
            short_blockable = tuple(SQ(i) for i in ["f8", "g8"])
            short_checkable = tuple(SQ(i) for i in ["e8", "f8", "g8"])
            short_king = SQ("g8")
            short_rook = SQ("f8")
            long_blockable = tuple(SQ(i) for i in ["b8", "c8", "d8"])
            long_checkable = tuple(SQ(i) for i in ["c8", "d8", "e8"])
            long_king = SQ("c8")
            long_rook = SQ("d8")

        class starting:
            all = ranks(7, 8)
            pawns = ranks(7)
            knights = tuple((SQ(s) for s in ["b8", "g8"]))
            bishops = tuple((SQ(s) for s in ["c8", "f8"]))
            rooks = tuple((SQ(s) for s in ["a8", "h8"]))
            queens = tuple((SQ(s) for s in ["d8"]))
            king = SQ("e8")
            promotion = ranks(1)

    all = tuple(SQ(i) for i in range(64))
    none = tuple()
    empty = tuple()
    a1 = SQ("a1")
    b1 = SQ("b1")
    c1 = SQ("c1")
    d1 = SQ("d1")
    e1 = SQ("e1")
    f1 = SQ("f1")
    g1 = SQ("g1")
    h1 = SQ("h1")
    a2 = SQ("a2")
    b2 = SQ("b2")
    c2 = SQ("c2")
    d2 = SQ("d2")
    e2 = SQ("e2")
    f2 = SQ("f2")
    g2 = SQ("g2")
    h2 = SQ("h2")
    a3 = SQ("a3")
    b3 = SQ("b3")
    c3 = SQ("c3")
    d3 = SQ("d3")
    e3 = SQ("e3")
    f3 = SQ("f3")
    g3 = SQ("g3")
    h3 = SQ("h3")
    a4 = SQ("a4")
    b4 = SQ("b4")
    c4 = SQ("c4")
    d4 = SQ("d4")
    e4 = SQ("e4")
    f4 = SQ("f4")
    g4 = SQ("g4")
    h4 = SQ("h4")
    a5 = SQ("a5")
    b5 = SQ("b5")
    c5 = SQ("c5")
    d5 = SQ("d5")
    e5 = SQ("e5")
    f5 = SQ("f5")
    g5 = SQ("g5")
    h5 = SQ("h5")
    a6 = SQ("a6")
    b6 = SQ("b6")
    c6 = SQ("c6")
    d6 = SQ("d6")
    e6 = SQ("e6")
    f6 = SQ("f6")
    g6 = SQ("g6")
    h6 = SQ("h6")
    a7 = SQ("a7")
    b7 = SQ("b7")
    c7 = SQ("c7")
    d7 = SQ("d7")
    e7 = SQ("e7")
    f7 = SQ("f7")
    g7 = SQ("g7")
    h7 = SQ("h7")
    a8 = SQ("a8")
    b8 = SQ("b8")
    c8 = SQ("c8")
    d8 = SQ("d8")
    e8 = SQ("e8")
    f8 = SQ("f8")
    g8 = SQ("g8")
    h8 = SQ("h8")


class ss:
    class starting:
        all = SS(sq.starting.all)
        white = SS(sq.starting.white)
        black = SS(sq.starting.black)
        pawns = SS(sq.starting.pawns)
        knights = SS(sq.starting.knights)
        bishops = SS(sq.starting.bishops)
        rooks = SS(sq.starting.rooks)
        queens = SS(sq.starting.queens)
        kings = SS(sq.starting.kings)

    class ranks:
        r1 = SS(sq.ranks.r1)
        r2 = SS(sq.ranks.r2)
        r3 = SS(sq.ranks.r3)
        r4 = SS(sq.ranks.r4)
        r5 = SS(sq.ranks.r5)
        r6 = SS(sq.ranks.r6)
        r7 = SS(sq.ranks.r7)
        r8 = SS(sq.ranks.r8)

    class files:
        a = SS(sq.files.a)
        b = SS(sq.files.b)
        c = SS(sq.files.c)
        d = SS(sq.files.d)
        e = SS(sq.files.e)
        f = SS(sq.files.f)
        g = SS(sq.files.g)
        h = SS(sq.files.h)

    class white:
        squares = SS(sq.white.squares)

        class castling:
            short_blockable = SS(sq.white.castling.short_blockable)
            short_checkable = SS(sq.white.castling.short_checkable)
            short_king = SS(sq.white.castling.short_king)
            short_rook = SS(sq.white.castling.short_rook)
            long_blockable = SS(sq.white.castling.long_blockable)
            long_checkable = SS(sq.white.castling.long_checkable)
            long_king = SS(sq.white.castling.long_king)
            long_rook = SS(sq.white.castling.long_rook)

        class starting:
            all = SS(sq.white.starting.all)
            pawns = SS(sq.white.starting.pawns)
            knights = SS(sq.white.starting.knights)
            bishops = SS(sq.white.starting.bishops)
            rooks = SS(sq.white.starting.rooks)
            queens = SS(sq.white.starting.queens)
            king = SS(sq.white.starting.king)
            promotion = SS(sq.white.starting.promotion)

    class black:
        squares = SS(sq.black.squares)

        class castling:
            short_blockable = SS(sq.black.castling.short_blockable)
            short_checkable = SS(sq.black.castling.short_checkable)
            short_king = SS(sq.black.castling.short_king)
            short_rook = SS(sq.black.castling.short_rook)
            long_blockable = SS(sq.black.castling.long_blockable)
            long_checkable = SS(sq.black.castling.long_checkable)
            long_king = SS(sq.black.castling.long_king)
            long_rook = SS(sq.black.castling.long_rook)

        class starting:
            all = SS(sq.black.starting.all)
            pawns = SS(sq.black.starting.pawns)
            knights = SS(sq.black.starting.knights)
            bishops = SS(sq.black.starting.bishops)
            rooks = SS(sq.black.starting.rooks)
            queens = SS(sq.black.starting.queens)
            king = SS(sq.black.starting.king)
            promotion = SS(sq.black.starting.promotion)

    all = SS(sq.all)
    none = SS(sq.none)
    empty = SS(sq.empty)
    a1 = SS("a1")
    b1 = SS("b1")
    c1 = SS("c1")
    d1 = SS("d1")
    e1 = SS("e1")
    f1 = SS("f1")
    g1 = SS("g1")
    h1 = SS("h1")
    a2 = SS("a2")
    b2 = SS("b2")
    c2 = SS("c2")
    d2 = SS("d2")
    e2 = SS("e2")
    f2 = SS("f2")
    g2 = SS("g2")
    h2 = SS("h2")
    a3 = SS("a3")
    b3 = SS("b3")
    c3 = SS("c3")
    d3 = SS("d3")
    e3 = SS("e3")
    f3 = SS("f3")
    g3 = SS("g3")
    h3 = SS("h3")
    a4 = SS("a4")
    b4 = SS("b4")
    c4 = SS("c4")
    d4 = SS("d4")
    e4 = SS("e4")
    f4 = SS("f4")
    g4 = SS("g4")
    h4 = SS("h4")
    a5 = SS("a5")
    b5 = SS("b5")
    c5 = SS("c5")
    d5 = SS("d5")
    e5 = SS("e5")
    f5 = SS("f5")
    g5 = SS("g5")
    h5 = SS("h5")
    a6 = SS("a6")
    b6 = SS("b6")
    c6 = SS("c6")
    d6 = SS("d6")
    e6 = SS("e6")
    f6 = SS("f6")
    g6 = SS("g6")
    h6 = SS("h6")
    a7 = SS("a7")
    b7 = SS("b7")
    c7 = SS("c7")
    d7 = SS("d7")
    e7 = SS("e7")
    f7 = SS("f7")
    g7 = SS("g7")
    h7 = SS("h7")
    a8 = SS("a8")
    b8 = SS("b8")
    c8 = SS("c8")
    d8 = SS("d8")
    e8 = SS("e8")
    f8 = SS("f8")
    g8 = SS("g8")
    h8 = SS("h8")
