from typing import *
from dataclasses import dataclass

SideNames = Union["white", "black", "both"]


class Square:
    def __init__(self, idx: int):
        if idx < 0 or idx > 63:
            raise ValueError("Square index can only be in the range [0,64)")
        self._idx = idx

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
    def __init__(self, initial: any):
        self.value = 0
        tipe = type(initial)
        if tipe == SquareSet:
            self.value = initial.value
        elif tipe == list:
            self._init_from_list(initial)
        elif tipe == Square:
            self.value = initial.mask
        elif tipe == int:
            self.value = initial

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
        self.value = acc

    def squares(self) -> List[Square]:
        for i in range(64):
            mask = 1 << i
            if self.value & mask:
                yield Square(i)


squares = [Square(i) for i in range(64)]
squareLookup = {s.name: s for s in squares}

