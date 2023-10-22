class NumSysDifferentBasesError(ValueError):
    def __init__(self, base1: int, base2: int) -> None:
        self.base1 = base1
        self.base2 = base2

    def __str__(self) -> str:
        return 'Arithmetic operations can be performed '\
               'on numerals with equal bases only '\
               f'(base1={self.base1}, base2={self.base2})'


class NumSysInvalidBaseError(ValueError):
    def __init__(self, base: int) -> None:
        self.base = base

    def __str__(self) -> str:
        return f'Number {self.base} cannot be a numeral system base'


class NumSysInvalidDigitError(ValueError):
    def __init__(self, digit: int | str, base: int = None) -> None:
        self.digit = digit
        self.base = base

    def __str__(self) -> str:
        value = f'Number {self.digit}' if isinstance(self.digit, int) else f"Character '{self.digit}'"
        what = f'the base-{self.base}' if self.base is not None else 'any'
        return f'{value} cannot be a digit in {what} positional numeral system'
