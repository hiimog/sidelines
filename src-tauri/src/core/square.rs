use std::fmt::{Debug, Formatter};
use std::ops::Index;
use serde::Serialize;

#[derive(Copy, Clone, Ord, PartialOrd, Eq, PartialEq, Hash)]
struct Square {
    index: u8,
}

struct SquareSet {
    mask: u64,
}

enum Squarish {
    U8(u8),
    STR(str),
    SS(SquareSet),
    SQ(Square),
}

enum Setish {
    U64(u64),
    SQ(Square),
    SS(SquareSet),
    STR(str),
    VEC(Vec<Squarish>)

}

impl Square {
    fn from(initializer: Squarish) -> Result<Square, Err> {
        match initializer {
            Squarish::U8(u) => match u {
                0..=63 => Ok(Square{index:u}),
                _ => Err("Square can only be created from 0 <= u8 <= 63")
            },
            Squarish::SQ(s) => s,
            Squarish::STR(s) => {
                if s.len() != 2 { Err("Square can only be created from 2 character strings")}
                let file: char = s[0];
                let rank: char = s[1];
                let col = match file {
                    'a'..='h' => u8::from(file - 'a'),
                    'A'..='H' => u8::from(file - 'A'),
                    _ => Err("Square first letter must be a-hA-H")
                }?;
                let row = match rank {
                    '1'..='8' => u8::from_char(row - '1'),
                    _ => Err("Square row must be 1-8")
                };
                row * 8 + col
            },
            Squarish::SS(ss) => {
                if ss.mask.is_power_of_two() { Square { index: u8::from(ss.mask.trailing_zeros())}}
                Err("Square can only be created from square set with exactly 1 square set")
            }
        }
    }

    fn rc(&self) -> (u8, u8) { (self.index / 8, self.index % 8) }
    fn rf(&self) -> (u8, char) { (self.index / 8 + 1, "abcdefgh"[self.index % 8])}
}

impl ToString for Square {
    fn to_string(&self) -> String {
        let (rank, file) = self.rf();
        return String::from(format!("{}{}", file, rank))
    }
}
