from dataclasses import dataclass
from typing import *

from core.magics import *
from core.square import SS, SQ


@dataclass
class Magic:
    attack_mask: SS
    attacks: List[SS]
    magic_num: int
    shift: int
    square_idx: int


KNIGHT_ATTACKS = [
    SS(0x20400),
    SS(0x50800),
    SS(0xa1100),
    SS(0x142200),
    SS(0x284400),
    SS(0x508800),
    SS(0xa01000),
    SS(0x402000),
    SS(0x2040004),
    SS(0x5080008),
    SS(0xa110011),
    SS(0x14220022),
    SS(0x28440044),
    SS(0x50880088),
    SS(0xa0100010),
    SS(0x40200020),
    SS(0x204000402),
    SS(0x508000805),
    SS(0xa1100110a),
    SS(0x1422002214),
    SS(0x2844004428),
    SS(0x5088008850),
    SS(0xa0100010a0),
    SS(0x4020002040),
    SS(0x20400040200),
    SS(0x50800080500),
    SS(0xa1100110a00),
    SS(0x142200221400),
    SS(0x284400442800),
    SS(0x508800885000),
    SS(0xa0100010a000),
    SS(0x402000204000),
    SS(0x2040004020000),
    SS(0x5080008050000),
    SS(0xa1100110a0000),
    SS(0x14220022140000),
    SS(0x28440044280000),
    SS(0x50880088500000),
    SS(0xa0100010a00000),
    SS(0x40200020400000),
    SS(0x204000402000000),
    SS(0x508000805000000),
    SS(0xa1100110a000000),
    SS(0x1422002214000000),
    SS(0x2844004428000000),
    SS(0x5088008850000000),
    SS(0xa0100010a0000000),
    SS(0x4020002040000000),
    SS(0x400040200000000),
    SS(0x800080500000000),
    SS(0x1100110a00000000),
    SS(0x2200221400000000),
    SS(0x4400442800000000),
    SS(0x8800885000000000),
    SS(0x100010a000000000),
    SS(0x2000204000000000),
    SS(0x4020000000000),
    SS(0x8050000000000),
    SS(0x110a0000000000),
    SS(0x22140000000000),
    SS(0x44280000000000),
    SS(0x88500000000000),
    SS(0x10a00000000000),
    SS(0x20400000000000),
]

KING_ATTACKS = [
    SS(0x302),
    SS(0x705),
    SS(0xe0a),
    SS(0x1c14),
    SS(0x3828),
    SS(0x7050),
    SS(0xe0a0),
    SS(0xc040),
    SS(0x30203),
    SS(0x70507),
    SS(0xe0a0e),
    SS(0x1c141c),
    SS(0x382838),
    SS(0x705070),
    SS(0xe0a0e0),
    SS(0xc040c0),
    SS(0x3020300),
    SS(0x7050700),
    SS(0xe0a0e00),
    SS(0x1c141c00),
    SS(0x38283800),
    SS(0x70507000),
    SS(0xe0a0e000),
    SS(0xc040c000),
    SS(0x302030000),
    SS(0x705070000),
    SS(0xe0a0e0000),
    SS(0x1c141c0000),
    SS(0x3828380000),
    SS(0x7050700000),
    SS(0xe0a0e00000),
    SS(0xc040c00000),
    SS(0x30203000000),
    SS(0x70507000000),
    SS(0xe0a0e000000),
    SS(0x1c141c000000),
    SS(0x382838000000),
    SS(0x705070000000),
    SS(0xe0a0e0000000),
    SS(0xc040c0000000),
    SS(0x3020300000000),
    SS(0x7050700000000),
    SS(0xe0a0e00000000),
    SS(0x1c141c00000000),
    SS(0x38283800000000),
    SS(0x70507000000000),
    SS(0xe0a0e000000000),
    SS(0xc040c000000000),
    SS(0x302030000000000),
    SS(0x705070000000000),
    SS(0xe0a0e0000000000),
    SS(0x1c141c0000000000),
    SS(0x3828380000000000),
    SS(0x7050700000000000),
    SS(0xe0a0e00000000000),
    SS(0xc040c00000000000),
    SS(0x203000000000000),
    SS(0x507000000000000),
    SS(0xa0e000000000000),
    SS(0x141c000000000000),
    SS(0x2838000000000000),
    SS(0x5070000000000000),
    SS(0xa0e0000000000000),
    SS(0x40c0000000000000),
]

BISHOP_MAGICS = []
for i in range(64):
    lo = BISHOP_OFFSETS[i]
    hi = BISHOP_OFFSETS[i + 1] if i < 63 else int("inf")
    square_attacks = BISHOP_ATTACK_TABLE[lo:hi]
    magic_num = BISHOP_MAGIC_NUMS[i]
    shift = BISHOP_SHIFTS[i]
    mask = BISHOP_MASKS[i]
    BISHOP_MAGICS.append(Magic(mask, square_attacks, magic_num, shift, i))

ROOK_MAGICS = []
for i in range(64):
    lo = ROOK_OFFSETS[i]
    hi = ROOK_OFFSETS[i + 1] if i < 63 else int("inf")
    square_attacks = ROOK_ATTACK_TABLE[lo:hi]
    magic_num = ROOK_MAGIC_NUMS[i]
    shift = ROOK_SHIFTS[i]
    mask = ROOK_MASKS[i]
    ROOK_MAGICS.append(Magic(mask, square_attacks, magic_num, shift, i))


def knight_attacks(location: SQ) -> SS:
    return KNIGHT_ATTACKS[location.idx]


def king_attacks(location: SQ) -> SS:
    return KING_ATTACKS[location.idx]


def bishop_attacks(location: SQ, occupied: SS) -> SS:
    magic = BISHOP_MAGICS[location.idx]
    index = (magic.magic_num * (occupied.value & magic.attack_mask)) >> (64 - magic.shift)
    return magic.attacks[index]


def rook_attacks(location: SQ, occupied: SS) -> SS:
    magic = ROOK_MAGICS[location.idx]
    index = (magic.magic_num * (occupied.value & magic.attack_mask)) >> (64 - magic.shift)
    return magic.attacks[index]


def queen_attacks(location: SQ, occupied: SS) -> SS:
    return bishop_attacks(location, occupied) | rook_attacks(location, occupied)
