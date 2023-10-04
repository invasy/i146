#!/usr/bin/env python
"""Перевод чисел в разные системы счисления"""
from dataclasses import dataclass, field


def sub(x: int) -> str:
    return ''.join([chr(ord(d) - ord('0') + 0x2080) for d in str(x)])


def dec(x: str, base: int) -> int:
    assert base <= 36, 'The base must be less than or equal to 36'
    dec = 0
    for digit in x.upper():
        if '0' <= digit <= '9':
            digit = ord(digit) - ord('0')
        elif 'A' <= digit <= 'Z':
            digit = ord(digit) - ord('A') + 10
        assert 0 <= digit < base, f'A digit ({digit}) must be less than the base ({base})'
        dec = dec * base + digit
    return dec


def num(dec: int, base: int) -> str:
    x = []
    while dec:
        dec, digit = divmod(dec, base)
        if digit >= 10:
            digit = chr(digit + ord('A') - 10)
        else:
            digit = chr(digit + ord('0'))
        x.append(digit)
    return ''.join(reversed(x))


@dataclass
class NumSysProblem:
    x: str
    base1: int
    base2: int
    _solution: str = field(default=None, init=False)

    def __str__(self) -> str:
        return f'{self.x}{sub(self.base1)} = X{sub(self.base2)}'

    @property
    def solution(self) -> str:
        if self._solution is None:
            self._solution = num(dec(self.x, self.base1), self.base2)
        return self._solution


problems_8v = [NumSysProblem(*p) for p in [
    ('1234567', 8, 16),
    ('ABCD', 16, 2),
    ('1001111011011', 2, 4),
    ('4561', 9, 3),
    ('12121', 3, 9),
]]


if __name__ == '__main__':
    for i, p in enumerate(problems_8v):
        print(f'{i+1}. {p}: {p.solution}')
