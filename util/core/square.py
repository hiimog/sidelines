import re
from typing import *
from dataclasses import dataclass

SideNames = Union["white", "black", "both"]

algebraic_regex = re.compile("^[a-h][1-8]$", re.I)


class Square:
    def __init__(self, which: any = None):
        if which is None:
            self._idx = 0
        tipe = type(which)
        if tipe == int:
            self._idx = which
            if not self._is_valid():
                raise ValueError("int must be 0<=X<=63")
        elif tipe == Tuple[int, int]:
            row, col = which
            self._idx = row * 8 + col
            if not self._is_valid():
                raise ValueError("2-tuple must have values 0<=X<=63")
        elif tipe == str:
            which = which.lower()
            if not algebraic_regex.search(which):
                raise ValueError("algebraic form only")
            row = int(which[1]) - 1
            col = "abcdefgh".index(which[0])
            self._idx = row * 8 + col
        elif tipe == Square:
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
    def rank(self):
        return self.row + 1

    @property
    def file(self):
        return "abcdefgh"[self.col]

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

    def is_promotion(self, sides: SideNames = "both"):
        if sides == "white":
            return self.row == 7
        if sides == "black":
            return self.row == 0
        if sides == "both":
            return self.row == 0 or self.row == 7
        raise ValueError("sides must be white, black, or both")

    def __str__(self):
        return self.name

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


class SquareSet:
    def __init__(self, initial: any = None):
        self._value = 0
        if initial is None:
            return
        tipe = type(initial)
        if tipe == SquareSet:
            self._value = initial.value
        elif tipe == list:
            self._init_from_list(initial)
        elif tipe == Square:
            self._value = initial.mask
        elif tipe == int:
            self._value = initial

    @property
    def value(self):
        return self._value

    def _init_from_list(self, initial: list) -> None:
        acc = 0
        for item in initial:
            tipe = type(item)
            if tipe == SquareSet:
                acc |= item.value
            elif tipe == Square:
                acc |= item.mask
            elif tipe == int:
                acc |= item
        self._value = acc

    def squares(self) -> List[Square]:
        for i in range(64):
            mask = 1 << i
            if self._value & mask:
                yield Square(i)

    def __contains__(self, item):
        if item is None:
            return True
        tipe = type(item)
        if tipe == SquareSet:
            return self.value & item.value == self.value


squares = [Square(i) for i in range(64)]
squareLookup = {s.name: s for s in squares}
