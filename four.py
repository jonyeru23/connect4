import numpy as np
from helper import which_player

EMPTY = 0
X = 1
O = 2

WIDTH = 7
HEIGHT = 6


class Game():
    """
    a class with the relevant board methods
    """
    def __init__(self):
        """
        initialize the board
        """
        self.board = np.zeros((HEIGHT, WIDTH), dtype=np.int16)

    def clear_board(self):
        """
        clear the board and make it all zeros
        """
        self.board = np.zeros((HEIGHT, WIDTH), dtype=np.int16)

    def update_board(self, action):
        """
        updates after the relevant action
        """
        self.board[action[0], action[1]] = which_player(self.board)


