from typing import *

from core.square import *


class Position:
    def __init__(self,
                 is_white: bool,
                 white_pawns: SquareSet,
                 white_knights: SquareSet,
                 white_bishops: SquareSet,
                 white_rooks: SquareSet,
                 white_queens: SquareSet,
                 white_king: Square,
                 black_pawns: SquareSet,
                 black_knights: SquareSet,
                 black_bishops: SquareSet,
                 black_rooks: SquareSet,
                 black_queens: SquareSet,
                 black_king: Square,
                 ep_square: Square | None,
                 castling: Tuple[bool, bool, bool, bool],
                 half_move_clock: int,
                 full_move_number: int):
        self.is_white = is_white
        self.white_pawns = white_pawns
        self.white_knights = white_knights
        self.white_bishops = white_bishops
        self.white_rooks = white_rooks
        self.white_queens = white_queens
        self.white_king = white_king
        self.black_pawns = black_pawns
        self.black_knights = black_knights
        self.black_bishops = black_bishops
        self.black_rooks = black_rooks
        self.black_queens = black_queens
        self.black_king = black_king
        self.ep_square = ep_square
        self.castling = castling
        self.half_move_clock = half_move_clock
        self.full_move_number = full_move_number
        self.half_move_number = full_move_number * 2 + int(is_white)

    @classmethod
    def empty(cls) -> "Position":
        return Position(
            is_white=True,
            white_pawns=ss.white.starting.pawns,
            white_knights=ss.white.starting.knights,
            white_bishops=ss.white.starting.bishops,
            white_rooks=ss.white.starting.rooks,
            white_queens=ss.white.starting.queens,
            white_king=sq.white.starting.king,
            black_pawns=ss.black.starting.pawns,
            black_knights=ss.black.starting.knights,
            black_bishops=ss.black.starting.bishops,
            black_rooks=ss.black.starting.rooks,
            black_queens=ss.black.starting.queens,
            black_king=sq.black.starting.king,
            ep_square=None,
            castling=(True, True, True, True),
            half_move_clock=0,
            full_move_number=1
        )