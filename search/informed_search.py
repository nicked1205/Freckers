from .core import MoveAction
from .tree import TreeNode
import heapq
import copy

def A_star_old(parent: TreeNode, goal_row: int, visited: list, added: list, best_path: list, pq: list, jumping: bool):
    while pq:
        # Pop the first node in the queue
        _, current = heapq.heappop(pq)
        print(f'Current: {current.coord.r}-{current.coord.c}')
        
        # Add node to visited
        visited.append(current)

        # Base case: if this node's row is the goal row, we've reached the target.
        if current.coord.r == goal_row:
            print('Goal')
            return best_path

        children = current.child_dict
        no_children = True

        for direction in children:
            child = children[direction]
            # Check if child is None, already visited or already in the queue
            if child is not None and child not in visited and child not in added:
                print(child)
                heapq.heappush(pq, (child.get_heuristic(), child)) # push child to queue
                added.append(child) # mark that child is ADDED TO QUEUE, not visited
                no_children = False
        
        print(f"No Children: {no_children}")
        if no_children:
            return None

        if parent:               
            # Check if there is any jump moves
            if current.isJumping(parent):
                print("JUMP")
                # Mutiple jump moves found
                if jumping:
                    print("MULTIPLE JUMP")
                    best_path[-1]._directions.append(next((key for key, value in parent.child_dict.items() if value and value == current), None)) # Make sure consecutive jumps are combined into 1 move action
                # First jump move
                else:
                    action = MoveAction(parent.coord, [next((key for key, value in parent.child_dict.items() if value == current), None)])
                    best_path.append(action)
                # Recurse on the child and capture the result.
                result = A_star(current, goal_row, visited, added, best_path, pq, True)
                if result:
                    return result
                
            # No jump moves    
            else:
                action = MoveAction(parent.coord, [next((key for key, value in parent.child_dict.items() if value == current), None)])
                best_path.append(action)
                result = A_star(current, goal_row, visited, added, best_path, pq, False)
                if result:
                    return result
        else:
            result = A_star(current, goal_row, visited, added, best_path, pq, False)
            if result:
                return result

            
    # If no path is found, return None or an appropriate value
    return None

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

