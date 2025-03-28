from .tree import TreeNode
from .core import CellState, Coord, Direction, MoveAction

def dfs_search(root: TreeNode, goal_row: int, visited: list, best_path: list, path: list, jumping: bool) -> list:
    # Base case: if this node's row is the goal row, we've reached the target.
    if root.coord.r == goal_row:
        #print(f"GOAL-{len(path)}")
        return path.copy()  # return a copy of the current path

    #print(f'Node: {root.coord}')
    # Mark the current node as visited.
    visited.append(root.coord)

    # Iterate over all children in the node's child dictionary.
    for direction in root.child_dict:
        child = root.child_dict[direction]

        # Proceed only if there is a child and we haven't visited it before.
        if child is not None and child.coord not in visited:
            # print(f'Root: {root.coord}')
            # print(f'{direction} child')
            added = False  # flag to check if we've appended an action
            if child.jumping:
                # print(f"Node: ({child.coord.r}, {child.coord.c}) JUMP")
                if jumping:
                    # print("DOUBLE JUMP")
                    path[-1]._directions.append(direction)
                    # Recurse on the child.
                    solution = dfs_search(child, goal_row, visited, best_path, path, True)
                    path[-1].directions.pop()
                else:
                    action = MoveAction(root.coord, [direction])
                    path.append(action)
                    added = True
                    # Recurse on the child.
                    solution = dfs_search(child, goal_row, visited, best_path, path, True)
            else:
                action = MoveAction(root.coord, [direction])
                path.append(action)
                added = True
                # Recurse on the child.
                solution = dfs_search(child, goal_row, visited, best_path, path, False)

            # If a valid path was found, check if it's the best (shortest) one.
            if solution is not None:
                if best_path is None or len(solution) < len(best_path):
                    best_path = solution.copy()

            # Backtrack: remove the move after exploring this branch.
            if added:
                path.pop()
    
    # Backtrack: remove the current coordinate from visited.
    visited.pop()
    
    return best_path

def bidirectional_search(root: TreeNode, visited):
    return
