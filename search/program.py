# COMP30024 Artificial Intelligence, Semester 1 2025
# Project Part A: Single Player Freckers

from .core import CellState, Coord, Direction, MoveAction
from .utils import render_board, find_red
from .tree import TreeNode, expand_tree, get_goal_nodes
from .heuristic import calculate_heuristics
from .uninformed_search import dfs_search, bfs_search
from .informed_search import A_star
import heapq
from collections import deque


def search(
    board: dict[Coord, CellState]
) -> list[MoveAction] | None:
    """
    This is the entry point for your submission. You should modify this
    function to solve the search problem discussed in the Part A specification.
    See `core.py` for information on the types being used here.

    Parameters:
        `board`: a dictionary representing the initial board state, mapping
            coordinates to "player colours". The keys are `Coord` instances,
            and the values are `CellState` instances which can be one of
            `CellState.RED`, `CellState.BLUE`, or `CellState.LILY_PAD`.
    
    Returns:
        A list of "move actions" as MoveAction instances, or `None` if no
        solution is possible.
    """

    # The render_board() function is handy for debugging. It will print out a
    # board state in a human-readable format. If your terminal supports ANSI
    # codes, set the `ansi` flag to True to print a colour-coded version!
    print(render_board(board, ansi=True))

    # Do some impressive AI stuff here to find the solution...
    red_coord = find_red(board)
    red_node = TreeNode(CellState.RED, red_coord)
    visited = expand_tree(board, [], red_coord, red_node)
    goals = get_goal_nodes(visited)

    calculate_heuristics(red_node, [])

    # return dfs_search(red_node, 7, [], None, [], False)

    queue = deque()
    queue.append((red_node, [], False))

    # return bfs_search(7, [], [], queue, False)

    priority_queue = []
    heapq.heappush(priority_queue, (red_node.get_heuristic(), (red_node, [], False)))
    return A_star(7, [], [], [], priority_queue, False)

    # Here we're returning "hardcoded" actions as an example of the expected
    # output format. Of course, you should instead return the result of your
    # search algorithm. Remember: if no solution is possible for a given input,
    # return `None` instead of a list.
    return [
        MoveAction(Coord(0, 5), [Direction.Down]),
        MoveAction(Coord(1, 5), [Direction.DownLeft]),
        MoveAction(Coord(3, 3), [Direction.Left]),
        MoveAction(Coord(3, 2), [Direction.Down, Direction.Right]),
        MoveAction(Coord(5, 4), [Direction.Down]),
        MoveAction(Coord(6, 4), [Direction.Down]),
    ]
