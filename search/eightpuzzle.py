# eightpuzzle.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).
import graphicsUtils
import search
import random
import itertools
import eightPuzzleAgents
import util
import eightPuzzleDisplay
import sys


# Module Classes

class EightPuzzleState:
    """
    The Eight Puzzle is described in the course textbook on
    page 64.

    This class defines the mechanics of the puzzle itself.  The
    task of recasting this puzzle as a search problem is left to
    the EightPuzzleSearchProblem class.
    """

    def __init__(self, numbers, size):
        """
            Constructs a new eight puzzle from an ordering of numbers.

            numbers: a list of integers from 0 to 8 representing an
            instance of the eight puzzle.  0 represents the blank
            space.  Thus, the list
            size: the size of the puzzle

            [1, 0, 2, 3, 4, 5, 6, 7, 8]

          represents the eight puzzle:
            -------------
            | 1 |   | 2 |
            -------------
            | 3 | 4 | 5 |
            -------------
            | 6 | 7 | 8 |
            ------------

        The configuration of the puzzle is stored in a 2-dimensional
        list (a list of lists) 'cells'.
        """
        self.size = size
        self.cells = []
        numbers = numbers[:]  # Make a copy so as not to cause side-effects.
        numbers.reverse()
        for row in range(self.size):
            self.cells.append([])
            for col in range(self.size):
                self.cells[row].append(numbers.pop())
                if self.cells[row][col] == 0:
                    self.blankLocation = row, col

    def isGoal(self):
        """
          Checks to see if the puzzle is in its goal state.

            -------------
            |   | 1 | 2 |
            -------------
            | 3 | 4 | 5 |
            -------------
            | 6 | 7 | 8 |
            -------------

        >>> EightPuzzleState([0, 1, 2, 3, 4, 5, 6, 7, 8]).isGoal()
        True

        >>> EightPuzzleState([1, 0, 2, 3, 4, 5, 6, 7, 8]).isGoal()
        False
        """
        current = 0
        for row in range(self.size):
            for col in range(self.size):
                if current != self.cells[row][col]:
                    return False
                current += 1
        return True

    def legalMoves(self):
        """
          Returns a list of legal moves from the current state.

        Moves consist of moving the blank space up, down, left or right.
        These are encoded as 'up', 'down', 'left' and 'right' respectively.

        >>> EightPuzzleState([0, 1, 2, 3, 4, 5, 6, 7, 8]).legalMoves()
        ['down', 'right']
        """
        moves = []
        row, col = self.blankLocation
        if (row != 0):
            moves.append('up')
        if (row != self.size - 1):
            moves.append('down')
        if (col != 0):
            moves.append('left')
        if (col != self.size - 1):
            moves.append('right')
        return moves

    def result(self, move):
        """
          Returns a new eightPuzzle with the current state and blankLocation
        updated based on the provided move.

        The move should be a string drawn from a list returned by legalMoves.
        Illegal moves will raise an exception, which may be an array bounds
        exception.

        NOTE: This function *does not* change the current object.  Instead,
        it returns a new object.
        """
        row, col = self.blankLocation
        if (move == 'up'):
            newrow = row - 1
            newcol = col
        elif (move == 'down'):
            newrow = row + 1
            newcol = col
        elif (move == 'left'):
            newrow = row
            newcol = col - 1
        elif (move == 'right'):
            newrow = row
            newcol = col + 1
        else:
            raise "Illegal Move"

        # Create a copy of the current eightPuzzle
        newPuzzle = EightPuzzleState([0] * (self.size ** 2), self.size)
        newPuzzle.cells = [values[:] for values in self.cells]
        # And update it to reflect the move
        newPuzzle.cells[row][col] = self.cells[newrow][newcol]
        newPuzzle.cells[newrow][newcol] = self.cells[row][col]
        newPuzzle.blankLocation = newrow, newcol

        return newPuzzle

    # Utilities for comparison and display
    def __eq__(self, other):
        """
            Overloads '==' such that two eightPuzzles with the same configuration
          are equal.

          >>> EightPuzzleState([0, 1, 2, 3, 4, 5, 6, 7, 8]) == \
              EightPuzzleState([1, 0, 2, 3, 4, 5, 6, 7, 8]).result('left')
          True
        """
        for row in range(self.size):
            if self.cells[row] != other.cells[row]:
                return False
        return True

    def __hash__(self):
        return hash(str(self.cells))

    def __getAsciiString(self):
        """
          Returns a display string for the maze
        """
        lines = []
        horizontalLine = ('-' * (13))
        lines.append(horizontalLine)
        for row in self.cells:
            rowLine = '|'
            for col in row:
                if col == 0:
                    col = ' '
                rowLine = rowLine + ' ' + col.__str__() + ' |'
            lines.append(rowLine)
            lines.append(horizontalLine)
        return '\n'.join(lines)

    def __str__(self):
        return self.__getAsciiString()


class EightPuzzleSearchProblem(search.SearchProblem):
    """
        Implementation of a SearchProblem for the  Eight Puzzle domain

        Each state is represented by an instance of an eightPuzzle.
    """

    def __init__(self, puzzle, size):
        "Creates a new EightPuzzleSearchProblem which stores search information."
        self.puzzle = puzzle
        self.size = size

    def getStartState(self):
        return self.puzzle

    def isGoalState(self, state):
        return state.isGoal()

    def getSuccessors(self, state):
        """
            Returns list of (successor, action, stepCost) pairs where
            each succesor is either left, right, up, or down
            from the original state and the cost is 1.0 for each
        """
        succ = []
        for a in state.legalMoves():
            succ.append((state.result(a), a, 1))
        return succ

    def getCostOfActions(self, actions):
        """
            actions: A list of actions to take

            This method returns the total cost of a particular sequence of actions.  The sequence must
            be composed of legal moves
        """
        return len(actions)

EIGHT_PUZZLE_DATA = [[1, 0, 2, 3, 4, 5, 6, 7, 8],
                     [1, 7, 8, 2, 3, 4, 5, 6, 0],
                     [4, 3, 2, 7, 0, 5, 1, 6, 8],
                     [5, 1, 3, 4, 0, 2, 6, 7, 8],
                     [1, 2, 5, 7, 6, 8, 0, 4, 3],
                     [0, 3, 1, 6, 8, 2, 7, 5, 4]]


def loadEightPuzzle(puzzleNumber):
    """
        puzzleNumber: The number of the eight puzzle to load.

        Returns an eight puzzle object generated from one of the
        provided puzzles in EIGHT_PUZZLE_DATA.

        puzzleNumber can range from 0 to 5.

      >>> print loadEightPuzzle(0)
      -------------
      | 1 |   | 2 |
      -------------
      | 3 | 4 | 5 |
      -------------
      | 6 | 7 | 8 |
      -------------
    """
    return EightPuzzleState(EIGHT_PUZZLE_DATA[puzzleNumber], 3)


def createRandomEightPuzzle(moves=100, size=3):
    """
        moves: number of random moves to apply
        size: the size of the puzzle

        Creates a random puzzle by applying a series
        of 'moves' random moves to a solved puzzle.
    """
    puzzle = EightPuzzleState(range(0, size ** 2), size)
    for i in range(moves):
        # Execute a random legal move
        puzzle = puzzle.result(random.sample(puzzle.legalMoves(), 1)[0])
    return puzzle


def default(str):
    return str + ' [Default: %default]'


def readCommand(argv):
    """
    Processes the command used to run eightpuzzle from the command line.
    """
    from optparse import OptionParser
    usageStr = """
       USAGE:      python eightpuzzle.py <options>
       EXAMPLES:   (1) python eightpuzzle.py
                       - creates an 8 puzzle game with a randomly generated state
                   (2) python eightpuzzle.py --size 4 --moves 100
                   OR  python eightpuzzle.py -s 4 --moves 100
                       - starts a 15 puzzle where and the position will be shuffled with 100 legal moves
       """
    parser = OptionParser(usageStr)

    parser.add_option('-s', '--size', type='int', dest='size',
                      help=default('The size of the puzzle (SIZE ** 2)'),
                      default=3)
    parser.add_option('-t', '--textGraphics', action='store_true', dest='textGraphics',
                      help=default('Display output as text only'),
                      default=False)
    parser.add_option('-a', '--agent', type='int', dest='agent',
                      help=default('Select the agent'),
                      default=0)
    parser.add_option('--width', type='int', dest='width',
                      help=default('Width of the graphics display'),
                      default=600)
    parser.add_option('--height', type='int', dest='height',
                      help=default('Height of the graphics display'),
                      default=600)
    parser.add_option('--frames', action='store_true', dest='frames',
                      help=default('Saves each puzzle state in ./frames'),
                      default=False)
    parser.add_option('--load', type='int', dest='load',
                      help=default('Loads one of 6 (0-5) 8 puzzles instead of generating a random one'),
                      default=-1)
    parser.add_option('--moves', type='int', dest='moves',
                      help=default('Shuffles the correct puzzle solution with MOVES legal moves to create random puzzle'),
                      default=30)
    options, otherjunk = parser.parse_args(argv)
    if len(otherjunk) != 0:
        raise Exception('Command line input not understood: ' + str(otherjunk))
    args = dict()

    if options.size < 2: parser.error('Size must be > 1')
    if options.width > 7680: parser.error('Try a width <= 7680')
    if options.width < 300: parser.error('Try a width >= 300')
    if options.height > 4320: parser.error('Try a height <= 4320')
    if options.height < 300: parser.error('Try a height >= 300')
    if options.moves < 0: parser.error('The number of moves should be positive')
    if options.size != 3 and options.load >= 0: parser.error('size must be 3 to use the stored puzzles')
    if options.load > 5: parser.error('There are 6 puzzle stored, numbered from 0 to 5')
    if options.agent < 0: parser.error('Agent is a value between 0 and 8')
    if options.agent > 8: parser.error('Agent is a value between 0 and 8')

    args['size'] = options.size
    args['width'] = options.width
    args['height'] = options.height
    args['frames'] = options.frames
    args['textGraphics'] = options.textGraphics
    args['load'] = options.load
    args['moves'] = options.moves
    args['agent'] = options.agent

    return args


def runGame(size, width, height, frames, textGraphics, load, moves, agent):
    # create or load a puzzle
    if load >= 0: puzzle = loadEightPuzzle(load)
    else: puzzle = createRandomEightPuzzle(moves, size)

    # initialize display
    if not textGraphics:
        display = eightPuzzleDisplay.Graphics(width, height, size)
        display.updatePuzzleGraphics(puzzle, "Starting State: click to continue")

    # saves the current state in ./frame as a ps file
    if frames: eightPuzzleDisplay.saveFrame()

    # find the solution to the puzzle
    problem = EightPuzzleSearchProblem(puzzle, size)
    path = eightPuzzleAgents.EightPuzzleAgent(problem, agent).searchFunction

    print('The algorithm found a path of %d moves: %s' % (len(path), str(path)))

    i = 1
    if textGraphics: raw_input("Press return for the next state...")  # wait for key stroke
    else: graphicsUtils.wait_for_click() # wait for click
    for a in path:
        puzzle = puzzle.result(a)
        s = ('After %d move%s: %s' % (i, ("", "s")[i > 1], a))

        if textGraphics:
            print s
            print(puzzle)
            raw_input("Press return for the next state...")  # wait for key stroke
        else:
            display.updatePuzzleGraphics(puzzle, s)
            graphicsUtils.wait_for_click() # wait for click

        if frames: eightPuzzleDisplay.saveFrame()
        i += 1


if __name__ == '__main__':
    """
    The main function called when eightpuzzle.py is run
    from the command line:
    > python eightpuzzle.py

    See the usage string for more details.
    > python eightpuzzle.py --help
    """
    args = readCommand(sys.argv[1:])  # Get game components based on input
    runGame(**args)