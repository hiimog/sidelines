from functools import reduce
from typing import *

"""
Notes:
- Moves can be illegal XOR (pseudo legal OR legal)
- Pseudo legal analysis does not consider if the move leaves the king in check
- Position << Move = Position'
- Positions have concepts like check, stalemate, etc moves do not
"""


class MoveAnalysis:
    next_analysis_id: int = 0

    def __init__(self, name: str, desc: str, is_legal: bool = True):
        self.id = MoveAnalysis.next_analysis_id
        MoveAnalysis.next_analysis_id += 1
        self.mask = 1 << self.id
        self.name = name
        self.desc = desc
        self.is_legal = is_legal


class MoveAnalysisGroup:
    def __init__(self, name: str, desc: str, analyses: List[MoveAnalysis]):
        if not analyses:
            raise ValueError("MoveAnalysisGroup must have members")
        self.name = name
        self.desc = desc
        self.analyses = analyses
        self.mask = reduce(lambda a, b: a | b.mask, analyses, 0)


pawn_capture = MoveAnalysis("PawnCapture", "Move captures an enemy pawn")
knight_capture = MoveAnalysis("KnightCapture", "Move captures an enemy knight")
bishop_capture = MoveAnalysis("KnightCapture", "Move captures an enemy bishop")
rook_capture = MoveAnalysis("KnightCapture", "Move captures an enemy rook")
queen_capture = MoveAnalysis("KnightCapture", "Move captures an enemy queen")

pawn_move = MoveAnalysis("PawnMove", "Pawn is the moved piece")
pawn_move_two = MoveAnalysis("PawnMoveTwo", "Pawn moves 2 squares from the starting rank")
promotion = MoveAnalysis("Promotion", "Pawn move to the final rank")
under_promotion = MoveAnalysis("UnderPromotion", "Promotion to something other than a queen")
en_passant = MoveAnalysis("EnPassant",
                          "Pawn capture on an enemy pawn to its left or right as a result of the enemy pawn moving "
                          "2 squares to start")
illegal_promotion_target_square = MoveAnalysis("IllegalPromotionTargetSquare",
                                               "Promotion attempted on a square not on final rank", is_legal=False)
illegal_promotion_target_piece = MoveAnalysis("IllegalPromotionTargetPiece", "Promotion attempted to pawn or king",
                                              is_legal=False)
illegal_promotion_source_piece = MoveAnalysis("IllegalPromotionSourcePiece", "Promotion attempted from a non-pawn",
                                              is_legal=False)
missed_promotion = MoveAnalysis("MissedPromotion", "Pawn move to final rank but without promotion", is_legal=False)

knight_move = MoveAnalysis("KnightMove", "Knight is the moved piece")
bishop_move = MoveAnalysis("BishopMove", "Bishop is the moved piece")
rook_move = MoveAnalysis("RookMove", "Rook is the moved pieced")
queen_move = MoveAnalysis("QueenMove", "Queen is the moved piece")
king_move = MoveAnalysis("KingMove", "King is the moved piece")
castle_short = MoveAnalysis("CastleShort", "Castle is performed to the king side")
castle_long = MoveAnalysis("CastleLong", "Castle is performed to the queen side")
castle_rights_lost_ally_short = MoveAnalysis("CastleRightsLostAllyShort", "Ally can no longer castle short")
castle_rights_lost_ally_long = MoveAnalysis("CastleRightsLostAllyLong", "Ally can no longer castle long")
castle_rights_lost_enemy_short = MoveAnalysis("CastleRightsLostEnemyShort", "Enemy can no longer castle short")
castle_rights_lost_enemy_long = MoveAnalysis("CastleRightsLostEnemyLong", "Enemy can no longer castle long")
illegal_castle_blocked = MoveAnalysis("IllegalCastleBlocked", "A piece is between the king and rook trying to castle",
                                      is_legal=False)
illegal_castle_through_check = MoveAnalysis("IllegalCastleThroughCheck",
                                            "The start, middle, or ending square of the king trying to castle is "
                                            "attacked by an enemy piece", is_legal=False)
illegal_castle_no_rights = MoveAnalysis("IllegalCastleNoRights",
                                        "Castling rights have been lost for the attempted castle", is_legal=False)
illegal_castle_arrangement = MoveAnalysis("IllegalCastleArrangement",
                                          "Position is detected where castling rights do not reflect the position e.g. "
                                          "misplaced castling rook", is_legal=False)

illegal_move_geometry = MoveAnalysis("IllegalMoveGeometry", "Piece move in a way not allowed by rules", is_legal=False)
illegal_move_blocked = MoveAnalysis("IllegalMoveBlocked", "Attempt to move piece through another a piece",
                                    is_legal=False)
illegal_move_turn = MoveAnalysis("IllegalMoveTurn", "Attempt to move enemy piece", is_legal=False)

all_move_analyses: List[MoveAnalysis] = [v for k, v in locals().items() if type(v) == MoveAnalysis]

illegal_group = MoveAnalysisGroup("IllegalGroup", "Any move that is illegal",
                                  [m for m in all_move_analyses if not m.is_legal])

illegal_pawn_group = MoveAnalysisGroup("IllegalPawnGroup", "Any pawn move that is illegal", [
    illegal_promotion_target_square,
    illegal_promotion_target_piece,
    missed_promotion,
])

capture_group = MoveAnalysisGroup("CaptureGroup", "Any move that is a capture", [
    pawn_capture,
    en_passant,
    knight_capture,
    bishop_capture,
    rook_capture,
    queen_capture
])

pawn_move_group = MoveAnalysisGroup("PawnMoveGroup", "All analyses that involve a pawn", [
    pawn_move,
    pawn_move_two,
    promotion,
    under_promotion,
    en_passant,
])

sliding_piece_group = MoveAnalysisGroup("SlidingPieceGroup", "Rook, bishop, and queen moves", [
    rook_move,
    bishop_move,
    queen_move,
])

castle_group = MoveAnalysisGroup("CastleGroup", "Analyses related to castling", [
    castle_long,
    castle_short,
    castle_rights_lost_ally_long,
    castle_rights_lost_ally_short,
    castle_rights_lost_enemy_long,
    castle_rights_lost_enemy_short,
])

illegal_castle_group = MoveAnalysisGroup("IllegalCastleGroup", "Analyses for illegal castling", [
    illegal_castle_no_rights,
    illegal_castle_blocked,
    illegal_castle_through_check,
    illegal_castle_arrangement,
])


def is_pseudo_legal(analysis: MoveAnalysis) -> bool:
    return not bool(analysis.mask & illegal_group.mask)


class PositionAnalysis:
    next_id: int = 0

    def __init__(self, name: str, desc: str, is_quick: bool = True, is_legal: bool = True):
        self.id = PositionAnalysis.next_id
        PositionAnalysis.next_id += 1
        self.mask = 1 << self.id
        self.name = name
        self.desc = desc
        self.is_quick = is_quick
        self.is_legal = is_legal


class PositionAnalysisGroup:
    def __init__(self, name: str, desc: str, analyses: List[PositionAnalysis]):
        if not analyses:
            raise ValueError("Analyses must be provided")
        self.name = name
        self.desc = desc
        self.analyses = analyses
        self.mask = reduce(lambda a, b: a | b.mask, analyses, 0)


check = PositionAnalysis("Check", "Side with the move is in check", is_quick=True, is_legal=True)
double_check = PositionAnalysis("DoubleCheck", "Side with the move is checked twice", is_quick=True, is_legal=True)
checkmate = PositionAnalysis("Checkmate", "Side with the move is in checkmate", is_quick=False, is_legal=True)
stalemate = PositionAnalysis("Stalemate", "Side with the move can make no legal moves", is_quick=False, is_legal=True)
insufficient_material = PositionAnalysis("InsufficientMaterial", "Neither side has enough material to mate the other",
                                         is_quick=True, is_legal=True)
kings_touching = PositionAnalysis("KingsTouching", "Kings are not separated by at least 1 square", is_quick=True,
                                  is_legal=False)
incorrect_king_count = PositionAnalysis("IncorrectKingCount", "Each side must have exactly 1 king", is_quick=True,
                                        is_legal=False)
incorrect_pawn_count = PositionAnalysis("IncorrectPawnCount", "A side can have at most 8 pawns", is_quick=True,
                                        is_legal=False)
too_many_checks = PositionAnalysis("TooManyChecks", "Either king is attacked 3 or more times", is_quick=True,
                                   is_legal=False)
enemy_in_check = PositionAnalysis("EnemyInCheck", "Enemy side is in check already, meaning they did not get out of "
                                                  "check on their turn", is_quick=True, is_legal=False)
pawn_on_end_ranks = PositionAnalysis("PawnOnEndRanks", "A pawn is on the 1st or 8th rank", is_quick=True,
                                     is_legal=False)
illogical_castling_rights = PositionAnalysis("IllogicalCastlingRights", "Any position where the ally has castling "
                                                                        "rights that should not be possible",
                                             is_quick=True, is_legal=False)
illogical_ep_square = PositionAnalysis("IllogicalEpSquare", "En passant square is not on the 3rd or 6th rank, there is "
                                                            "a piece in the way, or there is no corresponding pawn",
                                       is_quick=True, is_legal=False)

all_pos_analyses: List[PositionAnalysis] = [v for k, v in locals().items() if type(v) == PositionAnalysis]

illegal_pos_group = PositionAnalysisGroup("IllegalGroup", "Any position that is illegal",
                                          [m for m in all_pos_analyses if not m.is_legal])

game_over_group = PositionAnalysisGroup("GameOverGroup", "Game has come to an end", [
    checkmate,
    stalemate,
    insufficient_material
])
