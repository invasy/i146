from .game import Game
from .players import HardcodedPlayer, HumanPlayer, MinimaxPlayer, RandomPlayer


g = Game(HardcodedPlayer(), RandomPlayer())
r = g.play()
print(r)
