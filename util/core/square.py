import functools
import re
from typing import *
from addict import Dict
from bitarray import frozenbitarray, bitarray, util
from functools import total_ordering

ALGEBRAIC_REGEX = re.compile("^[a-h][1-8]$", re.I)
WHITE = "white"
BLACK = "black"
EITHER = "either"
SideNames = Literal["white", "black", "either"]


def int2fba(i):
    return frozenbitarray(util.int2ba(i, 64))


def int2ba(i):
    return util.int2ba(i, 64)


@total_ordering
class Square:
    def __init__(self, which: any = None):
        self._idx = 0
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
            self._idx = which.index
        else:
            raise ValueError("Unsupported constructor value")

    def _is_valid(self):
        return 0 <= self.index <= 63

    @property
    def index(self):
        return self._idx

    @property
    def row(self):
        return self.index // 8

    @property
    def col(self):
        return self.index % 8

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
    def mask(self):
        return util.int2ba(1 << self.index, 64)

    @property
    def smask(self):
        return self.mask.to01()

    def is_promotion(self, side: SideNames = EITHER):
        if side == WHITE:
            return self.row == 7
        if side == BLACK:
            return self.row == 0
        if side == EITHER:
            return self.row == 0 or self.row == 7
        raise ValueError("sides must be white, black, or either")

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Square({self.name})"

    def __int__(self):
        return self.index

    def __lt__(self, other):
        return self.index < Square(other).index

    def __eq__(self, other):
        if other is None:
            return False
        tipe = type(other)
        if tipe == int:
            return self.index == other
        if tipe == Square:
            return self.index == other.index
        if tipe == str:
            return self.name == other.lower()
        return False

    def __hash__(self):
        return self.index

    def __bytes__(self):
        return bytes(self.index)

    def __hex__(self):
        return hex(self.index)


SQ = Square


class SquareSet:
    def __init__(self, initial: any = None):
        self._value = int2fba(0)
        if initial is None:
            return
        tipe = type(initial)
        if tipe == SquareSet:
            self._value = initial.value
        elif tipe == int:
            self._value = int2fba(initial)
        elif tipe == list:
            self._init_from_list(initial)
        elif tipe == str:
            self._init_from_str(initial)
        elif tipe == Square:
            self._value = frozenbitarray(initial.mask)
        elif tipe in [frozenbitarray, bitarray]:
            self._value = frozenbitarray(initial)
        else:
            self._value = frozenbitarray(Square(initial).mask)

    @property
    def value(self):
        return self._value

    @property
    def inverse(self):
        return SquareSet(~self.value)

    def union(self, other: any):
        return SquareSet(self.value | SquareSet(other).value)

    def intersect(self, other: any):
        return SquareSet(self.value & SquareSet(other).value)

    def difference(self, other: any):
        return SquareSet(self.value & ~SquareSet(other).value)

    def is_subset_of(self, other: any):
        return self.value == (self.value & SquareSet(other).value)

    def has_subset(self, other: any):
        other = SquareSet(other)
        return other.value == (self.value & other.value)

    def is_proper_subset_of(self, other: any):
        other = SquareSet(other)
        return self.is_subset_of(other) and self.value != other.value

    def has_proper_subset(self, other: any):
        other = SquareSet(other).value
        return self.value == (other & self.value) and self.value != other

    def is_superset_of(self, other: any):
        other = SquareSet(other)
        return other.value == (other.value & self.value)

    def has_superset(self, other: any):
        return self.value == (SquareSet(other).value & self.value)

    def is_proper_superset_of(self, other: any):
        return self.is_superset_of(other) and self.value != SquareSet(other).value

    def has_proper_superset(self, other: any):
        return self.has_superset(other) and self.value != SquareSet(other).value

    def __add__(self, other):
        return self.union(other)

    def __and__(self, other):
        return self.intersect(other)

    def __bool__(self):
        return self.value.any()

    def __bytes__(self):
        return self.value.tobytes()

    def __getitem__(self, item):
        sq = Square(item)
        return bool(self.value[sq.index])

    def __contains__(self, item):
        return self.is_superset_of(item)

    def __copy__(self):
        return SquareSet(self.value)

    def __hex__(self):
        return util.ba2hex(self.value)

    def __format__(self, format_spec):
        if format_spec == "alg":
            return self._comma_sep_alg()
        raise ValueError(f"Unsupported format spec: \"{format_spec}\"")

    def __lt__(self, other):
        return self.is_proper_subset_of(SS(other))

    def __le__(self, other):
        return self.is_subset_of(SS(other))

    def __eq__(self, other):
        return self.value == SS(other).value

    def __ge__(self, other):
        return self.is_superset_of(SS(other))

    def __gt__(self, other):
        return self.is_proper_superset_of(SS(other))

    def _comma_sep_alg(self):
        return ",".join([sq.name for sq in self.squares()])

    def _init_from_str(self, initial: str):
        trimmed = [s.strip() for s in initial.split(",")]
        self._init_from_list(trimmed)

    def _init_from_list(self, initial: list) -> None:
        acc = util.int2ba(0, 64)
        for i, item in enumerate(initial):
            tipe = type(item)
            if tipe == SquareSet:
                acc |= item.value
            elif tipe in [frozenbitarray, bitarray]:
                acc |= item
            elif tipe == Square:
                acc |= item.mask
            elif tipe == int:
                acc |= util.int2ba(item, 64)
            else:
                try:
                    acc |= Square(item).mask
                except:
                    raise ValueError(f"item {i}: \"{item}\" can not be part of a SquareSet")
        self._value = frozenbitarray(acc)

    def squares(self) -> List[Square]:
        res = []
        for i in range(64):
            ba = util.int2ba(0, 64)
            ba.invert(i)
            if bool(ba & self.value):
                res.append(Square(i))
        return res

    def __str__(self) -> str:
        res = []
        for i in range(64):
            if not self.value[i]:
                continue
            res.append(Square(i).name)
        return "SS(" + ",".join(res) + ")"

    def __repr__(self) -> str:
        return self.__str__()

    def __hash__(self) -> int:
        return util.ba2int(self.value)

    def __sub__(self, other):
        return SS(self.value & ~SS(other).value)

    def __int__(self):
        return util.ba2int(self.value)

    def __iter__(self):
        for i, zeroOne in self.value:
            if not zeroOne:
                continue
            yield Square(i)

    def __len__(self):
        return self.count

    @property
    def count(self):
        return self.value.count(1)

    def __neg__(self):
        return SquareSet(~self.value)

    def __invert__(self):
        return SquareSet(~self.value)

    def intersect(self, other):
        return SS(self.value & SS(other).value)


SS = SquareSet

s = Dict()

s.all = [Square(i) for i in range(64)]
s.none = []
s.empty = []

s.starting.all = [sq for sq in s.all if sq.rank in [1, 2, 7, 8]]
s.starting.pawns = [sq for sq in s.all if sq.rank in [2, 7]]
s.starting.knights = [sq for sq in s.all if sq.name in "b1,g1,b8,g8"]
s.starting.bishops = [sq for sq in s.all if sq.name in "c1,f1,c8,f8"]
s.starting.rooks = [sq for sq in s.all if sq.name in "a1,h1,a8,h8"]
s.starting.queens = [SQ("d1"), SQ("d8")]
s.starting.kings = [SQ("e1"), SQ("e8")]

s.rank.r1 = [sq for sq in s.all if s.rank == 1]
s.rank.r2 = [sq for sq in s.all if s.rank == 2]
s.rank.r3 = [sq for sq in s.all if s.rank == 3]
s.rank.r4 = [sq for sq in s.all if s.rank == 4]
s.rank.r5 = [sq for sq in s.all if s.rank == 5]
s.rank.r6 = [sq for sq in s.all if s.rank == 6]
s.rank.r7 = [sq for sq in s.all if s.rank == 7]
s.rank.r8 = [sq for sq in s.all if s.rank == 8]

s.file.a = [sq for sq in s.all if sq.file == "a"]
s.file.b = [sq for sq in s.all if sq.file == "b"]
s.file.c = [sq for sq in s.all if sq.file == "c"]
s.file.d = [sq for sq in s.all if sq.file == "d"]
s.file.e = [sq for sq in s.all if sq.file == "e"]
s.file.f = [sq for sq in s.all if sq.file == "f"]
s.file.g = [sq for sq in s.all if sq.file == "g"]
s.file.h = [sq for sq in s.all if sq.file == "h"]

s.white.starting.all = [sq for sq in s.all if sq.rank in [1, 2]]
s.white.starting.king = SQ("e1")
s.white.starting.queen = SQ("d1")
s.white.starting.bishops = [SQ("c1"), SQ("f1")]
s.white.starting.knights = [SQ("b1"), SQ("g1")]
s.white.starting.rooks = [SQ("a1"), SQ("h1")]
s.white.starting.pawns = [sq for sq in s.all if sq.rank == 2]
s.white.promotion = [sq for sq in s.all if sq.rank == 8]
s.white.castling.short.blockable = [sq for sq in s.all if sq.name in "f1,g1"]
s.white.castling.short.checkable = [sq for sq in s.all if sq.name in "f1,g1"]
s.white.castling.short.king = [SQ("g1")]
s.white.castling.short.rook = [SQ("f1")]
s.white.castling.long.blockable = [sq for sq in s.all if sq.name in "d1, c1, b1"]
s.white.castling.long.checkable = [sq for sq in s.all if sq.name in "d1, c1"]
s.white.castling.long.king = [SQ("c1")]
s.white.castling.long.rook = [SQ("d1")]
s.white.squares = [sq for sq in s.all if sq.white]

s.black.starting.all = [sq for sq in s.all if sq.rank in [7, 8]]
s.black.starting.king = SQ("e8")
s.black.starting.queen = SQ("d8")
s.black.starting.bishops = [SQ("c8"), SQ("f8")]
s.black.starting.knights = [SQ("b8"), SQ("g8")]
s.black.starting.rooks = [SQ("a8"), SQ("h8")]
s.black.starting.pawns = [sq for sq in s.all if sq.rank == 2]
s.black.promotion = [sq for sq in s.all if sq.rank == 8]
s.black.castling.short.blockable = [sq for sq in s.all if sq.name in "f8,g8"]
s.black.castling.short.checkable = [sq for sq in s.all if sq.name in "f8,g8"]
s.black.castling.short.king = [SQ("g8")]
s.black.castling.short.rook = [SQ("f8")]
s.black.castling.long.blockable = [sq for sq in s.all if sq.name in "d8, c8, b8"]
s.black.castling.long.checkable = [sq for sq in s.all if sq.name in "d8, c8"]
s.black.castling.long.king = [SQ("c8")]
s.black.castling.long.rook = [SQ("d8")]
s.black.squares = [sq for sq in s.all if sq.black]

ss = Dict(s)


def _make_squaresets(root: Dict):
    for key, val in root.items():
        if type(val) in [SQ, list]:
            root[key] = SS(val)
        if type(val) == Dict:
            _make_squaresets(val)


_make_squaresets(ss)
