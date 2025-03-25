from .core import CellState, Coord, Direction
from dataclasses import dataclass

@dataclass(order=True)
class TreeNode():
    def __init__(self, heuristic: int, state: CellState, coord: Coord):
        self.heuristic = heuristic
        self.state = state
        self.coord = coord

    def add_child(self, dir_vector, node):
        match dir_vector:
            case (-1, 0):
                self.up = node
            case (-1, -1):
                self.upLeft = node
            case (-1, 1):
                self.upRight = node
            case (0, -1):
                self.left = node
            case (0, 1):
                self.right = node
            case (1, 0):
                self.down = node
            case (1, -1):
                self.downLeft = node
            case (1, 1):
                self.downRight = node

def expand_tree(board: dict[Coord, CellState], visited, coord: Coord, root: TreeNode):
    visited.append(coord)
    for m, n in [(1, 0), (0, 1), (1, -1), (1, 1), (-1, 1), (-1, -1), (-1, 0), (0, -1)]:
        try:
            new_coord = Coord(coord.r + m, coord.c + n)
        except:
            continue
        cell_state = board.get(new_coord)

        if cell_state == CellState.BLUE:
            try:
                new_jump_coord = Coord(coord.r + 2*m, coord.c + 2*n)
            except:
                continue
            cell_state_jump = board.get(new_jump_coord)
            
            if new_jump_coord not in visited and cell_state_jump == CellState.LILY_PAD:
                new_node = TreeNode(0, cell_state, new_jump_coord)
                root.add_child((m, n), new_node)
                expand_tree(board, visited, new_jump_coord, new_node)

        elif new_coord not in visited and cell_state == CellState.LILY_PAD:
            new_node = TreeNode(0, cell_state, new_coord)
            root.add_child((m, n), new_node)
            expand_tree(board, visited, new_coord, new_node)

def generate_tree(board: dict[Coord, CellState], visited, coord: Coord, root: TreeNode):
    visited.append(coord)
    for m, n in [(1, 0), (0, 1), (1, -1), (1, 1), (-1, 1), (-1, -1), (-1, 0), (0, -1)]:
        try:
            new_coord = Coord(coord.r + m, coord.c + n)
        except:
            continue
        cell_state = board.get(new_coord)

        if cell_state == CellState.BLUE:
            try:
                new_jump_coord = Coord(coord.r + 2*m, coord.c + 2*n)
            except:
                continue
            cell_state_jump = board.get(new_jump_coord)
            
            if new_jump_coord not in visited and cell_state_jump == CellState.LILY_PAD:
                new_node = TreeNode(0, cell_state, new_jump_coord)
                root.add_child((m, n), new_node)

        elif new_coord not in visited and cell_state == CellState.LILY_PAD:
            new_node = TreeNode(0, cell_state, new_coord)
            root.add_child((m, n), new_node)          