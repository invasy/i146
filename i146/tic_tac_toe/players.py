from pathlib import Path
from random import choice
from typing import Optional

from .abs import Player
from .board import Board, Mark
from .errors import InvalidNumberError, MarkedCellError, NotANumberError
from .strategies import Node, dump, load, simulate


class HumanPlayer(Player):
    def __input(self, board: Board) -> int:
        i = input(f'Your turn ({self.mark}) [1..9]: ')
        if not i.isdigit():
            raise NotANumberError(i)
        i = int(i)
        if i < 1 or i > 9:
            raise InvalidNumberError(i)
        if board[i-1] is not Mark.N:
            raise MarkedCellError(i)
        return i - 1

    def _index(self, board: Board) -> int:
        while True:
            try:
                i = self.__input(board)
                break
            except ValueError as e:
                print(f'{e}. Try again.')
        return i


class RandomPlayer(Player):
    def _index(self, board: Board) -> int:
        return choice(board.empty)


class MinimaxPlayer(Player):
    """Minimax with alpha-beta pruning"""

    def __minimax(
        self,
        board: Board,
        mark: Mark,
        alpha: int = -10,
        beta: int = 10,
    ) -> tuple[int, Optional[int]]:
        if board.turn == 0:
            return 1, 0
        if board.turn == 1:
            return -1, (4 if board[4] is Mark.N else 0)
        if (r := board.result) is not None:
            return r, None
        if mark is Mark.X:
            weight = -10
            for i in board.empty:
                w = self.__minimax(board.place_mark(i, mark), ~mark, alpha, beta)[0]
                if w > weight:
                    weight, index = w, i
                alpha = max(alpha, weight)
                if beta <= alpha:
                    break
        else:
            weight = 10
            for i in board.empty:
                w = self.__minimax(board.place_mark(i, mark), ~mark, alpha, beta)[0]
                if w < weight:
                    weight, index = w, i
                beta = min(beta, weight)
                if beta <= alpha:
                    break
        return weight, index

    def _index(self, board: Board) -> int:
        return self.__minimax(board, self.mark)[1]


class HardcodedPlayer(Player):
    def __init__(self, mark: Mark = None, name: str = None) -> None:
        super().__init__(mark, name)
        self.__node = None

    @staticmethod
    def __strategy(mark: Mark) -> Node:
        if s := load('minimax'):
            return s[mark]
        board = Board()
        player = MinimaxPlayer(mark)
        node = Node()
        if mark is Mark.X:
            simulate(board, player, node)
        else:
            node.next = {}
            for i in board.empty:
                node.next[i] = Node()
                simulate(board.place_mark(i, ~mark), player, node.next[i])
        return node

    @classmethod
    def _dump(cls) -> None:
        s = {m: cls.__strategy(m) for m in (Mark.X, Mark.O)}
        dump(s, Path('minimax.json'))

    def _on_mark_set(self, mark: Mark) -> None:
        self.__node = self.__strategy(mark)

    def _index(self, board: Board) -> int:
        if board.last:
            self.__node = self.__node.next[board.last]
        return self.__node.index


class XkcdPlayer(Player):
    def __init__(self, mark: Mark = None, name: str = None) -> None:
        super().__init__(mark, name)
        self.__node = None

    def _on_mark_set(self, mark: Mark) -> None:
        self.__node = load('xkcd')[mark]

    def _index(self, board: Board) -> int:
        if board.last is not None:
            self.__node = self.__node.next[board.last]
        return self.__node.index
