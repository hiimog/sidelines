import re
from typing import *

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

    def __iter__(self):
        for i in range(64):
            mask = 1 << i
            if self.value & mask:
                yield Square(i)

    def __contains__(self, item):
        if not item:
            return True
        if type(item) == SquareSet:
            return self.value & item.value == self.value
        if type(item) == Square:
            return self.value & item.mask
        return self.value & SquareSet(item).value

    def __len__(self):
        return self.value.bit_count()

    def __str__(self):
        algebraic = [s.name for s in iter(self)]
        return ",".join(algebraic)

    def __int__(self):
        return self.value

    def __eq__(self, other):
        if other is None:
            return False
        return self.value == SquareSet(other).value

    def __hex__(self):
        return hex(self.value)

    def __neg__(self):
        return SquareSet(~self.value)

    def __bool__(self):
        return bool(self.value)

    def __add__(self, other):
        return SquareSet(self.value | SquareSet(other).value)

    def __pos__(self):
        return self

    def __abs__(self):
        return self

    def __oct__(self):
        return oct(self.value)

    def __ceil__(self):
        return self

    def __copy__(self):
        return SquareSet(self)


    def __hash__(self):
        return self.value

    def __aiter__(self):
        return iter(self)

    def __long__(self):
        return self.value

    def __repr__(self):
        return f"SquareSet({self.value:08x})"

    def __bytes__(self):
        return bytes(self.value)

    def __delitem__(self, key):
        return SquareSet(self.value & ~SquareSet(key).value)

    def __and__(self, other):
        return SquareSet(self.value & SquareSet(other).value)


squares = frozenset([Square(i) for i in range(64)])
squareLookup = frozenset({s.name: s for s in squares})
