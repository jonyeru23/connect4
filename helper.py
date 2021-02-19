"""
in this file i will put all the helper functions i need
"""
import numpy as np
from time import sleep
import random
from math import inf

EMPTY = 0
X = 1
O = 2

WIDTH = 7
HEIGHT = 6


def update_board(board, action):
    """
    updates after the relevant action
    """
    new_board = board.copy()
    new_board[action[0], action[1]] = which_player(board)
    return new_board


def which_player(board):
    """
    accepts board and return whose turn it is based on the number of 0
    """
    counter = board[board == 0].size
    if counter % 2 == 1:
        return 1
    else:
        return 2


def not_player(player):
    """
    returns the opposite player
    """
    if player == 1:
        return 2
    else:
        return 1


def available_actions(board):
    """
    returns a set of the possible actions to be made on a board
    """
    actions = set()
    for i in range(WIDTH):
        # index the cul and then return how many zeros there are, and the put +1 to the action
        cul = board[:, i]
        row = cul[cul == 0].size - 1
        if row > -1:
            actions.add((row, i))

    return actions


def winner(board):
    """"
    return x if x wins, o if o wins and None if no winner
    """
    won, how = rec_winner(1, board)
    if won:
        return 1
    won, how = rec_winner(2, board)
    if won:
        return 2
    else:
        return None


def rec_winner(first, board):
    """
    checks for x or o
    """
    # go over the culs
    for i in range(WIDTH):
        cul = board[:, i]
        # this is how many zeros there are, if there are 6 zeros i want it to continue
        when = 6 - cul[cul == 0].size
        for j in range(when):
            row = HEIGHT - 1 - j
            if board[row, i] == first:
                won, how = sub_winner(i, row, first, board)
                if won:
                    return True, how
    return False, None


def sub_winner(cul, row, first, board):
    """
    checks for diagonal and cul and row winner
    """
    # row
    how = set()
    for i in range(1, 4):
        if cul + i >= WIDTH:
            break
        elif board[row, cul + i] != first:
            break
        elif board[row, cul + i] == first:
            how.add((row, cul + i))
        # if we reached the end, return True
        if i == 3:
            how.add((row, cul))
            return True, how
    # if cul + 3 < WIDTH:
    #     the_row = board[row, cul:cul+4:1]
    #     if np.all(the_row):
    #         how.add((row, cul + i) for i in range(4))
    #         return True, how

    how.clear()
    # down diagonal
    for i in range(1, 4):
        if cul + i >= WIDTH or row + i >= HEIGHT:
            break
        elif board[row + i, cul + i] != first:
            break
        elif board[row + i, cul + i] == first:
            how.add((row + i,cul + i))
        if i == 3:
            how.add((row, cul))
            return True, how

    how.clear()
    # up diagonal
    for i in range(1, 4):
        if cul + i >= WIDTH or row - i < 0:
            break
        elif board[row - i, cul + i] != first:
            break
        elif board[row - i, cul + i] == first:
            how.add((row - i,cul + i))
        if i == 3:
            how.add((row, cul))
            return True, how

    how.clear()
    # if in cul
    for i in range(1, 4):
        if row + i >= HEIGHT:
            break
        elif board[row + i, cul] != first:
            break
        elif board[row + i, cul] == first:
            how.add((row + i, cul))
        if i == 3:
            how.add((row, cul))
            return True, how

    return False, how


def choose_a_player():
    """
    returns a random player for the computer
    """
    options = (1, 2)
    return random.choice(options)


def take_how(board):
    """
    returns the set of the winning set
    """
    won_x, how = rec_winner(1, board)
    if won_x:
        return how
    won_o, how = rec_winner(2, board)
    if won_o:
        return how


def utility(board, com_player):
    """
    returns the value of each ending state, win, lose and tie
    """
    if winner(board) == com_player:
        return 1
    elif winner(board) == not_player(com_player):
        return -1
    else:
        return 0


def get_cell(actions, j):
    """
    returns the possible action for that click
    """
    for action in actions:
        if action[1] == j:
            return action


def game_is_over(board):
    """
    return true if game is over
    """
    if winner(board) is not None or available_actions(board) == set():
        return True
    else:
        return False


def order(actions):
    """
    orders the actions from middle to edges
    """
    sorted_actions = list()
    # is it an odd number
    odd = True
    # width = 7
    index = int((WIDTH / 2))
    for i in range(WIDTH):
        visit = False
        for action in actions:
            if action[1] == index + i and odd:
                sorted_actions.append(action)
                odd = False
                visit = True
                index = index + i
                break
            elif action[1] == index - i and not odd:
                sorted_actions.append(action)
                odd = True
                visit = True
                index = index - i
                break
        if not visit:
            odd = not odd
    return sorted_actions


def minimax(board, depth, is_player, alpha, beta, com_player):
    """
    the AI taking place
    """
    if game_is_over(board):
        return utility(board, com_player), None
    elif depth == 0:
        return value_estimate(board, com_player), None

    # is it our players turn?
    if is_player:
        # set the maximum value to minus infinity
        max_value = -inf
        # set the action to None
        best_move = None
        # check for a possible win first
        action = check_for_win(board, com_player)
        if action is not None:
            return 1, action
        # loop over all children of initial board
        for action in order(available_actions(board)):
            # call the minimax for these actions
            a_value, a_move = minimax(update_board(board, action), depth - 1, False, alpha, beta, com_player)
            # if the value that was given is greater than the last maximum value, set the value and move
            if a_value > max_value:
                max_value = a_value
                best_move = action
            # alpha beta pruning
            alpha = max(a_value, alpha)
            if alpha >= beta:
                break
        return max_value, best_move
    # it is our opponents turn
    else:
        # set the minimum value to inf
        min_value = inf
        # the the optimal action to None
        best_move = None
        # check for a possible win first
        action = check_for_win(board, not_player(com_player))
        if action is not None:
            return -1, action
        # loop over all children
        for action in order(available_actions(board)):
            # call the minimax function
            a_value, a_move = minimax(update_board(board, action), depth - 1, True, alpha, beta, com_player)
            # if the value found is smaller than the current optimal value
            if a_value < min_value:
                min_value = a_value
                best_move = action
            # alpha beta pruning
            beta = min(min_value, beta)
            if beta <= alpha:
                break
        return min_value, best_move


def check_for_win(board, player):
    """
    before depth in search, first check if you can win through is board
    """
    for action in available_actions(board):
        if winner(update_board(board, action)) == player:
            return action


def check_for_action(mouse, things_to_do, actions, game):
    for i in range(HEIGHT):
        for j in range(WIDTH):
            if things_to_do.cells[i][j].collidepoint(mouse):
                # check which cul
                action = get_cell(actions, j)
                sleep(0.1)
                if action is None:
                    continue
                game.update_board(action)
                things_to_do.add_square(action, game.board)


def clear_everything(things_to_do, game, checks):
    things_to_do.clear()
    game.clear_board()
    checks.first_time = True


def value_estimate(board, com_player):
    """
    the goal is to give an estimate in case the depth is to far in
    for every position in which the com has three in a row with an open space, it gets 0.1 bonus
    for every position the opponent has three in a row with a possibility for 4 the score goes down by 0.1
    the goal of the computer is to max the score
    """
    win_value = 0
    lose_value = 0
    # go over all the cells in the board
    for row in range(HEIGHT):
        for cul in range(WIDTH):
            if board[row, cul] == com_player:
                # find if there is a three in a good position for this disc
                win_value += local_value_estimate(board, com_player, row, cul)
            elif board[row, cul] == not_player(com_player):
                # the same but for the human player
                lose_value -= local_value_estimate(board, not_player(com_player), row, cul)

    return win_value + 1.5*lose_value


def local_value_estimate(board, player, row, cul):
    options = [
        np.array([0, player, player, player]),
        np.array([player, 0, player, player]),
        np.array([player, player, 0, player]),
        np.array([player, player, player, 0])
    ]
    value = 0
    for i in options:
        # all rows options
        if cul + 3 < WIDTH:
            if np.all(board[row][cul:cul+4:1] == i):
                value += 0.1
        # all culs options
        if row + 3 < HEIGHT:
            if np.all(board[[row, row+1, row+2, row+3],[cul, cul, cul, cul]] == i):
                value += 0.1
        # up diagonal options
        if row - 3 >= 0 and cul + 3 < WIDTH:
            if np.all(board[[row, row-1, row-2, row-3], [cul, cul+1, cul+2, cul+3]] == i):
                value += 0.1
        # down diagonal options
        if row + 3 < HEIGHT and cul + 3 < WIDTH:
            if np.all(board[[row, row+1, row+2, row+ 3], [cul, cul+1, cul+2, cul+3]] == i):
                value += 0.1
    return value

