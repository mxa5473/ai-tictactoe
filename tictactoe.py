# Your solution must contain a class called TicTacToe with the following method:
# place_marker(symbol, row, column) : Positions player's marker in a cell of the grid.
# Params: symbol can be x or o - use whatever datatype you think is most appropriate to represent this.
# row and column can be an integer from 0 to 2.

# Display Board
# Board
# Play game
# Check game
# Check win
    # check rows
    # check columns
    # check diagonals
# Check tie
# Flip player

""" from enum import IntEnum

class TicTacToe:
    class STATES(IntEnum):
        CROSS_TURN = 0
        NAUGHT_TURN = 1
        DRAW = 2
        CROSS_WON = 3
        NAUGHT_WON = 4

def place_marker(symbol, row, column):
    ...
# ...
# Other methods as necessary.
# ... """

# Modules
import copy
import random
import sys
import pygame
import numpy as np
from constants import * 

# *** PYGAME SETUP *** 

pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('TIC TAC TOE CHALLENGE')
screen.fill(background_color)

# *** BOARD (Console) *** 

class Board:

    def __init__(self): 
        self.bsquare = np.zeros((rows, cols))
        self.empty_bsqrs = self.bsquare # Start of game
        self.place_marked = 0

    def final_condition(self, show=False):
        """
            @return 0 if there is no win yet
            @return 1 if player 1 wins
            @return 2 if player 2 wins
        """
        # vertical wins
        for col in range(cols):
            if self.bsquare[0][col] == self.bsquare[1][col] == self.bsquare[2][col] != 0:
                if show:
                    color = circle_color if self.bsquare[0][col] == 2 else cross_color
                    iPos = (col * square + square // 2, 20 )
                    fPos = (col * square + square // 2, height - 20 )
                    pygame.draw.line(screen, color, iPos, fPos, line_width)
                return self.bsquare[0][col]

        # horizontal wins
        for row in range(rows):
            if self.bsquare[row][0] == self.bsquare[row][1] == self.bsquare[row][2] != 0:
                    if show:
                        color = circle_color if self.bsquare[row][0] == 2 else cross_color
                        iPos = (20, row * square + square // 2)
                        fPos = (width - 20, row * square + square // 2)
                        pygame.draw.line(screen, color, iPos, fPos, line_width)
                    return self.bsquare[row][0]

        # Descending diagnoal 
        if self.bsquare[0][0] == self.bsquare[1][1] == self.bsquare[2][2] != 0:
                    if show:
                        color = circle_color if self.bsquare[1][1] == 2 else cross_color
                        iPos = (20, 20)
                        fPos = (width - 20, height - 20)
                        pygame.draw.line(screen, color, iPos, fPos, cross_width)
                    return self.bsquare[1][1]

        # Ascending diagnoal 
        if self.bsquare[2][0] == self.bsquare[1][1] == self.bsquare[0][2] != 0:
                    if show:
                        color = circle_color if self.bsquare[1][1] == 2 else cross_color
                        iPos = (20, height - 20)
                        fPos = (width - 20, 20)
                        pygame.draw.line(screen, color, iPos, fPos, cross_width)
                    return self.bsquare[1][1]

        # No win yet
        return 0

    def place_marker(self, symbol, row, col):
        self.bsquare[row][col] = symbol
        self.place_marked += 1

    def empty_square(self, row, col):
        return self.bsquare[row][col] == 0

    def get_empty_bs(self):
        empty_bsqrs = [] # empty board squares 
        for row in range(rows):
            for col in range(cols):
                if self.empty_square(row, col):
                    empty_bsqrs.append((row,col))
        return empty_bsqrs

    def bFull(self):
        return self.place_marked == 9

    def bEmpty(self):
        return self.place_marked == 0

class AI:

    def __init__(self, level=1, symbol=2):
        self.level = level
        self.symbol = symbol

    def rand(self, board):
        empty_bsqrs = board.get_empty_bs()
        i = random.randrange(0, len(empty_bsqrs))

        return empty_bsqrs[i] # (row, col)

    def minimax(self, board, maximizing):
        
        # terminal case
        case = board.final_condition()

        # player 1 win
        if case == 1:
            return 1, None # eval, move
        
        # player 2 wins
        if case == 2:
            return -1, None

        # draw
        elif board.bFull():
            return 0, None

        if maximizing:
            max_eval = -100
            best_move = None
            empty_bsqrs = board.get_empty_bs()

            for (row, col) in empty_bsqrs:
                temp_board = copy.deepcopy(board)
                temp_board.place_marker(1, row, col)
                eval = self.minimax(temp_board, False)[0]
                if eval > max_eval:
                    max_eval = eval
                    best_move = (row, col)

            return max_eval, best_move
        
        elif not maximizing:
            min_eval = 100
            best_move = None
            empty_bsqrs = board.get_empty_bs()

            for (row, col) in empty_bsqrs:
                temp_board = copy.deepcopy(board)
                temp_board.place_marker(self.symbol, row, col)
                eval = self.minimax(temp_board, True)[0]
                if eval < min_eval:
                    min_eval = eval
                    best_move = (row, col)

            return min_eval, best_move

    def evaluate(self, main_board):
        if self.level == 0:
            # random choice 
            eval = 'random'
            move = self.rand(main_board)
        else:
            # minimax algo choice
            eval, move = self.minimax(main_board, False)

        print(f'AI has chosen to mark the square in pos {move} with an eval of: {eval}')

        return move # row, col

class Game:

    def __init__(self):
        self.board = Board()
        # Symbol-1-cross, Symbol-2-circle
        self.ai = AI()
        self.symbol = 1 
        self.gamemode = 'ai' # pvp or ai
        self.running = True
        self.show_lines()

    def make_move(self, row, col):
        self.board.place_marker(self.symbol, row, col)
        self.draw_symbol(row, col)
        self.game_symbol()
    
    def show_lines(self):

        # bg
        screen.fill(background_color)

        #vertical 
        pygame.draw.line(screen, line_color, (square, 0), (square, height), line_width)
        pygame.draw.line(screen, line_color, (width - square, 0), (width - square, height), line_width)

        #horizontal 
        pygame.draw.line(screen, line_color, (0, square), (width, square), line_width)
        pygame.draw.line(screen, line_color, (0, height - square), (width, height - square), line_width)

    def draw_symbol(self, row, col):
        if self.symbol == 1:
            # draw cross
            # descending line
            start_d = (col * square + offset, row * square + offset)
            end_d = (col * square + square - offset, row * square + square - offset)
            pygame.draw.line(screen, cross_color, start_d, end_d, cross_width)
            # ascending line
            start_a = (col * square + offset, row * square + square - offset)
            end_a = (col * square + square - offset, row * square + offset)
            pygame.draw.line(screen, cross_color, start_a, end_a, cross_width)

        elif self.symbol == 2:
            # draw circle
            center = (col * square + square // 2, row * square + square // 2)
            pygame.draw.circle(screen, circle_color, center, radius, circle_width)

    def game_symbol(self):
        # Remainder 
        # if self.symbol is 1, 1 % 2 + 1 = 2
        # if self.symbol is 2, 2 % 2 + 1 = 1
        self.symbol = self.symbol % 2 + 1 

    def change_gamemode(self):
        self.gamemode = 'ai' if self.gamemode == 'pvp' else 'pvp'

    def isover(self):
        return self.board.final_condition(show=True) != 0 or self.board.bFull()

    def reset(self):
        self.__init__()
            
# *** MAIN ***

def main():

    game = Game()
    board = game.board  
    ai = game.ai 

    # Main Loop - Graphic Board
    while True:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                # g-gamemode
                if event.key == pygame.K_g:
                    game.change_gamemode()

                # r-restart
                if event.key == pygame.K_r:
                    game.reset()
                    board = game.board  
                    ai = game.ai 

                # 0-random ai
                if event.key == pygame.K_0:
                    ai.level = 0

                # 1-random ai
                if event.key == pygame.K_1:
                    ai.level = 1

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                row = pos[1] // square
                col = pos[0] // square

                if board.empty_square(row, col) and game.running:
                    game.make_move(row, col)

                    if game.isover():
                        game.running = False

        if game.gamemode == 'ai' and game.symbol == ai.symbol and game.running:
            # update the screen
            pygame.display.update()

            # ai methods
            row, col = ai.evaluate(board)
            game.make_move(row, col)

            if game.isover():
                game.running = False

        pygame.display.update()

main() 







