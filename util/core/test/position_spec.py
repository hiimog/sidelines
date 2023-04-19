import pytest
from dataclasses import dataclass
import chess as c

from core.position import Position
from core.square import *

def position_should_calculate_half_move_number():
    @dataclass
    class Case:
        name: str
        value: Callable[[], Position]
        want: int


    cases = [
        Case("initial position", lambda: Position.starting(), 1),
        Case("after 1. e4", lambda: Position.Builder().moves("e4").position, 2),
        Case("after 1. e5 e5", Position.Builder().moves(["e4", "e5"]).position, 3),
        Case("after 1. e4 e5 2. Nf3", Position.Builder().moves(["e4", "e5", "Nf3"]).position, 4),
        Case("after 1. e4 e5 2. Nf3 Nc6", Position.Builder().moves(["e4", "e5", "Nf3", "Nc6"]).position, 5),
    ]
