import unittest
from KubaGame import *


class MyTestCase(unittest.TestCase):
    def test_winner(self):
        """
        Entire game's worth of code, tests that the winner is properly assigned when score reaches 7
        """
        game = KubaGame(("Bonnie", 'W'), ("Clyde", 'B'))
        game.make_move("Bonnie", (1, 0), 'R')
        game.make_move("Clyde", (1, 6), 'L')
        game.make_move("Bonnie", (1, 1), 'R')
        game.make_move("Clyde", (0, 6), 'B')
        game.make_move("Bonnie", (1, 2), 'R')
        game.make_move("Clyde", (0, 5), 'B')
        game.make_move("Bonnie", (1, 3), 'R')
        game.make_move("Clyde", (2, 6), 'F')
        game.make_move("Bonnie", (1, 4), 'R')
        game.make_move("Clyde", (0, 6), 'B')
        game.make_move("Bonnie", (1, 5), 'R')
        game.make_move("Clyde", (6, 0), 'R')
        game.make_move("Bonnie", (2, 6), 'L')
        game.make_move("Clyde", (6, 1), 'R')
        game.make_move("Bonnie", (2, 5), 'L')
        game.make_move("Clyde", (6, 2), 'R')
        game.make_move("Bonnie", (2, 4), 'L')
        game.make_move("Clyde", (6, 3), 'R')
        game.make_move("Bonnie", (2, 3), 'L')
        game.make_move("Clyde", (6, 4), 'R')
        game.make_move("Bonnie", (2, 2), 'L')
        game.make_move("Clyde", (6, 6), 'F')
        game.make_move("Bonnie", (2, 1), 'L')
        game.make_move("Clyde", (5, 6), 'F')
        game.make_move("Bonnie", (3, 6), 'L')
        game.make_move("Clyde", (4, 6), 'F')
        game.make_move("Bonnie", (5, 5), 'L')
        game.make_move("Clyde", (3, 6), 'F')
        game.make_move("Bonnie", (3, 5), 'L')
        game.make_move("Clyde", (2, 6), 'F')
        game.make_move("Bonnie", (3, 4), 'L')
        game.make_move("Clyde", (1, 6), 'F')
        game.make_move("Bonnie", (3, 3), 'L')
        self.assertEqual("Bonnie", game.get_winner())

    def test_capture_left(self):
        """
        Tests capture of a red marble via leftward move
        """
        game = KubaGame(("Bonnie", 'W'), ("Clyde", 'B'))
        game.make_move("Bonnie", (6, 6), 'F')
        game.make_move("Clyde", (0, 6), 'B')
        game.make_move("Bonnie", (5, 6), 'F')
        game.make_move("Clyde", (6, 0), 'R')
        game.make_move("Bonnie", (3, 6), 'L')
        game.make_move("Clyde", (6, 1), 'R')
        game.make_move("Bonnie", (3, 5), 'L')
        self.assertEqual(1, game.get_captured("Bonnie"))

    def test_capture_right(self):
        """
        Tests capture of a red marble via rightward move
        """
        game = KubaGame(("Bonnie", 'W'), ("Clyde", 'B'))
        game.make_move("Clyde", (6, 0), 'F')
        game.make_move("Bonnie", (0, 0), 'R')
        game.make_move("Clyde", (5, 0), 'F')
        game.make_move("Bonnie", (0, 1), "R")
        game.make_move("Clyde", (3, 0), "R")
        game.make_move("Bonnie", (0, 2), "R")
        game.make_move("Clyde", (3, 1), "R")
        self.assertEqual(1, game.get_captured("Clyde"))

    def test_capture_forward(self):
        """
        Tests capture of a red marble via forwards move
        """
        game = KubaGame(("Bonnie", 'W'), ("Clyde", 'B'))
        game.make_move("Clyde", (6, 0), 'R')
        game.make_move("Bonnie", (0, 0), 'B')
        game.make_move("Clyde", (6, 1), 'R')
        game.make_move("Bonnie", (1, 0), 'B')
        game.make_move("Clyde", (6, 3), 'F')
        game.make_move("Bonnie", (2, 0), 'B')
        game.make_move("Clyde", (5, 3), 'F')
        self.assertEqual(1, game.get_captured("Clyde"))

    def test_capture_backward(self):
        """
        Tests capture of a red marble via backwards move
        """
        game = KubaGame(("Bonnie", 'W'), ("Clyde", 'B'))
        game.make_move("Bonnie", (0, 0), 'R')
        game.make_move("Clyde", (6, 0), 'F')
        game.make_move("Bonnie", (0, 1), 'R')
        game.make_move("Clyde", (5, 0), 'F')
        game.make_move("Bonnie", (0, 3), 'B')
        game.make_move("Clyde", (4, 0), 'F')
        game.make_move("Bonnie", (1, 3), 'B')
        self.assertEqual(1, game.get_captured("Bonnie"))

    def test_ko_rule(self):
        """
        Tests the enforcement of the Ko rule, in which the board cannot return to it's previous state due to a
        redundant move (the move returns False as it is invalid)
        """
        game = KubaGame(("Bonnie", 'W'), ("Clyde", 'B'))
        game.make_move("Bonnie", (1, 0), 'R')
        game.make_move("Clyde", (1, 6), 'L')
        game.make_move("Bonnie", (1, 1), 'R')
        self.assertEqual(False, game.make_move("Clyde", (1, 5), 'L'))  # move invalid


if __name__ == '__main__':
    unittest.main()