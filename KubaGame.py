# Author: Jonathon Stoddart
# Date Created: 6/9/2021
# Last Updated: 6/16/2021
# Description: Class KubaGame allows two players to play the board game Kuba. See rules below:
# https://sites.google.com/site/boardandpieces/list-of-games/kuba

import copy


class KubaGame:
    """
    Represents a Kuba Game, in which two players push rows/columns of marbles in a race to push 7 red marbles off the
    board.
    """

    def __init__(self, tuple1, tuple2):
        """
        tuple1 and tuple2 each contain player name and color of the marble that the player is playing.
            ex: ('PlayerA', 'B'), ('PlayerB', 'W')
        initializes 7x7 board with R, B, W (red, white, black) marbles. top left = (0, 0) ... bottom right = (6, 6)
        """
        # Player dict, holding 2 names w/ respective marble color and scored red marbles
        self._players = {
            tuple1[0]: {
                'color': tuple1[1],
                'score': 0
            },
            tuple2[0]: {
                'color': tuple2[1],
                'score': 0
            }
        }

        self._names = [tuple1[0], tuple2[0]]

        # data members
        self._current_turn = None
        self._winner = None
        self._marble_count = None
        self._first_open = 0  # see getter methods for descriptions
        self._vert_marbles = []  # "                               "

        # 7x7 board initialization
        self._board = {}
        self._board_list = []
        self._temp_board = None
        self._prev_board = None

        for row in range(7):  # blank board
            self._board[row] = [' ', ' ', ' ', ' ', ' ', ' ', ' ']

        for row in range(7):
            for column in range(7):
                if (row <= 1 and column <= 1) or (row >= 5 and column >= 5):
                    self._board[row][column] = 'W'                              # white marbles placed
                elif (row <= 1 and column >= 5) or (row >= 5 and column <= 1):
                    self._board[row][column] = 'B'                              # black marbles placed
                elif (row == 1 or row == 5) and column == 3 or \
                        (row == 2 or row == 4) and 2 <= column <= 4 or \
                        row == 3 and 1 <= column <= 5:
                    self._board[row][column] = 'R'                              # red marbles placed

        # print initialized board
        for row in range(7):
            print(self._board[row])

    def get_current_turn(self):
        """
        Returns the  player name whose turn it is to play the game (None if game has not started yet, since either
        player can make the first move)
        """
        return self._current_turn

    def make_move(self, playername, coordinates, direction):
        """
        coordinates: a tuple containing the location of the marble being moved.
        direction: L(Left), R(Right), F(Forward), B(Backward).
        Validates the move: If the game is already won, it's not the player's turn, coordinates are not valid, or a
            marble in the coordinates can not be moved in the direction specified or it's not the player's marble, etc:
            returns False.
        If an opponent marble is pushed off, it is removed from the board.
        If a Red marble is pushed off, it is removed and 'captured' by the player who made the move.
        If the move is successful, returns True.
        """
        # validate the move first. if we have a winner, return false
        if self._winner is not None:
            return False

        # check if correct player is making the move
        elif playername not in self._players or (self._current_turn is not None and playername != self._current_turn):
            return False

        # check if coordinates are valid
        for pos in coordinates:
            if pos < 0 or pos > 6:
                return False

        # check if direction is valid
        if direction != 'L' and direction != 'R' and direction != 'F' and direction != 'B':
            return False

        # check if marble at coordinates is correct color
        if self._board[coordinates[0]][coordinates[1]] != self._players[playername]['color']:
            return False

        # check if there is an open space before the marble being pushed (opposite of pushing direction)
        if direction == 'L':  # LEFT
            if coordinates[1] != 6:
                if self._board[coordinates[0]][coordinates[1]+1] != ' ':
                    return False
            if self._board[coordinates[0]][0] == self._players[playername]['color']:
                if ' ' not in self._board[coordinates[0]][0:coordinates[1]]:
                    return False

        elif direction == 'R':  # RIGHT
            if coordinates[1] != 0:
                if self._board[coordinates[0]][coordinates[1]-1] != ' ':
                    return False
            if self._board[coordinates[0]][6] == self._players[playername]['color']:  # if rightmost is player color
                if ' ' not in self._board[coordinates[0]][coordinates[1]:6]:
                    return False

        elif direction == 'F':  # FORWARDS
            if coordinates[0] != 6:
                if self._board[coordinates[0]+1][coordinates[1]] != ' ':
                    return False

            self._vert_marbles = []  # init vert marbles
            for row in range(0, coordinates[0]):
                self._vert_marbles.append(self._board[row][coordinates[1]])
            if self._board[0][coordinates[1]] == self._players[playername]['color'] and ' ' not in self._vert_marbles:
                return False

        elif direction == 'B':  # BACKWARDS
            if coordinates[0] != 0:
                if self._board[coordinates[0]-1][coordinates[1]] != ' ':
                    return False

            self._vert_marbles = []
            for row in range(coordinates[0], 6):
                self._vert_marbles.append(self._board[row][coordinates[1]])
            if self._board[6][coordinates[1]] == self._players[playername]['color'] and ' ' not in self._vert_marbles:
                return False

        # store temp in case need to revert
        self._temp_board = copy.deepcopy(self._board)

        # move is valid. make the move.
        if direction == 'L':  # LEFT
            self._first_open = 0  # init first open

            if self._board[coordinates[0]][0] == 'R' and ' ' not in self._board[coordinates[0]][0:coordinates[1]]:
                self._players[playername]['score'] += 1

            for col in range(coordinates[1]):
                if self._board[coordinates[0]][col] == ' ':
                    self._first_open = col  # set rightmost open x, left of pushed marble

            for col in range(self._first_open, coordinates[1]):  # left, we work right
                if self._board[coordinates[0]][col+1] != ' ':
                    self._board[coordinates[0]][col] = self._board[coordinates[0]][col+1]  # shift left
            self._board[coordinates[0]][coordinates[1]] = ' '  # set pushed empty

            if self._board == self._prev_board:  # Ko rule - if move is redundant, we revert and repeat the turn
                self._board = copy.deepcopy(self._temp_board)
                return False
            else:
                self._prev_board = copy.deepcopy(self._temp_board)
                self.change_turn(playername)  # change current turn
                if self._players[playername]['score'] == 7:  # check for winner
                    self._winner = playername
                # print updated board
                print('\n')
                for row in range(7):
                    print(self._board[row])
                return True

        elif direction == 'R':  # RIGHT
            self._first_open = 6

            if self._board[coordinates[0]][6] == 'R' and ' ' not in self._board[coordinates[0]][coordinates[1]:6]:
                self._players[playername]['score'] += 1

            for col in range(6, coordinates[1], -1):
                if self._board[coordinates[0]][col] == ' ':
                    self._first_open = col  # set leftmost open x, right of pushed marble

            for col in range(self._first_open, coordinates[1], -1):  # right, we work left
                if self._board[coordinates[0]][col-1] != ' ':
                    self._board[coordinates[0]][col] = self._board[coordinates[0]][col-1]  # shift right
            self._board[coordinates[0]][coordinates[1]] = ' '

            if self._board == self._prev_board:  # Ko rule
                self._board = copy.deepcopy(self._temp_board)
                return False
            else:
                self._prev_board = copy.deepcopy(self._temp_board)
                self.change_turn(playername)  # change current turn
                if self._players[playername]['score'] == 7:  # check for winner
                    self._winner = playername
                # print updated board
                print('\n')
                for row in range(7):
                    print(self._board[row])
                return True

        elif direction == 'F':  # FORWARD
            self._first_open = 0

            if self._board[0][coordinates[1]] == 'R' and ' ' not in self._vert_marbles:
                self._players[playername]['score'] += 1

            for row in range(coordinates[0]):
                if self._board[row][coordinates[1]] == ' ':
                    self._first_open = row  # set topmost open x, above pushed marble

            for row in range(self._first_open, coordinates[0]):  # up, we work down
                if self._board[row+1][coordinates[1]] != ' ':
                    self._board[row][coordinates[1]] = self._board[row+1][coordinates[1]]  # shift up
            self._board[coordinates[0]][coordinates[1]] = ' '  # set pushed empty

            if self._board == self._prev_board:
                self._board = copy.deepcopy(self._temp_board)
                return False
            else:
                self._prev_board = copy.deepcopy(self._temp_board)
                self.change_turn(playername)  # change current turn
                if self._players[playername]['score'] == 7:  # check for winner
                    self._winner = playername
                # print updated board
                print('\n')
                for row in range(7):
                    print(self._board[row])
                return True

        elif direction == 'B':  # BACKWARD
            self._first_open = 6

            if self._board[6][coordinates[1]] == 'R' and ' ' not in self._vert_marbles:
                self._players[playername]['score'] += 1

            for row in range(6, coordinates[0], -1):
                if self._board[row][coordinates[1]] == ' ':
                    self._first_open = row

            for row in range(self._first_open, coordinates[0], -1):  # down, we work up
                if self._board[row-1][coordinates[1]] != ' ':
                    self._board[row][coordinates[1]] = self._board[row-1][coordinates[1]]  # shift down
            self._board[coordinates[0]][coordinates[1]] = ' '  # set pushed empty

            if self._board == self._prev_board:
                self._board = copy.deepcopy(self._temp_board)
                return False
            else:
                self._prev_board = copy.deepcopy(self._temp_board)
                self.change_turn(playername)  # change current turn
                if self._players[playername]['score'] == 7:  # check for winner
                    self._winner = playername
                # print updated board
                print('\n')
                for row in range(7):
                    print(self._board[row])
                return True

    def change_turn(self, current):
        """
        Changes which player's turn it is. Called when a move is completed, before returning True
        """
        if current == self._names[0]:
            self._current_turn = self._names[1]
        else:
            self._current_turn = self._names[0]

    def get_winner(self):
        """
        Returns the name of the winning player or None
        """
        return self._winner

    def get_captured(self, playername):
        """
        Returns the number of Red marbles capture by (playername) - 0 if no marbles captured
        """
        return self._players[playername]['score']

    def get_marble(self, coordinates):
        """
        coordinates: tuple (row, column)
        Returns the color of (W, B, R) the marble that is present at the location - ' ' if no marble present
        """
        return self._board[coordinates[0]][coordinates[1]]

    def get_marble_count(self):
        """
        Returns the numbers of White, Black, Red marbles remaining on the board as a tuple, in that order (W, B, R)
        Initially (8, 8, 13)
        """
        self._marble_count = [0, 0, 0]

        for row in range(7):
            for column in range(7):
                if self._board[row][column] == 'W':
                    self._marble_count[0] += 1
                elif self._board[row][column] == 'B':
                    self._marble_count[1] += 1
                elif self._board[row][column] == 'R':
                    self._marble_count[2] += 1

        return tuple(self._marble_count)

    def get_first_open(self):
        """
        Returns the first open cell in the previous move (i.e. pushing right, the column of the leftmost 'X' to the
        right of the marble pushed. Or, pushing forward, the row of the bottom-most ' ' above the marble pushed.
        """
        return self._first_open

    def get_vert_marbles(self):
        """
        Returns a list of the marbles in the path of a vertical push.
        """
        return self._vert_marbles

    def get_board(self):
        """
        Returns the game board dictionary.
        """
        return self._board

    def get_prev_board(self):
        """
        Returns a copy of the temp_board dictionary from the previous turn.
        Updated after executing a move.
        """
        return self._prev_board

    def get_temp_board(self):
        """
        Returns a copy of the game board dictionary from prior to the previous turn.
        Updated before executing a move.
        """
        return self._temp_board
