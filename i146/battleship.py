import sys
from dataclasses import dataclass, field
from enum import StrEnum
from itertools import islice
from pathlib import Path
from typing import Any, Iterable


WIDTH = 10
HEIGHT = 10
SEA = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]

COLUMNS = {
    'а': 0,
    'б': 1,
    'в': 2,
    'г': 3,
    'д': 4,
    'е': 5,
    'ж': 6,
    'з': 7,
    'и': 8,
    'к': 9,
}
COLUMN_NAMES = list(COLUMNS.keys())


@dataclass
class Ship:
    row: int
    col: int
    size: int = 1
    vertical: bool = False
    hp: int = field(init=False)

    def __post_init__(self) -> None:
        self.hp = self.size

    def inc(self, inc: int = 1) -> 'Ship':
        self.size += inc
        self.hp += inc
        return self

    def hit(self, damage: int = 1) -> int:
        if self.hp > 0:
            self.hp -= damage
        return self.hp


class Result(StrEnum):
    MISS = 'мимо'
    HIT = 'ранил'
    KILL = 'убил'


def read_ships(f: Iterable[str], width: int = WIDTH, height: int = HEIGHT) -> dict[tuple[int, int], Ship]:
    ships: dict[tuple[int, int], Ship] = {}
    for row, line in enumerate(islice(f, height)):
        for col, c in enumerate(line.strip()[0:width]):
            if c == '1':
                if row > 0 and (row - 1, col) in ships:
                    ships[(row, col)] = ships[(row - 1, col)]
                    ships[(row, col)].vertical = True
                    ships[(row, col)].inc()
                elif col > 0 and (row, col - 1) in ships:
                    ships[(row, col)] = ships[(row, col - 1)]
                    ships[(row, col)].vertical = False
                    ships[(row, col)].inc()
                else:
                    ships[(row, col)] = Ship(row, col)
    return ships


def shot_to_coords(shot: str) -> tuple[int, int]:
    col = COLUMNS[shot[0]]
    row = int(shot[1:]) - 1
    return row, col


def coords_to_shot(row: int, col: int) -> str:
    return f'{COLUMN_NAMES[col]}{row + 1}'


def read_shots(f: Iterable[str]) -> list[tuple[int, int]]:
    return [shot_to_coords(line.strip().lower()) for line in f]


def check(ships: dict[tuple[int, int], Ship], shot: tuple[int, int]) -> Result:
    if shot in ships:
        if ships[shot].hit() <= 0:
            return Result.KILL
        else:
            return Result.HIT
    else:
        return Result.MISS


def battleship(i: str = 'input.txt', o: str = 'output.txt') -> None:
    with open(i, 'r', encoding='utf-8') as f:
        ships = read_ships(f)
        shots = read_shots(f)

    results = [check(ships, shot) for shot in shots]
    lines = [f'{r}\n' for r in results]

    with open(o, 'w', encoding='utf-8') as f:
        f.writelines(lines)


if __name__ == '__main__':
    battleship()
