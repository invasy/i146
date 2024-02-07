from enum import IntEnum
from collections.abc import Generator
from functools import cached_property, total_ordering
from itertools import batched, compress
from typing import Optional


def decimal_to_ternary(x: int) -> list[int]:
    t = []
    while x:
        x, d = divmod(x, 3)
        if d == 2:
            d = -1
            x += 1
        t.append(d)
    return t


def ternary_to_decimal(t: list[int]) -> int:
    a, b = 0, 1
    for d in t:
        a += b * d
        b *= 3
    return a


class Mark(IntEnum):
    N = 0
    X = 1
    O = -1

    def __repr__(self) -> str:
        return str(self.value)
    
    def __str__(self) -> str:
        return ' ' if self is self.N else self.name
    
    def __neg__(self) -> 'Mark':
        return self.O if self is self.X else self.X

    def __invert__(self) -> 'Mark':
        return self.O if self is self.X else self.X


@total_ordering
class Board:
    WINS = [
        [1, 1, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 1, 1],
        [1, 0, 0, 1, 0, 0, 1, 0, 0],
        [0, 1, 0, 0, 1, 0, 0, 1, 0],
        [0, 0, 1, 0, 0, 1, 0, 0, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 1],
        [0, 0, 1, 0, 1, 0, 1, 0, 0],
    ]
    LINE = ['\u2500' * 3] * 3
    HEADER = '\u250C' + '\u252C'.join(LINE) + '\u2510'
    FOOTER = '\u2514' + '\u2534'.join(LINE) + '\u2518'
    SEP = '\u251C' + '\u253C'.join(LINE) + '\u2524'


    def __init__(self, cells: tuple[Mark, ...] | int = None, last: int = None) -> None:
        self.__hash = None
        self.__repr = None
        self.__str = None
        if cells is None:
            self.__cells = (Mark.N,) * 9
        elif isinstance(cells, int):
            self.__cells = tuple(Mark(i) for i in decimal_to_ternary(cells))
            self.__hash = cells
        else:
            self.__cells = cells
        self.__last = last

    def __hash__(self) -> int:
        if self.__hash is None:
            self.__hash = ternary_to_decimal(self.__cells)
        return self.__hash

    def __eq__(self, other: 'Board') -> bool:
        return self.__hash__() == other.__hash__()

    def __lt__(self, other: 'Board') -> bool:
        return self.__hash__() < other.__hash__()
    
    def __repr__(self) -> str:
        if self.__repr is None:
            self.__repr = f'{self.__class__.__name__}{self.__cells}'
        return self.__repr

    @staticmethod
    def __row(row):
        return '\u2502' + '\u2502'.join([f' {mark} ' for mark in row]) + '\u2502'

    def __str__(self) -> str:
        if self.__str is None:
            board = f'\n{self.SEP}\n'.join([self.__row(r) for r in batched(self.__cells, 3)])
            self.__str = '\n'.join((self.HEADER, board, self.FOOTER))
        return self.__str

    def __iter__(self) -> Generator[Mark, None, None]:
        yield from self.__cells
    
    def __getitem__(self, index: int) -> Mark:
        return self.__cells[index]
    
    @cached_property
    def turn(self) -> int:
        return len(self.__cells) - self.__cells.count(Mark.N)

    @cached_property
    def empty(self) -> tuple[int, ...]:
        return tuple(i for i, m in enumerate(self.__cells) if m is Mark.N)
    
    @property
    def last(self) -> int:
        return self.__last

    @cached_property
    def result(self) -> Optional[Mark]:
        for w in self.WINS:
            s = sum(compress(self.__cells, w))
            if abs(s) == 3:
                return Mark.X if s > 0 else Mark.O
        if not self.empty:
            return Mark.N

    def place_mark(self, index: int, mark: Mark) -> 'Board':
        pre = self.__cells[:index] if index > 0 else ()
        post = self.__cells[index+1:] if index < 8 else ()
        return self.__class__(pre + (mark,) + post, index)
