from .core import CellState, Coord

@dataclass(order=True)
class Treenode():
    def __init__(self, heuristic: int, state: CellState, coord: Coord):
        self.heuristic = heuristic
        self.state = state
        self.coord = coord

    def add_child(self, dir, node):
        match dir:
            case 'U':
                self.up = node
            case 'UL':
                self.upLeft = node
            case 'UR':
                self.upRight = node
            case 'L':
                self.left = node
            case 'R':
                self.right = node
            case 'D':
                self.down = node
            case 'DL':
                self.downLeft = node
            case 'DR':
                self.downRight = node