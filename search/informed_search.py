from .core import MoveAction
import heapq

def A_star(goal_row: int, visited: list, best_path: list, pq: list, jumping: bool):
    while pq:
        _, current = heapq.heappop(pq)
        print(f'Current: {current.coord.r}-{current.coord.c}')

        visited.append(current)
        if current.coord.r == goal_row:
            print('Goal')
            return best_path

        children = current.child_dict

        for direction in children:
            child = children[direction]
            if child is not None and child not in visited:
                print(f'Child: {child.coord.r}-{child.coord.c}, Heuristic: {child.get_heuristic()}')
                heapq.heappush(pq, (child.get_heuristic(), child))
                
        if current.jumping:
            print(f"Node: ({current.coord.r}, {current.coord.c}) JUMP")
            if jumping:
                print("DOUBLE JUMP")
                best_path[-1]._directions.append(direction)
            else:
                action = MoveAction(current.coord, [direction])
                best_path.append(action)
            # Recurse on the child and capture the result.
            result = A_star(goal_row, visited, best_path, pq, True)
            if result:
                return result
        else:
            action = MoveAction(current.coord, [direction])
            best_path.append(action)
            result = A_star(goal_row, visited, best_path, pq, False)
            if result:
                return result
    # If no path is found, return None or an appropriate value
    return None
