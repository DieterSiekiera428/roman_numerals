"""Core conversion routines for Roman numerals.

The implementation uses the standard subtractive notation:
    I=1, V=5, X=10, L=50, C=100, D=500, M=1000
and the canonical forms such as IV for 4, IX for 9, XL for 40, etc.

Only integers in the closed interval [1, 3999] are supported.  Zero
and negative numbers have no conventional Roman numeral representation
in this notation, and values above 3999 require an extension such as
the apostrophus or vinculum, which this library deliberately omits in
order to keep the API small and predictable.
"""

from __future__ import annotations

from typing import Tuple

__all__ = ["from_int", "to_int"]

# Value-to-symbol pairs ordered from largest to smallest.  The pairs
# are deliberately listed in descending order so that a single forward
# scan can build the numeral without sorting or additional lookups.
_NUMERALS: Tuple[Tuple[int, str], ...] = (
    (1000, "M"),
    (900, "CM"),
    (500, "D"),
    (400, "CD"),
    (100, "C"),
    (90, "XC"),
    (50, "L"),
    (40, "XL"),
    (10, "X"),
    (9, "IX"),
    (5, "V"),
    (4, "IV"),
    (1, "I"),
)


class RomanNumeralError(ValueError):
    """Raised when a value cannot be converted to or from Roman numerals."""


def from_int(number: int) -> str:
    """Convert an integer in [1, 3999] to its Roman numeral representation.

    Args:
        number: The integer to convert.

    Returns:
        The Roman numeral string, using only the characters I, V, X, L,
        C, D, and M.

    Raises:
        TypeError: If *number* is not an integer.
        RomanNumeralError: If *number* is outside the supported range.
    """

    if not isinstance(number, int):
        raise TypeError(f"Expected int, got {type(number).__name__}")

    if not 1 <= number <= 3999:
        raise RomanNumeralError(
            "Only integers between 1 and 3999 can be represented "
            "in standard Roman numerals"
        )

    result: list[str] = []
    remaining = number

    for value, symbol in _NUMERALS:
        count = remaining // value
        if count:
            result.append(symbol * count)
            remaining %= value

    return "".join(result)


def to_int(roman: str) -> int:
    """Convert a Roman numeral string to its integer value.

    Args:
        roman: The Roman numeral to parse.  Leading and trailing
            whitespace is ignored.  The input must be a syntactically
            valid, canonical Roman numeral in the range [1, 3999].

    Returns:
        The integer value represented by *roman*.

    Raises:
        TypeError: If *roman* is not a string.
        RomanNumeralError: If *roman* is empty, contains invalid
            characters, uses non-canonical forms (such as "IIII" for 4
            or "VX" for 5), or represents a value outside [1, 3999].
    """

    if not isinstance(roman, str):
        raise TypeError(f"Expected str, got {type(roman).__name__}")

    text = roman.strip()
    if not text:
        raise RomanNumeralError("Roman numeral string must not be empty")

    value = 0
    index = 0
    n = len(text)

    while index < n:
        # Try to match a two-character subtractive form first, since
        # those pairs are the only place where a smaller symbol may
        # precede a larger one in canonical notation.
        matched = False
        for numeric, symbol in _NUMERALS:
            if text.startswith(symbol, index):
                value += numeric
                index += len(symbol)
                matched = True
                break

        if not matched:
            raise RomanNumeralError(
                f"Invalid Roman numeral sequence at position {index}: "
                f"{text[index:]!r}"
            )

    # Reject non-canonical input such as "IIII", "VX", or "IC".  The
    # canonical check is not merely syntactic; it requires the input to
    # match exactly what from_int would produce for the same value.
    if from_int(value) != text:
        raise RomanNumeralError(
            f"{text!r} is not a canonical Roman numeral"
        )

    return value
