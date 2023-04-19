from dataclasses import dataclass

@dataclass
class PieceType:
    name: str
    worth: int
    white_letter: str
    black_letter: str

@dataclass
class Piece:
    name: str
    letter: str
    type: PieceType

PAWN = PieceType("pawn", 1, "P", "p")
KNIGHT = PieceType("knight", 3, "N", "n")
BISHOP = PieceType("bishop", 3, "B", "b")
ROOK = PieceType("rook", 5, "R", "r")
QUEEN = PieceType("quene", 9, "Q", "q")
KING = PieceType("king", 10, "K", "k")

WHITE_PAWN = Piece("white pawn", PAWN.white_letter, PAWN)
WHITE_KNIGHT = Piece("white knight", KNIGHT.white_letter, KNIGHT)
WHITE_BISHOP = Piece("white bishop", PAWN.white_letter, BISHOP)
WHITE_ROOK = Piece("white rook", PAWN.white_letter, ROOK)
WHITE_QUEEN = Piece("white queen", PAWN.white_letter, QUEEN)
WHITE_KING = Piece("white king", PAWN.white_letter, KING)
