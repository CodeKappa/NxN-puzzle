import itertools
import util
import search
from eightpuzzle import EightPuzzleState


class EightPuzzleAgent():
    "A SearchAgent for Eight Puzzle Problem using A*"

    def __init__(self, problem, index=0):
        if index == 0:
            self.searchFunction = search.aStarSearch(problem, eightPuzzle_euclidManhattanHeuristic)
        elif index == 1:
            self.searchFunction = search.aStarSearch(problem, eightPuzzle_euclidHeuristic)
        elif index == 2:
            self.searchFunction = search.aStarSearch(problem, eightPuzzle_manhattanHeuristic)
        elif index == 3:
            self.searchFunction = search.aStarSearch(problem, eightPuzzle_displacedHeuristic)
        elif index == 4:
            self.searchFunction = search.aStarSearch(problem, eightPuzzle_displacedManhattanHeuristic)
        elif index == 5:
            self.searchFunction = search.breadthFirstSearch(problem)
        elif index == 6:
            self.searchFunction = search.uniformCostSearch(problem)
        elif index == 7:
            self.searchFunction = search.aStarSearch(problem, search.nullHeuristic())
        elif index == 8:
            self.searchFunction = search.aStarSearch(problem, eightPuzzle_thinkingAhead)


def eightPuzzle_euclidHeuristic(state, problem, info={}):
    "The Euclid distance heuristic for a EightPuzzleProblem"

    sum = 0
    arrayX = list(
        itertools.chain(*[([i] * problem.size) for i in range(problem.size)]))  # [0, 0, 0, 1, 1, 1, 2, 2, 2] for size = 3
    arrayY = range(0, problem.size) * problem.size  # [0, 1, 2, 0, 1, 2, 0, 1, 2] for size = 3

    for row in range(problem.size):
        for col in range(problem.size):
            sum = sum + ((row - arrayX[state.cells[row][col]]) ** 2 + (
                    col - arrayY[state.cells[row][col]]) ** 2) ** 0.5
    return sum


def eightPuzzle_manhattanHeuristic(state, problem, info={}):
    "The Manhattan distance heuristic for a EightPuzzleProblem"

    sum = 0
    arrayX = list(
        itertools.chain(*[([i] * problem.size) for i in range(problem.size)]))  # [0, 0, 0, 1, 1, 1, 2, 2, 2] for size = 3
    arrayY = range(0, problem.size) * problem.size  # [0, 1, 2, 0, 1, 2, 0, 1, 2] for size = 3

    for row in range(problem.size):
        for col in range(problem.size):
            sum = sum + util.manhattanDistance((row, col),
                                               (arrayX[state.cells[row][col]], arrayY[state.cells[row][col]]))
    return sum


def eightPuzzle_displacedHeuristic(state, problem, info={}):
    notInPlace = 0
    goalPuzzle = EightPuzzleState(range(0, problem.size ** 2), problem.size)
    for row in range(problem.size):
        for col in range(problem.size):
            if state.cells[row][col] != goalPuzzle.cells[row][col]:
                notInPlace = notInPlace + 1
    return notInPlace


def eightPuzzle_displacedManhattanHeuristic(state, problem, info={}):
    return eightPuzzle_displacedHeuristic(state, problem) + eightPuzzle_manhattanHeuristic(state, problem)


def eightPuzzle_euclidManhattanHeuristic(state, problem, info={}):
    return eightPuzzle_euclidHeuristic(state, problem) + eightPuzzle_manhattanHeuristic(state, problem)


def eightPuzzle_thinkingAhead(state, problem, info={}):
    successors = problem.getSuccessors(state)
    h2 = 10000000000000000000
    for nextLocation, nextDirection, cost in successors:
        haux = eightPuzzle_euclidHeuristic(nextLocation, problem)
        if haux < h2:
            h2 = haux

    return eightPuzzle_euclidHeuristic(state, problem) + h2
