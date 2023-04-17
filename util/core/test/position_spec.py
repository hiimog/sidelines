import pytest
import dataclasses as dc
import chess as c
from core.square import *

def position_should_calculate_half_move_number():
    @dc.dataclass
    class Case:
        name: str
        value: int
        want: int