from .core import MoveAction
from .tree import TreeNode
import heapq
import copy

def A_star(visited: list, added: list, best_path: list, pq: list, jumping: bool):
    while pq:
        _, (current, best_path, jumping) = heapq.heappop(pq)
        print(f"Current: {current.coord.r}-{current.coord.c}")
        visited.append(current)
        
        # Goal check.
        if current.isGoal:
            print("Goal")
            return best_path
        
        # Process each child of the current node.
        for direction, child in current.child_dict.items():
            if child is None:
                continue
            if child in visited or child in added:
                continue
            
            print(child)
            # Create a new path based on whether this move is a jump.
            if child.isJumping(current):
                print(f"Jump move from {current.coord.r}-{current.coord.c} to {child.coord.r}-{child.coord.c} via {direction}")
                if jumping:
                    # Already in a jump sequence—make a deep copy of the path and combine with the last move.
                    new_path = copy.deepcopy(best_path)
                    if new_path:
                        new_path[-1]._directions.append(direction)
                    else:
                        # In the unlikely event best_path is empty.
                        new_path.append(MoveAction(current.coord, [direction]))
                    new_jumping = True
                else:
                    # Start a new jump move.
                    new_path = copy.deepcopy(best_path)
                    new_path.append(MoveAction(current.coord, [direction]))
                    new_jumping = True
            else:
                # Normal move: start a new move action.
                new_path = copy.deepcopy(best_path)
                new_path.append(MoveAction(current.coord, [direction]))
                new_jumping = False

            new_state = (child, new_path, new_jumping)
            heapq.heappush(pq, ((child.get_heuristic(), child.isGoal), new_state))
            added.append(child)
    
    # If the search exhausts without finding a goal, return None.
    return None

