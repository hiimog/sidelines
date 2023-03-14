import functools
import re
from typing import *
from addict import Dict
from functools import total_ordering

ALGEBRAIC_REGEX = re.compile("^[a-h][1-8]$", re.I)
BLACK = "black"
EITHER = "either"
WHITE = "white"

SideNames = Literal["white", "black", "either"]

SquareConstructorType = Union[int, str, Tuple[int, int], Self]

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

SquareSetConstructorType = Union[Self, int, List, str, Square]


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
            self._init_from_list(initial)
        elif tipe == str:
            self._init_from_str(initial)
        elif tipe == Square:
            self._value = initial.mask
        else:
            self._value = Square(initial).mask
        if self._value < 0:
            self._value += 2**64

    @property
    def value(self):
        return self._value

    @property
    def inverse(self):
        return SquareSet(~self.value)

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
        return self.value == (other.value & self.value) and self.value != other.value

    def is_superset_of(self, other: any):
        other = SS(other)
        return other.value == (other.value & self.value)

    def has_superset(self, other: any):
        other = SS(other)
        return self.value == other.value & self.value

    def is_proper_superset_of(self, other: any):
        other = SS(other)
        return self.is_superset_of(other.value) and self.value != other.value

    def has_proper_superset(self, other: any):
        other = SS(other)
        return self.has_superset(other.value) and self.value != other.value

    def squares(self) -> List[Square]:
        return list(self)

    @property
    def count(self):
        return self.value.bit_count()

    def _comma_sep_alg(self):
        return ",".join([sq.name for sq in self.squares()])

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

    def _init_from_str(self, initial: str):
        trimmed = [sq.strip() for sq in initial.split(",")]
        self._init_from_list(trimmed)

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
        raise ValueError(f"Unsupported format spec: \"{format_spec}\"")

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

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return f"SS({self._comma_sep_alg()})"

    def __sub__(self, other):
        return SS(self.value & ~SS(other).value)


SS = SquareSet

s = Dict()

s.all = tuple([Square(i) for i in range(64)])
s.none = tuple([])
s.empty = tuple([])

s.starting.all = tuple([sq for sq in s.all if sq.rank in [1, 2, 7, 8]])
s.starting.pawns = tuple([sq for sq in s.all if sq.rank in [2, 7]])
s.starting.knights = tuple([sq for sq in s.all if sq.name in "b1,g1,b8,g8"])
s.starting.bishops = tuple([sq for sq in s.all if sq.name in "c1,f1,c8,f8"])
s.starting.rooks = tuple([sq for sq in s.all if sq.name in "a1,h1,a8,h8"])
s.starting.queens = tuple([SQ("d1"), SQ("d8")])
s.starting.kings = tuple([SQ("e1"), SQ("e8")])

s.rank.r1 = tuple([sq for sq in s.all if sq.rank == 1])
s.rank.r2 = tuple([sq for sq in s.all if sq.rank == 2])
s.rank.r3 = tuple([sq for sq in s.all if sq.rank == 3])
s.rank.r4 = tuple([sq for sq in s.all if sq.rank == 4])
s.rank.r5 = tuple([sq for sq in s.all if sq.rank == 5])
s.rank.r6 = tuple([sq for sq in s.all if sq.rank == 6])
s.rank.r7 = tuple([sq for sq in s.all if sq.rank == 7])
s.rank.r8 = tuple([sq for sq in s.all if sq.rank == 8])

s.file.a = tuple([sq for sq in s.all if sq.file == "a"])
s.file.b = tuple([sq for sq in s.all if sq.file == "b"])
s.file.c = tuple([sq for sq in s.all if sq.file == "c"])
s.file.d = tuple([sq for sq in s.all if sq.file == "d"])
s.file.e = tuple([sq for sq in s.all if sq.file == "e"])
s.file.f = tuple([sq for sq in s.all if sq.file == "f"])
s.file.g = tuple([sq for sq in s.all if sq.file == "g"])
s.file.h = tuple([sq for sq in s.all if sq.file == "h"])

s.white.starting.all = tuple([sq for sq in s.all if sq.rank in [1, 2]])
s.white.starting.king = SQ("e1")
s.white.starting.queen = SQ("d1")
s.white.starting.bishops = tuple([SQ("c1"), SQ("f1")])
s.white.starting.knights = tuple([SQ("b1"), SQ("g1")])
s.white.starting.rooks = tuple([SQ("a1"), SQ("h1")])
s.white.starting.pawns = tuple([sq for sq in s.all if sq.rank == 2])
s.white.promotion = tuple([sq for sq in s.all if sq.rank == 8])
s.white.castling.short.blockable = tuple([sq for sq in s.all if sq.name in "f1,g1"])
s.white.castling.short.checkable = tuple([sq for sq in s.all if sq.name in "f1,g1"])
s.white.castling.short.king = tuple([SQ("g1")])
s.white.castling.short.rook = tuple([SQ("f1")])
s.white.castling.long.blockable = tuple([sq for sq in s.all if sq.name in "d1, c1, b1"])
s.white.castling.long.checkable = tuple([sq for sq in s.all if sq.name in "d1, c1"])
s.white.castling.long.king = tuple([SQ("c1")])
s.white.castling.long.rook = tuple([SQ("d1")])
s.white.squares = tuple([sq for sq in s.all if sq.white])

s.black.starting.all = tuple([sq for sq in s.all if sq.rank in [7, 8]])
s.black.starting.king = SQ("e8")
s.black.starting.queen = SQ("d8")
s.black.starting.bishops = tuple([SQ("c8"), SQ("f8")])
s.black.starting.knights = tuple([SQ("b8"), SQ("g8")])
s.black.starting.rooks = tuple([SQ("a8"), SQ("h8")])
s.black.starting.pawns = tuple([sq for sq in s.all if sq.rank == 2])
s.black.promotion = tuple([sq for sq in s.all if sq.rank == 8])
s.black.castling.short.blockable = tuple([sq for sq in s.all if sq.name in "f8,g8"])
s.black.castling.short.checkable = tuple([sq for sq in s.all if sq.name in "f8,g8"])
s.black.castling.short.king = tuple([SQ("g8")])
s.black.castling.short.rook = tuple([SQ("f8")])
s.black.castling.long.blockable = tuple([sq for sq in s.all if sq.name in "d8, c8, b8"])
s.black.castling.long.checkable = tuple([sq for sq in s.all if sq.name in "d8, c8"])
s.black.castling.long.king = tuple([SQ("c8")])
s.black.castling.long.rook = tuple([SQ("d8")])
s.black.squares = tuple([sq for sq in s.all if sq.black])

ss = Dict(s)


def _make_squaresets(root: Dict):
    for key, val in root.items():
        if type(val) in [SQ, tuple]:
            root[key] = SS(val)
        if type(val) == Dict:
            _make_squaresets(val)


# turn squares or list[square] from s into SquareSets
_make_squaresets(ss)
