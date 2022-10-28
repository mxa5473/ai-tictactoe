import unittest
from tictactoe import *


# class TestBoard(unittest.TestCase):

#     def test_place_marker():
#         return

#     def test_empty_square():
#         return

class TestTicTacToe(unittest.TestCase):

    # def test_show_lines():
    #     pass 

    # def test_draw_symbol():
    #     pass 

    def test_game_symbol(self):
        symbol = Game.game_symbol(1)
        self.assertEqual(symbol, 2)


# if __name__ == '__main__':
#     unittest.main()