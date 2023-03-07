import pytest
from dataclasses import dataclass
import chess as c
from core.square import *


def square_should_be_constructible():
    @dataclass()
    class Case:
        name: str
        value: any
        want: int

    dummy = Square()
    dummy._idx = 42
    cases = [
        Case("None", None, 0),
        Case("int", 42, 42),
        Case("Algebraic notation", "e4", c.parse_square("e4")),
        Case("Row and col", (1, 2), c.parse_square("c2")),
        Case("Another square", dummy, 42),
    ]
    for case in cases:
        try:
            sq = Square(case.value)
        except:
            pytest.fail(f"'{case.name}' raised unexpectedly", True)
        assert sq.index == case.want, f"'{case.name}' can be used to construct a Square"
