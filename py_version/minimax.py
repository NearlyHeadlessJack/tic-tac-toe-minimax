from math import inf as infinity
from random import choice
import platform
import time
from os import system

PV = []
global total
global total_this
total = 0
total_this = 0

HUMAN = -1
COMP = +1
board = [
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
]


# 判断是否胜利
def evaluate(state):
    if wins(state, COMP):
        score = +1
    elif wins(state, HUMAN):
        score = -1
    else:
        score = 0

    return score


# 胜利的状态
def wins(state, player):
    win_state = [
        [state[0][0], state[0][1], state[0][2]],
        [state[1][0], state[1][1], state[1][2]],
        [state[2][0], state[2][1], state[2][2]],
        [state[0][0], state[1][0], state[2][0]],
        [state[0][1], state[1][1], state[2][1]],
        [state[0][2], state[1][2], state[2][2]],
        [state[0][0], state[1][1], state[2][2]],
        [state[2][0], state[1][1], state[0][2]],
        [state[0][1], state[0][2], state[0][3]],
        [state[1][1], state[1][2], state[1][3]],
        [state[2][1], state[2][2], state[2][3]],
        [state[0][3], state[1][3], state[2][3]],
        [state[1][3], state[2][3], state[3][3]],
        [state[3][0], state[3][1], state[3][2]],
        [state[3][1], state[3][2], state[3][3]],
        [state[1][2], state[2][1], state[3][0]],
        [state[1][3], state[2][2], state[3][1]],
        [state[0][3], state[1][2], state[2][1]],
        [state[0][1], state[1][2], state[2][3]],
        [state[1][1], state[2][2], state[3][3]],
        [state[1][0], state[2][1], state[3][2]],
        [state[1][2], state[2][2], state[3][2]],
        [state[1][1], state[2][1], state[3][1]],
    ]
    if [player, player, player] in win_state:
        return True
    else:
        return False


# 游戏结束
def game_over(state):
    return wins(state, HUMAN) or wins(state, COMP)


# 返回空格位置列表
def empty_cells(state):
    cells = []

    for x, row in enumerate(state):
        for y, cell in enumerate(row):
            if cell == 0:
                cells.append([x, y])

    return cells


# 判断所选位置是否被占用
def valid_move(x, y):
    if [x, y] in empty_cells(board):
        return True
    else:
        return False


# 判断所选位置是否被占用并更改期盘状态
def set_move(x, y, player):
    if valid_move(x, y):
        board[x][y] = player
        return True
    else:
        return False


# minimax算法主体
def minimax(state, depth, player):
    global total
    global total_this
    if player == COMP:
        best = [-1, -1, -infinity]
    else:
        best = [-1, -1, +infinity]

    if depth == 0 or game_over(state):
        score = evaluate(state)
        return [-1, -1, score]

    for cell in empty_cells(state):
        x, y = cell[0], cell[1]
        state[x][y] = player
        score = minimax(state, depth - 1, -player)
        total += 1
        total_this += 1
        state[x][y] = 0
        score[0], score[1] = x, y

        if player == COMP:
            if score[2] > best[2]:
                best = score  # max value
        else:
            if score[2] < best[2]:
                best = score  # min value

    return best


# negamax算法主体
def negamax(state, depth, player):
    global total
    global total_this

    best = [-1, -1, -infinity]

    if depth == 0 or game_over(state):
        score = estimate_value(state, player, depth)
        return [-1, -1, -score]

    for cell in empty_cells(state):
        x, y = cell[0], cell[1]
        state[x][y] = player
        score = negamax(state, depth - 1, -player)

        total += 1
        total_this += 1
        state[x][y] = 0
        score[0], score[1] = x, y
        if score[2] > best[2]:
            best = score

    best[2] *= -1
    return best


def estimate_value(state, player, depth):
    if wins(state, player):
        score = +1
    else:
        score = -1

    return score * (depth + 1)


# 多系统调用的清屏
def clean():
    os_name = platform.system().lower()
    if 'windows' in os_name:
        system('cls')
    else:
        system('clear')


# 输出棋盘目前落子状态
def render(state, c_choice, h_choice):
    chars = {
        -1: h_choice,
        +1: c_choice,
        0: ' '
    }
    str_line = '---------------'

    print('\n' + str_line)
    for row in state:
        for cell in row:
            symbol = chars[cell]
            print(f'| {symbol} |', end='')
        print('\n' + str_line)


# 电脑运行的回合逻辑
def ai_turn(c_choice, h_choice):
    depth = len(empty_cells(board))
    if depth == 0 or game_over(board):
        return

    clean()
    print(f'Computer turn [{c_choice}]')
    render(board, c_choice, h_choice)

    if depth == 16:
        x = choice([0, 1, 2, 3])
        y = choice([0, 1, 2, 3])
    else:
        move = minimax(board, depth, COMP)

        PV.append(move)
        x, y = move[0], move[1]

    set_move(x, y, COMP)
    time.sleep(1)


# 用户下棋回合逻辑
def human_turn(c_choice, h_choice):
    depth = len(empty_cells(board))
    if depth == 0 or game_over(board):
        return

    # Dictionary of valid moves
    move = -1
    moves = {
        1: [0, 0], 2: [0, 1], 3: [0, 2], 4: [0, 3],
        5: [1, 0], 6: [1, 1], 7: [1, 2], 8: [1, 3],
        9: [2, 0], 10: [2, 1], 11: [2, 2], 12: [2, 3],
        13: [3, 0], 14: [3, 1], 15: [3, 2], 16: [3, 3]
    }

    clean()
    print(f'Human turn [{h_choice}]')
    render(board, c_choice, h_choice)

    while move < 1 or move > 16:
        try:
            move = int(input('Use numpad (1..16): '))
            coord = moves[move]
            can_move = set_move(coord[0], coord[1], HUMAN)
            PV.append(moves[move])

            if not can_move:
                print('Bad move')
                move = -1
        except (EOFError, KeyboardInterrupt):
            print('Bye')
            exit()
        except (KeyError, ValueError):
            print('Bad choice')


# 主程序开始点
def main():
    clean()
    h_choice = ''  # X or O
    c_choice = ''  # X or O
    first = ''  # if human is the first

    # Human chooses X or O to play
    while h_choice != 'O' and h_choice != 'X':
        try:
            print('')
            h_choice = 'X'
        except (EOFError, KeyboardInterrupt):
            print('Bye')
            exit()
        except (KeyError, ValueError):
            print('Bad choice')

    # Setting computer's choice
    if h_choice == 'X':
        c_choice = 'O'
    else:
        c_choice = 'X'

    # Human may starts first
    clean()
    while first != 'Y' and first != 'N':
        try:
            first = input('你要先手吗?[y/n]: ').upper()
        except (EOFError, KeyboardInterrupt):
            print('Bye')
            exit()
        except (KeyError, ValueError):
            print('Bad choice')
    global total_this
    # Main loop of this game
    while len(empty_cells(board)) > 0 and not game_over(board):
        if first == 'N':
            total_this = 0
            ai_turn(c_choice, h_choice)
            first = ''
            print("本轮搜索节点数:")
            print(total_this)

        human_turn(c_choice, h_choice)
        total_this = 0
        ai_turn(c_choice, h_choice)
        print("本轮搜索节点数:")
        print(total_this)

    # Game over message
    if wins(board, HUMAN):
        clean()
        print(f'请落子 [{h_choice}]')
        render(board, c_choice, h_choice)
        print('游戏结束，您胜利了')
    elif wins(board, COMP):
        clean()
        print(f'Computer turn [{c_choice}]')
        render(board, c_choice, h_choice)
        print('游戏结束，您失败了')
    else:
        clean()
        render(board, c_choice, h_choice)
        print('游戏结束，平局')
    ep = 1
    for pv in PV:
        print('第' + str(ep) + '层')
        print('节点:' + str(pv[0] + 1) + " " + str(pv[1] + 1))
        ep += 1
    print("共搜索节点数：")
    global total

    print(total)
    exit()


# 应用程序入口
if __name__ == '__main__':
    main()
