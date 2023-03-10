import re
from typing import *
from addict import Dict

ALGEBRAIC_REGEX = re.compile("^[a-h][1-8]$", re.I)
WHITE = "white"
BLACK = "black"
EITHER = "either"
SideNames = Literal["white", "black", "either"]


class Square:
    def __init__(self, which: any = None):
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
        return 0 <= self._idx <= 63

    @property
    def index(self):
        return self._idx

    @property
    def row(self):
        return self._idx // 8

    @property
    def col(self):
        return self._idx % 8

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
        return 1 << self._idx

    @property
    def smask(self):
        return f"{self.mask:063b}"

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
        return f"Square({self._idx})"

    def __int__(self):
        return self._idx

    def __eq__(self, other):
        if other is None:
            return False
        tipe = type(other)
        if tipe == int:
            return self._idx == other
        if tipe == Square:
            return self._idx == other.index
        if tipe == str:
            return self.name == other.lower()
        return False


class SquareSet:
    def __init__(self, initial: any = None):
        self._value = 0
        if initial is None:
            return
        tipe = type(initial)
        if tipe == SquareSet:
            self._value = initial.value
        elif tipe == int:
            self._value = initial
        elif tipe == list:
            self._init_from_list(initial)
        elif tipe == str:
            self._init_from_str(initial)
        elif tipe == Square:
            self._value = initial.mask
        else:
            try:
                self._value = Square(initial).mask
            except:
                raise ValueError("Unsupported constructor value")

    @property
    def inverse(self):
        return SquareSet(~self.value)

    @property
    def as_bool(self):
        return bool(self.value)

    @property
    def as_int(self):
        return self.value

    def union(self, other: any):
        return SquareSet(self.value | SquareSet(other).value)

    def intersect(self, other: any):
        return SquareSet(self.value & SquareSet(other).value)

    def difference(self, other: any):
        return SquareSet(self.value & ~SquareSet(other).value)

    def is_subset_of(self, other: any):
        return self.value == (self.value & SquareSet(other).value)

    def is_subset(self, other: any):
        other = SquareSet(other)
        return other.value == (self.value & other.value)

    def is_proper_subset_of(self, other: any):
        other = SquareSet(other)
        return self.is_subset_of(other) and self.value != other.value

    def is_proper_subset(self, other: any):
        other = SquareSet(other).value
        return self.value == (other & self.value) and self.value != other

    def is_superset_of(self, other: any):
        other = SquareSet(other)
        return other.value == (other.value & self.value)

    def is_superset(self, other: any):
        return self.value == (SquareSet(other).value & self.value)

    def is_proper_superset_of(self, other: any):
        return self.is_superset_of(other) and self.value != SquareSet(other).value

    def is_proper_superset(self, other: any):
        return self.is_superset(other) and self.value != SquareSet(other).value

    def __add__(self, other):
        return self.union(other)

    def __and__(self, other):
        return self.intersect(other)

    def __bool__(self):
        return bool(self.value)

    def __bytes__(self):
        return bytes(self.value)

    def __contains__(self, item):
        return self.is_superset_of(item)

    def __copy__(self):
        return SquareSet(self.value)

    def __ge__(self, other):
        return self.is_superset_of(other)

    def __gt__(self, other):
        return self.is_proper_superset_of(other)

    def __hex__(self):
        return hex(self.value)

    @property
    def value(self):
        return self._value

    def _init_from_str(self, initial: str):
        trimmed = [s.strip() for s in initial.split(",")]
        self._init_from_list(trimmed)

    def _init_from_list(self, initial: list) -> None:
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
                except:
                    raise ValueError(f"item {i}: \"{item}\" can not be part of a SquareSet")
        self._value = acc

    def squares(self) -> List[Square]:
        return list(self)

    def __eq__(self, o: object) -> bool:
        return super().__eq__(o)

    def __ne__(self, o: object) -> bool:
        return super().__ne__(o)

    def __str__(self) -> str:
        return super().__str__()

    def __repr__(self) -> str:
        return super().__repr__()

    def __hash__(self) -> int:
        return super().__hash__()



s = Dict()

s.all = [Square(i) for i in range(64)]
s.none = []
s.empty = []

s.starting.white = [sq for sq in s.all if sq.rank in [1,2]]
s.starting.white.king = Square("e1")
s.starting.white.queen = Square("d1")
s.starting.white.bishops = [Square("c1"), Square("f1")]
s.starting.white.knights = [Square("b1"), Square("g1")]
s.starting.white.rooks = [Square("a1"), Square("h1")]
s.starting.white.pawns = [sq for sq in s.all if sq.rank == 2]
s.starting.black = [sq for sq in s.all if sq.rank in [7,8]]
s.starting.black.king = Square("e8")
s.starting.black.queen = Square("d8")
s.starting.black.bishops = [Square("c8"), Square("f8")]
s.starting.black.knights = [Square("b8"), Square("g8")]
s.starting.black.rooks = [Square("a8"), Square("h8")]
s.starting.black.pawns = [sq for sq in s.all if sq.rank == 7]
s.starting.pawns = [sq for sq in s.all if sq.rank in [2,7]]
s.starting.knights = [sq for sq in s.all if sq.name in "b1,g1,b8,g8"]
s.starting.bishops = [sq for sq in s.all if sq.name in "c1,f1,c8,f8"]
s.starting.rooks = [sq for sq in s.all if sq.name in "a1,h1,a8,h8"]
s.starting.queens = [Square("d1"), Square("d8")]
s.starting.kings = [Square("e1"), Square("e8")]
s.white.promotion = [sq for sq in s.all if sq.rank == 8]
s.white.castling.short.blockable = [sq for sq in s.all if s.name in "f1,g1"]
s.white.castling.short.checkable = [sq for sq in s.all if s.name in "f1,g1"]
s.white.castling.short.king = [Square("g1")]
s.white.castling.short.rook = [Square("f1")]





s.black.promotion = [sq for sq in s.all if sq.rank == 1]
s.rank._1 = [sq for sq in s.all if s.rank == 1]
s.rank._2 = [sq for sq in s.all if s.rank == 2]
s.rank._3 = [sq for sq in s.all if s.rank == 3]
s.rank._4 = [sq for sq in s.all if s.rank == 4]
s.rank._5 = [sq for sq in s.all if s.rank == 5]
s.rank._6 = [sq for sq in s.all if s.rank == 6]
s.rank._7 = [sq for sq in s.all if s.rank == 7]
s.rank._8 = [sq for sq in s.all if s.rank == 8]
s.file.a = [sq for sq in s.all if sq.file == "a"]
s.file.b = [sq for sq in s.all if sq.file == "b"]
s.file.c = [sq for sq in s.all if sq.file == "c"]
s.file.d = [sq for sq in s.all if sq.file == "d"]
s.file.e = [sq for sq in s.all if sq.file == "e"]
s.file.f = [sq for sq in s.all if sq.file == "f"]
s.file.g = [sq for sq in s.all if sq.file == "g"]
s.file.h = [sq for sq in s.all if sq.file == "h"]


