import unittest
from dataclasses import dataclass
from core.square import *


class SquareShould(unittest.TestCase):
    def get_correct_square_color(self):
        @dataclass
        class TestCase:
            name: str
            square: Square
            want: bool

        test_data = [
            TestCase("a1 is black", squareLookup["a1"], False),
            TestCase("a2 is white", squareLookup["a2"], True),
            TestCase("b1 is white", squareLookup["b1"], True),
            TestCase("h8 is black", squareLookup["h8"], False),
            TestCase("h1 is white", squareLookup["h1"], True),
        ]
        for i, t in enumerate(test_data):
            self.assertEqual(t.square.white, t.want, f"Test case failure: {i}) {t.name}")


if __name__ == '__main__':
    unittest.main()
