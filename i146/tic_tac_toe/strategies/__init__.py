import json
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from ..abs import Player
from ..game import Board


DIR = Path(__file__).parent


@dataclass
class Node:
    index: int = -1
    next: Optional[dict[int, 'Node']] = None


def simulate(board: Board, player: Player, node: Node) -> None:
    if board.result is not None:
        return
    board = player.place_mark(board)
    node.index = board.last
    if board.turn == 8 or board.result is not None:
        return
    node.next = {}
    for i in board.empty:
        b = board.place_mark(i, ~player.mark)
        if board.result is not None:
            continue
        node.next[i] = Node()
        simulate(b, player, node.next[i])


def dump(s: dict[int, Node], path: Path) -> None:
    with path.open('w') as f:
        json.dump(s, f, default=lambda o: o.__dict__)


def _object_hook(obj: dict) -> dict | Node:
    if 'index' in obj:
        return Node(obj['index'], obj['next'])
    return {(int(k) if k.isdigit() else k): v for k, v in obj.items()}


def load(path: str | Path) -> Optional[dict[int, Node]]:
    if isinstance(path, str):
        path = Path(path)
    if not path.is_absolute():
        path = DIR / f'{path}.json'
    if not path.exists():
        return None
    with path.open('r') as f:
        return json.load(f, object_hook=_object_hook)
