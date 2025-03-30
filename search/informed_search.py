from .core import MoveAction
from .tree import TreeNode
import heapq

def A_star(parent: TreeNode, goal_row: int, visited: list, added: list, best_path: list, pq: list, jumping: bool):
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

        for direction in children:
            child = children[direction]
            # Check if child is None, already visited or already in the queue
            if child is not None and child not in visited and child not in added:
                print(f'Child: {child.coord.r}-{child.coord.c}, Heuristic: {child.get_heuristic()}')
                heapq.heappush(pq, (child.get_heuristic(), child)) # push child to queue
                added.append(child) # mark that child is ADDED TO QUEUE, not visited
        
        # Check if there is any jump moves
        if current.isJumping(parent):
            print("JUMP")
            # Mutiple jump moves found
            if jumping:
                print("MULTIPLE JUMP")
                best_path[-1]._directions.append(direction) # Make sure consecutive jumps are combined into 1 move action
            # First jump move
            else:
                action = MoveAction(current.coord, [direction])
                best_path.append(action)
            # Recurse on the child and capture the result.
            result = A_star(current, goal_row, visited, added, best_path, pq, True)
            if result:
                return result
            
        # No jump moves    
        else:
            action = MoveAction(current.coord, [direction])
            best_path.append(action)
            result = A_star(current, goal_row, visited, added, best_path, pq, False)
            if result:
                return result
            
    # If no path is found, return None or an appropriate value
    return None
