from typing import *


class MoveAnalysis:
    def __init__(self, name: str, desc: str):
        self.val = 0  # to be set by auto assign process
        self.name = name
        self.desc = desc
        self._children: List[MoveAnalysis] = []


PawnMove = MoveAnalysis("PawnMove", "Any move where a pawn was moved")
KnightMove = MoveAnalysis("PawnMove", "Any move where a knight was moved")
Bishop = MoveAnalysis("PawnMove", "Any move where a bishop was moved")
Rook = MoveAnalysis("PawnMove", "Any move where a rook was moved")
Queen = MoveAnalysis("PawnMove", "Any move where a queen was moved")
King = MoveAnalysis("PawnMove", "Any move where a king was moved")
