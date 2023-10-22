from dataclasses import dataclass, field
from enum import StrEnum, unique
from itertools import zip_longest
from numbers import Integral
from typing import Callable, Optional, TypeVar, Union

from i146.numsys.errors import (
    NumSysDifferentBasesError,
    NumSysInvalidBaseError,
    NumSysInvalidDigitError,
)
from i146.util import line, subscript

T = TypeVar('T')

MIN_BASE = 2
MAX_BASE = 36

INDEX_0 = ord('0')
INDEX_A = ord('A') - 10


def add(*lists: list[int]) -> list[int] | map:
    return map(sum, zip_longest(*lists, fillvalue=0))


def adc(digits: list[int] | map, carry: int, base: int, f: Callable[[int], int] = None) -> list[int]:
    if f is None:
        f = lambda digit: digit
    result = []
    for digit in digits:
        carry, digit = divmod(carry + f(digit), base)
        result.append(digit)
    while carry:
        carry, digit = divmod(carry, base)
        result.append(digit)
    return result


def mul(digits: list[int], factor: int, base: int, shift: int = 0) -> list[int]:
    return [0] * shift + adc(digits, 0, base, lambda digit: digit * factor)


def digit_to_string(digit: int, base: int = None) -> str:
    if base is not None and digit >= base:
        raise NumSysInvalidDigitError(digit, base)
    if 0 <= digit <= 9:
        index = INDEX_0
    elif 10 <= digit < MAX_BASE:
        index = INDEX_A
    else:
        raise NumSysInvalidDigitError(digit)
    return chr(index + digit)


def digit_from_string(digit: str, base: int = None) -> int:
    upper = digit[0].upper()
    if '0' <= upper <= '9':
        index = INDEX_0
    elif 'A' <= upper <= 'Z':
        index = INDEX_A
    else:
        raise NumSysInvalidDigitError(digit)
    value = ord(upper) - index
    if base is not None and value >= base:
        raise NumSysInvalidDigitError(digit, base)
    return value


def default_abstract_methods(cls: T) -> T:
    base = cls.__bases__[0]
    for name in base.__abstractmethods__:
        if getattr(getattr(cls, name), '__isabstractmethod__', False):
            setattr(cls, name, lambda self, *args, **kwargs: NotImplemented)
            getattr(cls, name).__name__ = name
    cls.__abstractmethods__ = frozenset()
    return cls


Digits = list[int]


@unique
class ArithmeticOperation(StrEnum):
    ADD = '+'
    SUB = '−'
    MUL = '×'
    DIV = '÷'


@dataclass
class Computation:
    operation: ArithmeticOperation
    a: 'Numeral'
    b: Union['Numeral', int]
    terms: Optional[list[Digits]] = field(default=None)

    def __str__(self) -> str:
        return f'{self.a} {self.operation} {self.b}'

    def has_solution(self) -> bool:
        return self.terms is not None

    @property
    def solution(self) -> Optional[str]:
        if not self.has_solution():
            return None
        width = len(self.a.digits) + len(self.b.digits)
        base_width = len(subscript(self.a.base))
        s = [
            f' {self.a!s:>{width + base_width}}',
            f'{self.operation}{self.b!s:>{width + base_width}}',
            line(width + base_width + 1),
        ]
        first = True
        for i, term in enumerate(self.terms):
            if term:
                t = ''.join([digit_to_string(d) for d in reversed(term[i:])]) + ' ' * i
                s.append(f'{" " if first else ArithmeticOperation.ADD}{t:>{width}}')
                first = False
        s.append(line(width + base_width + 1))
        return '\n'.join(s)

    @property
    def solution_width(self) -> Optional[int]:
        if not self.has_solution():
            return None
        return len(self.a.digits) + len(self.b.digits)\
            + len(subscript(self.a.base)) + 1


@default_abstract_methods
class Numeral(Integral):
    def __init__(
        self,
        x: int | str | Digits,
        base: int,
        computation: Optional[Computation] = None,
    ) -> None:
        if base > MAX_BASE or base < MIN_BASE:
            raise NumSysInvalidBaseError(base)
        if isinstance(x, int):
            self._decimal = x
            self._digits = []
            if not x:
                self._string = '0'
            else:
                self._string = []
                while x:
                    x, digit = divmod(x, base)
                    self._digits.append(digit)
                    self._string.append(digit_to_string(digit, base))
                self._string.reverse()
                self._string = ''.join(self._string)
        elif isinstance(x, str):
            self._decimal = 0
            self._digits = []
            if not x:
                self._string = '0'
            else:
                self._string = x
                for digit in x:
                    digit = digit_from_string(digit, base)
                    self._decimal = self._decimal * base + digit
                    self._digits.append(digit)
                self._digits.reverse()
        elif isinstance(x, list):
            self._decimal = 0
            self._digits = x
            if not x:
                self._string = '0'
            else:
                self._string = []
                for digit in reversed(x):
                    self._decimal = self._decimal * base + digit
                    self._string.append(digit_to_string(digit, base))
                self._string = ''.join(self._string)
        else:
            raise TypeError(f"Invalid type '{type(x).__name__}' to construct a Numeral from")
        self._base: int = base
        self._computation = computation

    def __repr__(self) -> str:
        cls = self.__class__.__name__
        return f"{cls}('{self._string}', {self._base})"

    def __str__(self) -> str:
        return self._string + subscript(self._base)

    def __int__(self) -> int:
        return self._decimal

    def __abs__(self) -> int:
        return abs(int(self))

    def __neg__(self) -> int:
        return -int(self)

    def __pos__(self) -> int:
        return int(self)

    def __eq__(self, other: 'Numeral') -> bool:
        if isinstance(other, self.__class__):
            return (self._decimal, self._base) == (other._decimal, other._base)
        else:
            return NotImplemented

    def __add__(self, other: Union['Numeral', int, str]) -> 'Numeral':
        if isinstance(other, int):
            digits, carry = self._digits, other
        elif isinstance(other, (self.__class__, str)):
            if isinstance(other, str):
                other = self.__class__(other, self._base)
            elif self._base != other._base:
                raise NumSysDifferentBasesError(self._base, other._base)
            digits, carry = add(self._digits, other._digits), 0
        else:
            return NotImplemented
        digits = adc(digits, carry, self._base)
        computation = Computation(ArithmeticOperation.ADD, self, other)
        return Numeral(digits, self._base, computation)

    def __radd__(self, other: Union['Numeral', int, str]) -> 'Numeral':
        return self.__add__(other)

    def __mul__(self, other: Union['Numeral', int, str]) -> 'Numeral':
        if isinstance(other, int):
            product = mul(self._digits, other, self._base)
            computation = Computation(ArithmeticOperation.MUL, self, other)
        elif isinstance(other, (self.__class__, str)):
            if isinstance(other, str):
                other = self.__class__(other, self._base)
            elif self._base != other._base:
                raise NumSysDifferentBasesError(self._base, other._base)
            terms = [mul(self._digits, d, self._base, i) if d else []
                     for i, d in enumerate(other._digits)]
            product = adc(add(*terms), 0, self._base)
            computation = Computation(ArithmeticOperation.MUL, self, other, terms)
        else:
            return NotImplemented
        return self.__class__(product, self._base, computation)

    def __lshift__(self, other: int) -> 'Numeral':
        if isinstance(other, int):
            return self.__class__([0] * other + self._digits, self._base)
        else:
            return NotImplemented

    def __rshift__(self, other: int) -> 'Numeral':
        if isinstance(other, int):
            return self.__class__(self._digits[other:], self._base)
        else:
            return NotImplemented

    @property
    def digits(self) -> Digits:
        return self._digits

    @property
    def base(self) -> int:
        return self._base

    def convert(self, base: int) -> 'Numeral':
        return self.__class__(self._decimal, base) if self._base != base else self

    def has_computation(self) -> bool:
        return self._computation is not None

    @property
    def computation(self) -> Optional[Computation]:
        return self._computation

    @property
    def solution(self) -> Optional[str]:
        if not self.has_computation() and not self.computation.has_solution():
            return None
        return f'{self.computation.solution}\n{self!s:>{self.computation.solution_width}}'

    @property
    def answer(self) -> Optional[str]:
        a = f'{self._computation} = ' if self.has_computation() else ''
        return a + str(self)
