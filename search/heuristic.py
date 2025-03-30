from .tree import TreeNode, BOARD_N
from .core import Direction

def calculate_heuristics(node: TreeNode, visited: list[TreeNode]):
    if node not in visited:
        visited.append(node)
        child: TreeNode
        for child in node.child_dict.values():
            if child:
                print(child)
                distances = [0, 0, 1, 1, 1]
                child_dict = child.child_dict
                if child_dict[Direction.Left]:
                    distances[0] += (test_jump(child_dict[Direction.Left], child, distances[0], []))
                if child_dict[Direction.Right]:
                    distances[1] += (test_jump(child_dict[Direction.Right], child, distances[1], []))
                if child_dict[Direction.DownLeft]:
                    if child_dict[Direction.DownLeft].isJumping(child):
                        distances[2] = 2
                    distances[2] += (test_jump(child_dict[Direction.DownLeft], child, distances[2], []))
                if child_dict[Direction.Down]:
                    if child_dict[Direction.Down].isJumping(child):
                        distances[3] = 2
                    distances[3] += (test_jump(child_dict[Direction.Down], child, distances[3], []))
                if child_dict[Direction.DownRight]:
                    if child_dict[Direction.DownRight].isJumping(child):
                        distances[4] = 2
                    distances[4] += (test_jump(child_dict[Direction.DownRight], child, distances[4], []))
                print('Conclusion:')
                print(distances)
                print('\n')
                child.set_heuristic(BOARD_N - child.coord.r - max(distances, default=0))
                calculate_heuristics(child, visited)

def test_jump(child: TreeNode, parent: TreeNode, distance: int, visited):
    distances = [distance for i in range(5)]
    if child not in visited:
        visited.append(child)
        if child.isJumping(parent):
            child_dict = child.child_dict
            if child_dict[Direction.Left]:
                distances[0] += (test_jump(child_dict[Direction.Left], child, 0, visited))
            if child_dict[Direction.Right]:
                distances[1] += (test_jump(child_dict[Direction.Right], child, 0, visited))
            if child_dict[Direction.DownLeft]:
                if child_dict[Direction.DownLeft].isJumping(child):
                    distances[2] += (test_jump(child_dict[Direction.DownLeft], child, 2, visited))
                else:
                    distances[2] += (test_jump(child_dict[Direction.DownLeft], child, 1, visited))
            if child_dict[Direction.Down]:
                if child_dict[Direction.Down].isJumping(child):
                    distances[3] += (test_jump(child_dict[Direction.Down], child, 2, visited))
                else:
                    distances[3] += (test_jump(child_dict[Direction.Down], child, 1, visited))
            if child_dict[Direction.DownRight]:
                if child_dict[Direction.DownRight].isJumping(child):
                    distances[4] += (test_jump(child_dict[Direction.DownRight], child, 2, visited))
                else:
                    distances[4] += (test_jump(child_dict[Direction.DownRight], child, 1, visited))
        # print('----------------')
        print(child)
        print(distances)
    return max(distances, default=0)