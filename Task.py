from enum import Enum, unique


@unique
class Move(Enum):
    THE_SAME = 0,
    LEFT = 1,
    TOP = 2,
    RIGHT = 3,
    DOWN = 4,
    LEFT_TOP = 5,
    RIGHT_TOP = 6
    LEFT_DOWN = 7,
    RIGHT_DOWN = 8


class P:
    Left = 0.2
    Right = 0.4
    Top = 0.3
    Down = 0.2
    Vertical_Same = 0.5
    Horizontal_Same = 0.4


def classify_move(x_diff, y_diff):
    if x_diff == 0 and y_diff == 0:
        return Move.THE_SAME
    if x_diff == -1 and y_diff == 0:
        return Move.LEFT
    if x_diff == 0 and y_diff == 1:
        return Move.TOP
    if x_diff == 1 and y_diff == 0:
        return Move.RIGHT
    if x_diff == 0 and y_diff == -1:
        return Move.DOWN
    if x_diff == -1 and y_diff == 1:
        return Move.LEFT_TOP
    if x_diff == 1 and y_diff == 1:
        return Move.RIGHT_TOP
    if x_diff == -1 and y_diff == -1:
        return Move.LEFT_DOWN
    if x_diff == 1 and y_diff == -1:
        return Move.RIGHT_DOWN


def calculate_move_probability(move):
    result = {
        Move.THE_SAME:    P.Vertical_Same * P.Horizontal_Same,
        Move.LEFT:        P.Left * P.Vertical_Same,
        Move.TOP:         P.Top * P.Horizontal_Same,
        Move.RIGHT:       P.Right * P.Vertical_Same,
        Move.DOWN:        P.Down * P.Horizontal_Same,
        Move.LEFT_TOP:    P.Left * P.Top,
        Move.RIGHT_TOP:   P.Right * P.Top,
        Move.LEFT_DOWN:   P.Left * P.Down,
        Move.RIGHT_DOWN:  P.Right * P.Down
    }
    return result[move]


def calculate_common_direction_probability(path):
    p = 0
    for move in path:
        p += calculate_move_probability(move)
    return p


def calculate_single_path_probability(path):
    p = 1
    for move in path:
        p *= calculate_move_probability(move)
    return p


# This recursion can calculate probability without copying moves to paths to speed up process
# But this solution is more clear, easily testable and debuggable.
def calculate_paths(paths_success, paths_fail, moves, x0, y0, step):
    if step == 5:
        if x0 == 0 and y0 == 0:
            paths_success.append(moves.copy())
        else:
            paths_fail.append(moves.copy())
    elif step < 5:
        for x in range(-1, 2):
            for y in range(-1, 2):
                move = classify_move(x, y)
                moves.append(move)
                calculate_paths(paths_success, paths_fail, moves, x0 + x, y0 + y, step + 1)
                del moves[-1]


def calculate_multiple_paths_probability(paths):
    p = 0
    for path in paths:
        p += calculate_single_path_probability(path)
    return p


def test1():
    p = calculate_common_direction_probability([Move.THE_SAME,
                                                Move.LEFT,
                                                Move.LEFT_DOWN,
                                                Move.DOWN,
                                                Move.RIGHT_DOWN,
                                                Move.RIGHT,
                                                Move.RIGHT_TOP,
                                                Move.TOP,
                                                Move.LEFT_TOP])
    res = round(p, 0) == 1
    print(res)


def test2():
    p = calculate_single_path_probability([Move.LEFT, Move.RIGHT])
    res = round(p, 2) == 0.02
    print(res)


def test3():
    paths_success = []
    paths_fail = []
    moves = []
    calculate_paths(paths_success, paths_fail, moves, 0, 0, 0)
    p_success = calculate_multiple_paths_probability(paths_success)
    p_fail = calculate_multiple_paths_probability(paths_fail)
    res = round(p_success + p_fail, 0) == 1
    print(res)


def test():
    test1()
    test2()
    test3()


def main():
    paths_success = []
    paths_fail = []
    moves = []
    calculate_paths(paths_success, paths_fail, moves, 0, 0, 0)
    p_success = calculate_multiple_paths_probability(paths_success)
    p_fail = calculate_multiple_paths_probability(paths_fail)
    print(p_success)
    print(p_fail)


#test()
main()