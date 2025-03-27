from .core import CellState, Coord, Direction
from dataclasses import dataclass

@dataclass(order=True)
class TreeNode():
    def __init__(self, heuristic: int, state: CellState, coord: Coord, jumping: bool):
        self.heuristic = heuristic
        self.state = state
        self.coord = coord
        self.child_dict = {
                        Direction.Left: None,
                        Direction.DownLeft: None,
                        Direction.Down: None,
                        Direction.DownRight: None,
                        Direction.Right: None,
                        }
        self.jumping = jumping

    def add_child(self, dir_vector, node):
        self.child_dict[dir_vector] = node

def expand_tree(board: dict[Coord, CellState], visited, coord: Coord, root: TreeNode):
    visited.append(coord)
    for dir in [Direction.Left, Direction.DownLeft, Direction.Down, Direction.DownRight, Direction.Right]:
        try:
            new_coord = Coord(coord.r + dir.r, coord.c + dir.c)
        except:
            continue
        cell_state = board.get(new_coord)

        if cell_state == CellState.BLUE:
            try:
                new_jump_coord = Coord(coord.r + 2*dir.r, coord.c + 2*dir.c)
            except:
                continue
            cell_state_jump = board.get(new_jump_coord)
            
            if new_jump_coord not in visited and cell_state_jump == CellState.LILY_PAD:
                new_node = TreeNode(0, cell_state, new_jump_coord, True)
                root.add_child(dir, new_node)
                expand_tree(board, visited, new_jump_coord, new_node)

        elif new_coord not in visited and cell_state == CellState.LILY_PAD:
            new_node = TreeNode(0, cell_state, new_coord, False)
            root.add_child(dir, new_node)
            expand_tree(board, visited, new_coord, new_node)

def generate_tree(board: dict[Coord, CellState], visited, coord: Coord, root: TreeNode):
    visited.append(coord)
    for dir in [Direction.Left, Direction.DownLeft, Direction.Down, Direction.DownRight, Direction.Right]:
        try:
            new_coord = Coord(coord.r + dir.r, coord.c + dir.c)
        except:
            continue
        cell_state = board.get(new_coord)

        if cell_state == CellState.BLUE:
            try:
                new_jump_coord = Coord(coord.r + 2*dir.r, coord.c + 2*dir.c)
            except:
                continue
            cell_state_jump = board.get(new_jump_coord)
            
            if new_jump_coord not in visited and cell_state_jump == CellState.LILY_PAD:
                new_node = TreeNode(0, cell_state, new_jump_coord, True)
                root.add_child(dir, new_node)

        elif new_coord not in visited and cell_state == CellState.LILY_PAD:
            new_node = TreeNode(0, cell_state, new_coord, False)
            root.add_child(dir, new_node)
    return visited          