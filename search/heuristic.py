from .tree import TreeNode, BOARD_N
from .core import Direction

def calculate_heuristics(node: TreeNode, visited: list[TreeNode]):
    if node not in visited:
        visited.append(node)
    child: TreeNode
    for child in node.child_dict.values():
        if child and child not in visited:
            if not child.isGoal:
                visited.append(child)
                # print(child)
                distance = 0
                # if (node.child_dict[Direction.DownLeft] is not None and child == node.child_dict[Direction.DownLeft])\
                #       or (node.child_dict[Direction.DownRight] is not None and child == node.child_dict[Direction.DownRight])\
                #           or (node.child_dict[Direction.Down] is not None and child == node.child_dict[Direction.Down]):
                #     distance = 1
                #     if child.isJumping(node):
                #         distance = 2
                distances = [distance for i in range(5)]
                child_dict = child.child_dict
                if child_dict[Direction.Left]:
                    distances[0] += (test_jump(child_dict[Direction.Left], child, 0, []))
                if child_dict[Direction.Right]:
                    distances[1] += (test_jump(child_dict[Direction.Right], child, 0, []))
                if child_dict[Direction.DownLeft]:
                    distance = 1
                    if child_dict[Direction.DownLeft].isJumping(child):
                        distance = 2
                    distances[2] += (test_jump(child_dict[Direction.DownLeft], child, distance, []))
                if child_dict[Direction.Down]:
                    distance = 1
                    if child_dict[Direction.Down].isJumping(child):
                        distance = 2
                    distances[3] += (test_jump(child_dict[Direction.Down], child, distance, []))
                if child_dict[Direction.DownRight]:
                    distance = 1
                    if child_dict[Direction.DownRight].isJumping(child):
                        distance = 2
                    distances[4] += (test_jump(child_dict[Direction.DownRight], child, distance, []))
                # print('Conclusion:')
                # print(distances)
                # print('\n')
                child.set_heuristic(BOARD_N - child.coord.r - max(distances, default=0))
                print(child)
                calculate_heuristics(child, visited)
            else:
                child.set_heuristic(0)
                print(child)

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
            if child_dict[Direction.Down]:
                if child_dict[Direction.Down].isJumping(child):
                    distances[3] += (test_jump(child_dict[Direction.Down], child, 2, visited))
            if child_dict[Direction.DownRight]:
                if child_dict[Direction.DownRight].isJumping(child):
                    distances[4] += (test_jump(child_dict[Direction.DownRight], child, 2, visited))
        # print(child)
        # print(distances)
        return max(distances, default=0)
    return 0