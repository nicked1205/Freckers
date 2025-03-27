from .tree import TreeNode
from .core import CellState, Coord, Direction, MoveAction

def dfs_search(root: TreeNode, goal_row: int, visited: list, best_path: list, path: list) -> list:
    # Base case: if this node's row is the goal row, we've reached the target.
    if root.coord.r == goal_row:
        return path.copy()  # return a copy of the current path

    # Mark the current node as visited.
    visited.append(root.coord)

    print(f'Node {root.coord}')
    print(f'Children: {root.child_dict}')
    
    # Iterate over all children in the node's child dictionary.
    for direction in root.child_dict:
        print(f'Look {direction}')
        child = root.child_dict[direction]
        # Proceed only if there is a child and we haven't visited it before.
        if child is not None and child.coord not in visited:
            print(f'{direction} child')
            action = MoveAction(root.coord, direction)
            path.append(action)
            # Recurse on the child.
            solution = dfs_search(child, goal_row, visited, best_path, path)
            # If a valid path was found, check if it's the best (shortest) one.
            if solution is not None:
                if best_path is None or len(solution) < len(best_path):
                    best_path = solution.copy()
            # Backtrack: remove the move after exploring this branch.
            path.pop()
    
    # Backtrack: remove the current coordinate from visited.
    visited.pop()
    
    return best_path
