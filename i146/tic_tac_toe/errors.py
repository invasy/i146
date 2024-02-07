from typing import Any


class NotANumberError(ValueError):
    def __init__(self, value: Any) -> None:
        self.value = value

    def __str__(self) -> str:
        return f'{self.value} is not a number'


class InvalidNumberError(ValueError):
    def __init__(self, value: int) -> None:
        self.value = value

    def __str__(self) -> str:
        return f'{self.value} is not a tic-tac-toe cell number (1..9)'


class MarkedCellError(ValueError):
    def __init__(self, value: int) -> None:
        self.value = value

    def __str__(self) -> str:
        return f'Cell {self.value} is already marked'
