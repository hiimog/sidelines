from dataclasses import dataclass

from core.piece import PieceType
from core.square import Square


@dataclass
class Move:
    frm: Square
    to: Square
    prom: PieceType | None
