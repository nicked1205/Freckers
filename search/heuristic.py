from .tree import TreeNode
from .core import Direction

def calculate_heuristics(node: TreeNode, visited: list[TreeNode]):
    if node.coord not in visited:
        visited.append(node.coord)
        child: TreeNode
        for child in node.child_dict.values():
            if child:
                # print(child)
                distances = []
                child_dict = child.child_dict
                if child_dict[Direction.Left]:
                    distance = 0
                    distances.append(test_jump(child_dict[Direction.Left], distance, []))
                if child_dict[Direction.Right]:
                    distance = 0
                    distances.append(test_jump(child_dict[Direction.Right], distance, []))
                if child_dict[Direction.DownLeft]:
                    distance = 1
                    if child_dict[Direction.DownLeft].jumping:
                        distance = 2
                    distances.append(test_jump(child_dict[Direction.DownLeft], distance, []))
                if child_dict[Direction.Down]:
                    distance = 1
                    if child_dict[Direction.Down].jumping:
                        distance = 2
                    distances.append(test_jump(child_dict[Direction.Down], distance, []))
                if child_dict[Direction.DownRight]:
                    distance = 1
                    if child_dict[Direction.DownRight].jumping:
                        distance = 2
                    distances.append(test_jump(child_dict[Direction.DownRight], distance, []))
                # print('Conclusion:')
                # print(distances)
                # print('\n')
                child.set_heuristic(max(distances, default=0))
                calculate_heuristics(child, visited)

def test_jump(node: TreeNode, distance: int, visited):
    distances = [distance]
    if node.coord not in visited:
        visited.append(node.coord)
        if node.jumping:
            child_dict = node.child_dict
            if child_dict[Direction.Left]:
                distances.append(test_jump(child_dict[Direction.Left], distance, visited))
            if child_dict[Direction.Right]:
                distances.append(test_jump(child_dict[Direction.Right], distance, visited))
            if child_dict[Direction.DownLeft]:
                if child_dict[Direction.DownLeft].jumping:
                    distances.append(test_jump(child_dict[Direction.DownLeft], distance + 2, visited))
                else:
                    distances.append(test_jump(child_dict[Direction.DownLeft], distance + 1, visited))
            if child_dict[Direction.Down]:
                if child_dict[Direction.Down].jumping:
                    distances.append(test_jump(child_dict[Direction.Down], distance + 2, visited))
                else:
                    distances.append(test_jump(child_dict[Direction.Down], distance + 1, visited))
            if child_dict[Direction.DownRight]:
                if child_dict[Direction.DownRight].jumping:
                    distances.append(test_jump(child_dict[Direction.DownRight], distance + 2, visited))
                else:
                    distances.append(test_jump(child_dict[Direction.DownRight], distance + 1, visited))
        # print('----------------')
        # print(node)
        # print(distances)
    return max(distances, default=0)