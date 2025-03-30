from .tree import TreeNode
from .core import CellState, Coord, Direction, MoveAction
from collections import deque
import copy

def dfs_search(root: TreeNode, goal_row: int, visited: list, best_path: list, path: list, jumping: bool) -> list:
    # Base case: if this node's row is the goal row, we've reached the target.
    if root.coord.r == goal_row:
        #print(f"GOAL-{len(path)}")
        return path.copy()  # return a copy of the current path

    # print(f'Node: {root.coord}')
    # Mark the current node as visited.
    visited.append(root.coord)

    children = root.child_dict

    # Iterate over all children in the node's child dictionary.
    for direction in children:
        child = children[direction]

        # Proceed only if there is a child and we haven't visited it before.
        if child is not None and child.coord not in visited:
            # print(f'Root: {root.coord}')
            # print(f'{direction} child')
            added = False  # flag to check if we've appended an action

            # Check if there is any jump moves
            if child.isJumping(root):
                # print(f"Node: ({child.coord.r}, {child.coord.c}) JUMP")
                # Mutiple jump moves found
                if jumping:
                    # print("MULTIPLE JUMP")
                    path[-1]._directions.append(direction) # Make sure consecutive jumps are combined into 1 move action
                    # Recurse on the child.
                    solution = dfs_search(child, goal_row, visited, best_path, path, True)
                    path[-1].directions.pop()
                # First jump move    
                else:
                    action = MoveAction(root.coord, [direction])
                    path.append(action)
                    added = True
                    # Recurse on the child.
                    solution = dfs_search(child, goal_row, visited, best_path, path, True)

            # No jump moves
            else:
                action = MoveAction(root.coord, [direction])
                path.append(action)
                added = True
                # Recurse on the child.
                solution = dfs_search(child, goal_row, visited, best_path, path, False)

            # If a valid path was found, check if it's the best (shortest) one.
            if solution:
                if best_path or len(solution) < len(best_path):
                    best_path = solution.copy()

            # Backtrack: remove the move after exploring this branch.
            if added:
                path.pop()
    
    # Backtrack: remove the current coordinate from visited.
    visited.pop()
    
    return best_path

def bfs_search(goal_row: int, visited: list, added: list, queue: deque, jumping: bool) -> list:
    while queue:
        current, path, jumping = queue.popleft()
        print(f"Current: {current.coord.r}-{current.coord.c}")
        
        # Mark the current node as visited.
        visited.append(current)
        
        # Check if the goal condition is met.
        if current.coord.r == goal_row:
            print("Goal reached")
            return path
        
        # Process all children of the current node.
        for direction, child in current.child_dict.items():
            if child is not None and child not in visited and child not in added:
                print(f"Child: {child.coord.r}-{child.coord.c}") 
                new_path = copy.deepcopy(path)  # Copy the current path to extend it.
                
                if child.isJumping(current):
                    print("JUMP")
                    # Multiple jump moves
                    if jumping and new_path:
                        print("MUTIPLE JUMP")
                        new_path[-1]._directions.append(direction) # Make sure consecutive jump moves are combined
                    else:
                        # First jump move.
                        action = MoveAction(current.coord, [direction])
                        new_path.append(action)
                    queue.append((child, new_path, True))

                else:
                    # No jump moves
                    action = MoveAction(current.coord, [direction])
                    new_path.append(action)
                    queue.append((child, new_path, False))
                
                added.append(child)
    
    # Return None if no path is found.
    return None

def bidirectional_search(root: TreeNode, visited):
    return
