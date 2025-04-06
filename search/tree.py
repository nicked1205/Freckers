from .core import CellState, Coord, Direction, BOARD_N
from dataclasses import dataclass

"""
A tree node representing a position in the game. Each node has a state, a coordinate, whether it is a goal,
a dictionary of child nodes, a dictionary of parent nodes, and a heuristic value.
"""
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
    # Append the current node to the visited list
    visited.append(root)

    # Expand the tree by checking all possible directions (as allowed by the game rules)
    for dir in [Direction.Left, Direction.DownLeft, Direction.Down, Direction.DownRight, Direction.Right]:
        try:
            new_coord = Coord(coord.r + dir.r, coord.c + dir.c)
        except:
            continue
        cell_state = board.get(new_coord)

        # Check if the cell is a valid state (LILY_PAD or BLUE)
        if cell_state == CellState.BLUE:

            # Check if the next cell in the direction is a valid jump (LILY_PAD) when the current cell is BLUE
            try:
                new_jump_coord = Coord(coord.r + 2*dir.r, coord.c + 2*dir.c)
            except:
                continue
            cell_state_jump = board.get(new_jump_coord)
            
            if cell_state_jump == CellState.LILY_PAD:

                # Create a new node for the jump
                new_node = TreeNode(cell_state, new_jump_coord)

                # Check if the heuristic needs to be updated as the frog can jump multiple times
                if new_node not in root.parent_dict.values():
                    test_jump_heuristic(board, new_jump_coord, root, [root.coord])

                # Check if the node is already visited
                if new_node not in visited:

                    # Check if the node is a goal node
                    if (new_jump_coord.r == BOARD_N - 1):
                        new_node.setGoal()

                    # If the node is not visited, add the new node as a child of the current node
                    root.add_child(dir, new_node)
                    new_node.add_parent(dir.__neg__(), root)               
                    visited = expand_tree(board, visited, new_jump_coord, new_node)
                else:

                    # If the node is already visited, add the already created node as a child of the current node, discarding the new node
                    for node in visited:
                        if node.coord_search(new_jump_coord):
                            root.add_child(dir, node)
                            new_node.add_parent(dir.__neg__(), root)
                    

        elif cell_state == CellState.LILY_PAD:

            # Similar to the above, but for non-jump moves
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

    # Check if the current node is already visited
    if cur not in visited:

        # If not, add it to the visited list
        visited.append(cur)

        # Variable to check if the jump sequence has ended
        end_jump_sequence = True

        # Check all possible directions (as allowed by the game rules) for jumps
        for dir in [Direction.Left, Direction.DownLeft, Direction.Down, Direction.DownRight, Direction.Right]:
            try:
                new_coord = Coord(cur.r + dir.r, cur.c + dir.c)
            except:
                continue
            cell_state = board.get(new_coord)

            # If the cell is BLUE, check if the next cell in the direction is a valid jump (LILY_PAD)
            if cell_state == CellState.BLUE:
                end_jump_sequence = False
                try:
                    new_jump_coord = Coord(cur.r + 2*dir.r, cur.c + 2*dir.c)
                except:
                    continue
                cell_state_jump = board.get(new_jump_coord)

                if cell_state_jump == CellState.LILY_PAD:

                    # Recursively check for jumps
                    test_jump_heuristic(board, new_jump_coord, root, visited)

        # Check if the jump sequence has ended
        if end_jump_sequence:
            print(root)
            print(cur)
            print((float(BOARD_N) - float(cur.r)) / 2)

            # Update the heuristic
            if root.get_heuristic() > (float(BOARD_N) - float(cur.r)) / 2:
                    root.set_heuristic((float(BOARD_N) - float(cur.r)) / 2)
                    if (cur.r == BOARD_N - 1):
                        root.set_heuristic(0)

# Get the goal nodes from the visited list   
def get_goal_nodes(visited: list[TreeNode]):
    goal_nodes = []
    for node in visited:
        if node.isGoal:
            goal_nodes.append(node)
    return goal_nodes