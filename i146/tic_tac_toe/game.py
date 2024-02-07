from .board import Board, Mark
from .players import Player


class Game:
    def __init__(self, player1: Player, player2: Player) -> None:
        player1.mark = Mark.X
        player2.mark = Mark.O
        self.__players = player1, player2
        self.__board = Board()

    def play(self) -> Mark:
        print(self.__board)
        while self.__board.result is None:
            for p in self.__players:
                self.__board = p.place_mark(self.__board)
                print(f'{p}:\n{self.__board}')
                if self.__board.result is not None:
                    break
        return self.__board.result
