"""Tests for the roman_numerals package."""

import unittest

from roman_numerals import RomanNumeralError, from_int, to_int


class TestFromInt(unittest.TestCase):
    def test_basic_symbols(self):
        expected = {
            1: "I",
            5: "V",
            10: "X",
            50: "L",
            100: "C",
            500: "D",
            1000: "M",
        }
        for number, numeral in expected.items():
            with self.subTest(number=number):
                self.assertEqual(from_int(number), numeral)

    def test_subtractive_forms(self):
        expected = {
            4: "IV",
            9: "IX",
            40: "XL",
            90: "XC",
            400: "CD",
            900: "CM",
        }
        for number, numeral in expected.items():
            with self.subTest(number=number):
                self.assertEqual(from_int(number), numeral)

    def test_compound_values(self):
        expected = {
            3: "III",
            8: "VIII",
            14: "XIV",
            19: "XIX",
            39: "XXXIX",
            44: "XLIV",
            49: "XLIX",
            88: "LXXXVIII",
            99: "XCIX",
            399: "CCCXCIX",
            444: "CDXLIV",
            999: "CMXCIX",
            1994: "MCMXCIV",
            2024: "MMXXIV",
            3888: "MMMDCCCLXXXVIII",
            3999: "MMMCMXCIX",
        }
        for number, numeral in expected.items():
            with self.subTest(number=number):
                self.assertEqual(from_int(number), numeral)

    def test_rejects_zero(self):
        with self.assertRaises(RomanNumeralError):
            from_int(0)

    def test_rejects_negative(self):
        with self.assertRaises(RomanNumeralError):
            from_int(-1)

    def test_rejects_too_large(self):
        with self.assertRaises(RomanNumeralError):
            from_int(4000)

    def test_rejects_non_integer(self):
        for value in (1.5, "3", None):
            with self.subTest(value=value):
                with self.assertRaises(TypeError):
                    from_int(value)


class TestToInt(unittest.TestCase):
    def test_basic_symbols(self):
        expected = {
            "I": 1,
            "V": 5,
            "X": 10,
            "L": 50,
            "C": 100,
            "D": 500,
            "M": 1000,
        }
        for numeral, number in expected.items():
            with self.subTest(numeral=numeral):
                self.assertEqual(to_int(numeral), number)

    def test_subtractive_forms(self):
        expected = {
            "IV": 4,
            "IX": 9,
            "XL": 40,
            "XC": 90,
            "CD": 400,
            "CM": 900,
        }
        for numeral, number in expected.items():
            with self.subTest(numeral=numeral):
                self.assertEqual(to_int(numeral), number)

    def test_compound_values(self):
        expected = {
            "III": 3,
            "VIII": 8,
            "XIV": 14,
            "XIX": 19,
            "XXXIX": 39,
            "XLIV": 44,
            "XLIX": 49,
            "LXXXVIII": 88,
            "XCIX": 99,
            "CCCXCIX": 399,
            "CDXLIV": 444,
            "CMXCIX": 999,
            "MCMXCIV": 1994,
            "MMXXIV": 2024,
            "MMMDCCCLXXXVIII": 3888,
            "MMMCMXCIX": 3999,
        }
        for numeral, number in expected.items():
            with self.subTest(numeral=numeral):
                self.assertEqual(to_int(numeral), number)

    def test_ignores_surrounding_whitespace(self):
        self.assertEqual(to_int("  XIV\n"), 14)

    def test_rejects_empty_string(self):
        with self.assertRaises(RomanNumeralError):
            to_int("")

    def test_rejects_non_canonical_repetition(self):
        for numeral in ("IIII", "VV", "XXXX", "LL", "CCCC", "DD", "MMMM"):
            with self.subTest(numeral=numeral):
                with self.assertRaises(RomanNumeralError):
                    to_int(numeral)

    def test_rejects_invalid_order(self):
        for numeral in ("VX", "IL", "IC", "XD", "XM", "LC", "DM"):
            with self.subTest(numeral=numeral):
                with self.assertRaises(RomanNumeralError):
                    to_int(numeral)

    def test_rejects_non_string(self):
        for value in (123, None, ["X"]):
            with self.subTest(value=value):
                with self.assertRaises(TypeError):
                    to_int(value)


class TestRoundTrip(unittest.TestCase):
    def test_all_values_round_trip(self):
        for number in range(1, 4000):
            with self.subTest(number=number):
                numeral = from_int(number)
                self.assertEqual(to_int(numeral), number)
                self.assertEqual(from_int(to_int(numeral)), numeral)


if __name__ == "__main__":
    unittest.main()
