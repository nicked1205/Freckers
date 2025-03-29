from .tree import TreeNode
from .core import MoveAction
import heapq

def A_star(goal_row: int, visited: list, best_path: list, pq: list, jumping: bool):
    while pq:
        _, current = heapq.heappop(pq)
        
        visited.append(current)

        if current.coord.r == goal_row:
            return best_path

    
        children = current.child_dict

        for direction in children:
            child = children[direction]
            if child is not None and child not in visited:
                heapq.heappush(pq, (-child.heuristic, child))
                if child.jumping:
                    # print(f"Node: ({child.coord.r}, {child.coord.c}) JUMP")
                    if jumping:
                        # print("DOUBLE JUMP")
                        best_path[-1]._directions.append(direction)
                    else:
                        action = MoveAction(current.coord, [direction])
                        best_path.append(action)
                    # Recurse on the child.
                    best_path = A_star(goal_row, visited, best_path, pq, True)
                else:
                    action = MoveAction(current.coord, [direction])
                    best_path.append(action)
                    best_path = A_star(goal_row, visited, best_path, pq, False)                       
        

