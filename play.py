import math
import pygame
import sys
from time import sleep, monotonic
from datetime import timedelta
import numpy as np

from four import Game
import helper

# sizes
HEIGHT = 6
WIDTH = 7
# helpers
EMPTY = 0
X = 1
O = 2
# colors
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
# size
size = width, height = 600, 400

# create a pygame
pygame.init()
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Connect 4")

# creates a board-screen
class PyBoard():
    """
    This is a class for the sizes of the board. It will be a parent class to other classes
    """
    def __init__(self, BOARD_PADDING=20):
        self.BOARD_PADDING = BOARD_PADDING
        self.board_width = ((2 / 3) * width) - (BOARD_PADDING * 2)
        self.board_height = ((2 / 3) * width) - (BOARD_PADDING * 2)
        self.cell_size = int(min(self.board_width / WIDTH, self.board_height / HEIGHT))
        self.half_cell = int(self.cell_size/2)
        self.board_origin = (BOARD_PADDING + width/6, BOARD_PADDING)

# fonts class
class Fonts():
    """
    Initialising the fonts
    """
    def __init__(self):
        self.open_sans = pygame.font.get_default_font()
        self.small = pygame.font.Font(self.open_sans, 20)
        self.medium = pygame.font.Font(self.open_sans, 28)
        self.large = pygame.font.Font(self.open_sans, 40)


class Text():
    """
    What a text needs, the text, the color and the font
    """
    def __init__(self, text, text_color, font):
        self.text = text
        self.text_color = text_color
        self.font = font

        self.full = self.font.render(self.text, True, self.text_color)


# button class
class Button(Text):
    """
    Accepts text as a parent class. creates a button
    """
    def __init__(self, text, text_color, font, left, top, button_width, button_height, button_color):
        super().__init__(text, text_color, font)
        self.left = left
        self.top = top
        self.button_width = button_width
        self.button_height = button_height
        self.button_color = button_color
        # create the button
        # make a rectangle
        self.buttonRect = pygame.Rect(self.left, self.top, self.button_width, self.button_height)
        # the text for the button
        buttonText = self.font.render(self.text, True, self.text_color)
        # getting a rect in the proper size
        buttonTextRect = buttonText.get_rect()
        # centering the button
        buttonTextRect.center = self.buttonRect.center
        # drawing the button
        pygame.draw.rect(screen, self.button_color, buttonTextRect)
        screen.blit(buttonText, buttonTextRect)


# making the actions to paint
class Actions(PyBoard):
    def __init__(self):
        super().__init__(BOARD_PADDING=20)
        self.O = set()
        self.X = set()
        self.wins = set()
        self.cells = []

    def add_win_strike(self, board):
        if helper.game_is_over(board) and helper.winner(board) is not None:
            for action in helper.take_how(board):
                x, y = self.make_x_y(action)
                self.wins.add((x, y))

    def clear(self):
        self.O.clear()
        self.X.clear()
        self.wins.clear()

    def draw_board(self):
        for i in range(HEIGHT):
            row = []
            for j in range(WIDTH):
                # Draw rectangle for cell
                rect = pygame.Rect(
                    self.board_origin[0] + j * self.cell_size,
                    self.board_origin[1] + i * self.cell_size,
                    self.cell_size, self.cell_size
                )
                pygame.draw.rect(screen, BLUE, rect)
                pygame.draw.rect(screen, BLUE, rect, 3)
                x, y = self.make_x_y((i, j))
                self.draw_action((x, y))

                row.append(rect)
            self.cells.append(row)

    def draw_action(self, action):
        if action in self.wins:
            pygame.draw.circle(screen, GREEN, action, self.half_cell)
        elif action in self.X:
            pygame.draw.circle(screen, RED, action, self.half_cell)
        elif action in self.O:
            pygame.draw.circle(screen, YELLOW, action, self.half_cell)
        else:
            pygame.draw.circle(screen, BLACK, action, self.half_cell)

    def make_x_y(self, action):
        x = (self.board_origin[0] + action[1] * self.cell_size) + self.half_cell
        y = (self.board_origin[1] + action[0] * self.cell_size) + self.half_cell
        return x, y

    def add_square(self, action, board):
        x, y = self.make_x_y(action)
        if helper.which_player(board) == X:
            self.X.add((x, y))
        else:
            self.O.add((x, y))


# checking for true and false
class Checks():
    def __init__(self):
        # Show instructions initially
        self.instructions = True
        # Check for ai button
        self.AI = False
        # paint blue
        self.first_time = True


def start_page(fonts, checks):
    """
    print the starting page
    """
    # Title
    title = Text("Play game!", WHITE, fonts.large)
    titleRect = title.full.get_rect()
    titleRect.center = ((width / 2), 50)
    screen.blit(title.full, titleRect)

    # Rules
    rules = [
        "Click at the column in which you want to place your disc",
        "The first player to put 4 discs in a row, ",
        "a column or diagonally wins!",
        "Good luck!"
    ]
    for i, rule in enumerate(rules):
        line = Text(rule, WHITE, fonts.small)
        lineRect = line.full.get_rect()
        lineRect.center = ((width / 2), 150 + 30 * i)
        screen.blit(line.full, lineRect)

    local_button = Button("Local match", BLACK, fonts.medium,
                          (width / 8),
                          (3 / 4) * height,
                          (width / 3),
                          50,
                          WHITE
                          )
    # create a button for AI match
    AI_button = Button("AI match", BLACK, fonts.medium,
                       (width / 2),
                       (3 / 4) * height,
                       (width / 3),
                       50,
                       WHITE
                       )
    click, _, _ = pygame.mouse.get_pressed()
    if click == 1:
        mouse = pygame.mouse.get_pos()
        if local_button.buttonRect.collidepoint(mouse):
            checks.instructions = False
            sleep(0.3)
        elif AI_button.buttonRect.collidepoint(mouse):
            checks.instructions = False
            checks.AI = True
            sleep(0.3)


def print_AI(fonts):
    """
    print the words on the screen
    """
    text = Text("AI thinking...", WHITE, fonts.medium)
    textRect = text.full.get_rect()
    textRect.center = ((width / 2), (height*7/8))
    screen.blit(text.full, textRect)


def end_page(checks, game, com_player, fonts, things_to_do):
    """
    presents the ending page
    """
    if checks.first_time:
        pygame.display.flip()
        sleep(10)
        checks.first_time = False
    winner = helper.winner(game.board)
    screen.fill(BLACK)
    # Title
    if winner == com_player:
        title = Text("The computer has won!", WHITE, fonts.large)
        # title = fonts.large.render("The computer has won!", True, WHITE)
    elif winner == helper.not_player(com_player):
        title = Text("You beat the computer!", WHITE, fonts.large)
        # title = fonts.large.render("You beat the computer!", True, WHITE)
    else:
        title = Text("It's a tie!", WHITE, fonts.large)
        # title = fonts.large.render("It's a tie!", True, WHITE)
    titleRect = title.full.get_rect()
    titleRect.center = ((width / 2), 50)
    screen.blit(title.full, titleRect)

    # print
    announcement = [
        "Shimol is yellow",
        "If you want another game...",
        " just click the button!"
    ]
    for i, rule in enumerate(announcement):
        line = Text(rule, WHITE, fonts.medium)
        # line = fonts.small.render(rule, True, WHITE)
        lineRect = line.full.get_rect()
        lineRect.center = ((width / 2), 150 + 30 * i)
        screen.blit(line.full, lineRect)

        # if create a button and check if it was clicked
        # Play game button
        play_button = Button("Play Game", BLACK, fonts.medium,
                             (width / 4),
                             (3 / 4) * height,
                             width / 2,
                             50,
                             WHITE
                             )
        # Check if play button clicked
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1:
            mouse = pygame.mouse.get_pos()
            if play_button.buttonRect.collidepoint(mouse):
                sleep(0.3)
                helper.clear_everything(things_to_do, game, checks)
                continue


def AI_move(game, com_player, things_to_do):
    """
    all the functions that need to take place when it's AI's move
    """
    # do what it takes
    start_time = monotonic()
    value_action = helper.minimax(game.board, 8, True, -math.inf, math.inf, com_player)
    end_time = monotonic()
    print(timedelta(seconds=end_time - start_time))
    action = value_action[1]
    print(value_action)
    game.update_board(action)
    things_to_do.add_square(action, game.board)

def create():
    # Fonts
    fonts = Fonts()

    # create a functions board
    game = Game()

    # checking for bools
    checks = Checks()

    # remember what was made
    things_to_do = Actions()

    # give the AI a player
    com_player = helper.choose_a_player()
    # the game
    while True:
        # Check if game quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        screen.fill(BLACK)

        # show instructions
        if checks.instructions:
            start_page(fonts, checks)
            pygame.display.flip()
            continue

        # paint the winning strike
        things_to_do.add_win_strike(game.board)

        # Draw board
        things_to_do.draw_board()

        if not helper.game_is_over(game.board):
            if not checks.AI:
                # get possible actions
                actions = helper.available_actions(game.board)
                # Check if play button clicked
                click, _, _ = pygame.mouse.get_pressed()
                if click == 1:
                    mouse = pygame.mouse.get_pos()
                    helper.check_for_action(mouse, things_to_do, actions, game)
            else:
                # see who's turn it is
                if helper.which_player(game.board) == com_player:
                    AI_move(game, com_player, things_to_do)
                else:
                    actions = helper.available_actions(game.board)
                    # Check if play button clicked
                    click, _, _ = pygame.mouse.get_pressed()
                    if click == 1:
                        mouse = pygame.mouse.get_pos()
                        helper.check_for_action(mouse, things_to_do, actions, game)
                        things_to_do.draw_board()
                        print_AI(fonts)
        else:
            # present the ending page
            end_page(checks, game, com_player, fonts, things_to_do)

        pygame.display.flip()


def main():
    # board = np.zeros((6, 7))
    # number = board[board != 0].size
    # print(number)
    create()

if __name__ == '__main__':
    main()