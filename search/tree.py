from .core import CellState, Coord, Direction, BOARD_N
from dataclasses import dataclass

@dataclass(order=True)
class TreeNode():
    def __init__(self, state: CellState, coord: Coord, jumping: bool):
        self.state = state
        self.coord = coord
        self.jumping = jumping
        self.child_dict = {
                        Direction.Left: None,
                        Direction.DownLeft: None,
                        Direction.Down: None,
                        Direction.DownRight: None,
                        Direction.Right: None,
                        }
        self.parent_dict = {
                        Direction.Left: None,
                        Direction.UpLeft: None,
                        Direction.Up: None,
                        Direction.UpRight: None,
                        Direction.Right: None,
                        }
        self.isGoal = False
        self.heuristic = 0

    def add_child(self, dir_vector, node):
        self.child_dict[dir_vector] = node

    def add_parent(self, dir_vector, node):
        self.parent_dict[dir_vector] = node

    def set_heuristic(self, heuristic):
        self.heuristic = heuristic

    def get_heuristic(self):
        return self.heuristic
    
    def setGoal(self):
        self.isGoal = True

    def coord_search(self, coord):
        if self.coord == coord:
            return True
        return False
    
    def __str__(self):
        return f"Coord: {self.coord} Jumping: {self.jumping}"

    def __eq__(self, another_node):
        if not isinstance(another_node, TreeNode):
            raise TypeError('Can only compare two Nodes')   
        if self.coord != another_node.coord or self.jumping != another_node.jumping:
            return False
        return True

def expand_tree(board: dict[Coord, CellState], visited: list[TreeNode], coord: Coord, root: TreeNode):
    visited.append(root)
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
            
            if cell_state_jump == CellState.LILY_PAD:
                new_node = TreeNode(cell_state, new_jump_coord, True)
                if new_node not in visited:
                    if (new_jump_coord.r == BOARD_N - 1):
                        new_node.setGoal()
                    root.add_child(dir, new_node)                 
                    visited = expand_tree(board, visited, new_jump_coord, new_node)
                else:
                    for node in visited:
                        if node.coord_search(new_jump_coord):
                            root.add_child(dir, node)
                    

        elif cell_state == CellState.LILY_PAD:
            new_node = TreeNode(cell_state, new_coord, False)
            if new_node not in visited:   
                if (new_coord.r == BOARD_N - 1):
                    new_node.setGoal()
                root.add_child(dir, new_node)
                new_node.add_parent(dir.__neg__(), root)                 
                visited = expand_tree(board, visited, new_coord, new_node)
            else:
                for node in visited:
                    if node.coord_search(new_coord):
                        root.add_child(dir, node)
                        node.add_parent(dir.__neg__(), root)
        
    return visited
    
def get_goal_nodes(visited: list[TreeNode]):
    goal_nodes = []
    for node in visited:
        if node.isGoal:
            goal_nodes.append(node)
    return goal_nodes

# def generate_tree(board: dict[Coord, CellState], visited: list[TreeNode], coord: Coord, root: TreeNode):
#     visited.append(coord)
#     for dir in [Direction.Left, Direction.DownLeft, Direction.Down, Direction.DownRight, Direction.Right]:
#         try:
#             new_coord = Coord(coord.r + dir.r, coord.c + dir.c)
#         except:
#             continue
#         cell_state = board.get(new_coord)

#         if cell_state == CellState.BLUE:
#             try:
#                 new_jump_coord = Coord(coord.r + 2*dir.r, coord.c + 2*dir.c)
#             except:
#                 continue
#             cell_state_jump = board.get(new_jump_coord)
            
#             if new_jump_coord not in visited and cell_state_jump == CellState.LILY_PAD:
#                 new_node = TreeNode(cell_state, new_jump_coord, True)
#                 root.add_child(dir, new_node)

#         elif new_coord not in visited and cell_state == CellState.LILY_PAD:
#             new_node = TreeNode(cell_state, new_coord, False)
#             root.add_child(dir, new_node)
#     return visited        