from .tree import TreeNode
from .core import CellState, Coord, Direction, MoveAction
from collections import deque
import copy
from dataclasses import replace

def dfs_search(root: TreeNode, visited: list, best_path: list, path: list, jumping: bool) -> list:
    # Base case: if this node's row is the goal row, we've reached the target.
    if root.isGoal:
        return path.copy()  # return a copy of the current path

    # Mark the current node as visited.
    visited.append(root.coord)

    children = root.child_dict

    # Iterate over all children in the node's child dictionary.
    for direction in children:
        child = children[direction]

        # Proceed only if there is a child and we haven't visited it before.
        if child is not None and child.coord not in visited:
            added = False  # flag to check if we've appended an action

            # Check if there is any jump moves
            if child.isJumping(root):
                # print(f"Node: ({child.coord.r}, {child.coord.c}) JUMP")
                # Mutiple jump moves found
                if jumping:
                    # print("MULTIPLE JUMP")
                    path[-1]._directions.append(direction) # Make sure consecutive jumps are combined into 1 move action
                    # Recurse on the child.
                    solution = dfs_search(child, visited, best_path, path, True)
                    path[-1].directions.pop()
                # First jump move    
                else:
                    action = MoveAction(root.coord, [direction])
                    path.append(action)
                    added = True
                    # Recurse on the child.
                    solution = dfs_search(child, visited, best_path, path, True)

            # No jump moves
            else:
                action = MoveAction(root.coord, [direction])
                path.append(action)
                added = True
                # Recurse on the child.
                solution = dfs_search(child, visited, best_path, path, False)

            # If a valid path was found, check if it's the best (shortest) one.
            if solution:
                if best_path is None or len(solution) < len(best_path):
                    best_path = solution.copy()

            # Backtrack: remove the move after exploring this branch.
            if added:
                path.pop()
    
    # Backtrack: remove the current coordinate from visited.
    visited.pop()
    
    return best_path

def bfs_search(visited: list, added: list, queue: deque, jumping: bool) -> list:
    while queue:
        current, path, jumping = queue.popleft()
        print(f"Current: {current.coord.r}-{current.coord.c}")
        
        # Mark the current node as visited.
        visited.append(current)
        
        # Check if the goal condition is met.
        if current.isGoal:
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

def combine_paths(forward_path: tuple[list[MoveAction], bool], backward_path: tuple[list[MoveAction], bool]):
    """
    Combine the forward path and the backward path
    to form the complete solution path.
    Assumes the meeting node is the last node in forward_path and the first in backward_path.
    """

    # Resolve multiple jumps issue in the last move of each path
    if forward_path[1] and backward_path[1]:
        for direction in backward_path[0][-1]._directions:
            if direction not in forward_path[0][-1]._directions:
                forward_path[0][-1]._directions_.append(direction)
        # Remove duplicated move
        backward_path[0].pop(-1)

    # Combine two paths
    solution = [move for move in forward_path[0]] + [move for move in list(reversed(backward_path[0]))]

    return solution

def bidirectional_search(start: TreeNode, goal: TreeNode):
    """
    Performs a bidirectional search from the start node to the goal node.
    Both searches respect the jump move rules defined in your original bfs_search.
    
    Parameters:
      start: the starting node.
      goal: the target node.
      
    Returns:
      A list of MoveActions forming the path from start to goal, or None if no path is found.
    """
    # Quick check if start is already the goal.
    if start == goal:
        return []
    
    # Initialize forward search.
    forward_queue = deque([(start, [], False)])
    forward_visited = []
    forward_paths = {id(start): []}
    
    # Initialize backward search.
    backward_queue = deque([(goal, [], False)])
    backward_visited = []
    backward_paths = {id(goal): []}
    
    while forward_queue and backward_queue:
        # --- Expand forward search (similar to normal bfs) ---
        if forward_queue:
            current, path, jumping = forward_queue.popleft()
            print(f"Forward Current: {current.coord.r}-{current.coord.c}")
            forward_visited.append(current)
            
            # Check if the current node has been reached by the backward search.
            if id(current) in backward_paths:
                print("Meeting point found in forward search")
                return combine_paths(forward_paths[id(current)], backward_paths[id(current)])
            
            # Process all children of the current node.
            for direction, child in current.child_dict.items():
                if child is not None and child not in forward_visited and id(child) not in forward_paths:
                    print(f"Forward Child: {child.coord.r}-{child.coord.c}")
                    new_path = copy.deepcopy(path)
                    
                    if child.isJumping(current):
                        print("Forward JUMP")
                        if jumping and new_path:
                            print("Forward MULTIPLE JUMP")
                            new_path[-1]._directions.append(direction)
                        else:
                            action = MoveAction(current.coord, [direction])
                            new_path.append(action)
                        new_jumping = True
                    else:
                        action = MoveAction(current.coord, [direction])
                        new_path.append(action)
                        new_jumping = False
                    forward_queue.append((child, new_path, new_jumping))
                    forward_paths[id(child)] = (new_path, new_jumping)
        
        # --- Expand backward search (still bfs but with some modifications) ---
        if backward_queue:
            current, path, jumping = backward_queue.popleft()
            print(f"Backward Current: {current.coord.r}-{current.coord.c}")
            backward_visited.append(current)
            
            if id(current) in forward_paths:
                print("Meeting point found in backward search")
                return combine_paths(forward_paths[id(current)], backward_paths[id(current)])
            
            for direction, parent in current.parent_dict.items():
                if parent is not None and parent not in backward_visited and id(parent) not in backward_paths:
                    print(f"Backward parent: {parent.coord.r}-{parent.coord.c}")
                    new_path = copy.deepcopy(path)
                    
                    if current.isJumping(parent):
                        print("Backward JUMP")
                        if jumping and new_path:
                            print("Backward MULTIPLE JUMP")
                            new_path[-1]._directions.append(direction.__neg__())
                            # Update the coordinate to the parent node's since we jumped backwards
                            new_action = replace(new_path[-1], coord=parent.coord)
                            new_path[-1] = new_action
                        else:
                            # Since we are moving backwards, the move-action coordinate is the parent's
                            action = MoveAction(parent.coord, [direction.__neg__()])
                            new_path.append(action)
                        new_jumping = True
                    else:
                        # Same here
                        action = MoveAction(parent.coord, [direction.__neg__()])
                        new_path.append(action)
                        new_jumping = False
                    backward_queue.append((parent, new_path, new_jumping))
                    backward_paths[id(parent)] = (new_path, new_jumping)
                    
    # No connection found between the two searches.
    return None

def bidirectional_search_multiple_goals(start: TreeNode, goal_list: list[TreeNode]):
    best_solution = None
    # Do bidirectional search on every goal 
    for goal in goal_list:
        solution = bidirectional_search(start, goal)
        if best_solution is None or len(solution) < len(best_solution):
            best_solution = solution
            print("THIS")
    
    return best_solution