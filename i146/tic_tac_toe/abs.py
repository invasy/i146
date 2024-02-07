from abc import ABCMeta, abstractmethod

from .board import Board, Mark


class Player(metaclass=ABCMeta):
    def __init__(self, mark: Mark = None, name: str = None) -> None:
        self.__mark = mark
        self._name = name

    @property
    def mark(self) -> Mark:
        return self.__mark

    @mark.setter
    def mark(self, mark: Mark) -> None:
        self.__mark = mark
        self._on_mark_set(mark)

    def _on_mark_set(self, mark: Mark) -> None:
        pass

    @property
    def name(self) -> str:
        return self._name or self.__class__.__name__

    @name.setter
    def name(self, name: str) -> None:
        self._name = name

    def __str__(self) -> str:
        return f'{self.name} ({self.mark})'

    @abstractmethod
    def _index(self, board: Board) -> int:
        ...

    def place_mark(self, board: Board) -> Board:
        return board.place_mark(self._index(board), self.mark)
