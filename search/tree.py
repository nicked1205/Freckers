from .core import CellState, Coord, Direction, BOARD_N
from dataclasses import dataclass

@dataclass(order=True)
class TreeNode():
    def __init__(self, state: CellState, coord: Coord):
        self.state = state
        self.coord = coord
        self.child_dict: dict[Direction, TreeNode]
        self.child_dict = {
                        Direction.Down: None,
                        Direction.DownLeft: None,
                        Direction.DownRight: None,
                        Direction.Left: None,
                        Direction.Right: None,
                        }
        self.parent_dict = {
                        Direction.Up: None,
                        Direction.UpLeft: None,
                        Direction.UpRight: None,
                        Direction.Left: None,
                        Direction.Right: None,
                        }
        self.isGoal = False
        self.heuristic = BOARD_N / 2

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
        self.set_heuristic(0)

    def isJumping(self, parent_node):
        if abs(self.coord.r - parent_node.coord.r) == 2 or abs(self.coord.c - parent_node.coord.c) == 2:
            return True
        return False

    def coord_search(self, coord):
        if self.coord == coord:
            return True
        return False
    
    def __str__(self):
        return f"Coord: {self.coord} Goal: {self.isGoal} Heuristic: {self.heuristic}"

    def __eq__(self, another_node):
        if not another_node:
            return False
        if not isinstance(another_node, TreeNode):
            raise TypeError('Can only compare two Nodes')   
        if self.coord != another_node.coord:
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
                new_node = TreeNode(cell_state, new_jump_coord)
                if new_node not in root.parent_dict.values():
                    test_jump_heuristic(board, new_jump_coord, root, [root.coord])
                if new_node not in visited:
                    if (new_jump_coord.r == BOARD_N - 1):
                        new_node.setGoal()
                    root.add_child(dir, new_node)
                    new_node.add_parent(dir.__neg__(), root)               
                    visited = expand_tree(board, visited, new_jump_coord, new_node)
                else:
                    for node in visited:
                        if node.coord_search(new_jump_coord):
                            root.add_child(dir, node)
                            new_node.add_parent(dir.__neg__(), root)
                    

        elif cell_state == CellState.LILY_PAD:
            new_node = TreeNode(cell_state, new_coord)
            if root.get_heuristic() > (float(BOARD_N) - float(new_coord.r)) / 2:
                    root.set_heuristic((float(BOARD_N) - float(new_coord.r)) / 2)
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

def test_jump_heuristic(board: dict[Coord, CellState], cur: Coord, root: TreeNode, visited: list[TreeNode]):
    if cur not in visited:
        visited.append(cur)
        end_jump_sequence = True
        for dir in [Direction.Left, Direction.DownLeft, Direction.Down, Direction.DownRight, Direction.Right]:
            try:
                new_coord = Coord(cur.r + dir.r, cur.c + dir.c)
            except:
                continue
            cell_state = board.get(new_coord)

            if cell_state == CellState.BLUE:
                end_jump_sequence = False
                try:
                    new_jump_coord = Coord(cur.r + 2*dir.r, cur.c + 2*dir.c)
                except:
                    continue
                cell_state_jump = board.get(new_jump_coord)

                if cell_state_jump == CellState.LILY_PAD:
                    test_jump_heuristic(board, new_jump_coord, root, visited)
        if end_jump_sequence:
            print(root)
            print(cur)
            print((float(BOARD_N) - float(cur.r)) / 2)
            if root.get_heuristic() > (float(BOARD_N) - float(cur.r)) / 2:
                    root.set_heuristic((float(BOARD_N) - float(cur.r)) / 2)
                    if (cur.r == BOARD_N - 1):
                        root.set_heuristic(0)

    
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