from typing import *

SideNames = Union["white", "black", "both"]


class Square:
    def __init__(self, idx: int):
        if idx < 0 or idx > 63:
            raise ValueError("Square index can only be in the range [0,64)")
        self.idx = idx

    @property
    def row(self):
        return self.idx // 8

    @property
    def col(self):
        return self.idx % 8

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
        return 1 << self.idx

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


squares = [Square(i) for i in range(64)]
