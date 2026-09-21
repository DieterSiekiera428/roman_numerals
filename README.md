# roman-numerals

Convert between integers and Roman numerals in both directions.

```python
from roman_numerals import from_int, to_int

from_int(2024)  # "MMXXIV"
to_int("MCMXCIV")  # 1994
```

The library supports the canonical, subtractive Roman numeral notation
for integers from 1 through 3999.  Zero, negative numbers, and values
above 3999 are rejected because standard Roman numerals do not have a
unambiguous representation for them without introducing extensions such
as the vinculum.

It exists because the conversion rules, especially the subtractive
pairs like IV and CM, are easy to get subtly wrong.  The parser is
strict: it accepts only the exact canonical form that `from_int`
produces.  Inputs such as `IIII` for 4 or `VX` for 5 are treated as
errors rather than being silently corrected.

Both functions raise `RomanNumeralError`, a subclass of `ValueError`,
for invalid values.  `from_int` raises `TypeError` for non-integers,
and `to_int` raises `TypeError` for non-strings.
