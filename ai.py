"""
Tetris ai


A move is a pair of (board, (piecename, row, col, rot))

>>> f = evaluator((blocks, 3.2), (caverns, -2))
>>> f(b)
123.456
>>> g = move_thresholder(f, 150)
>>> g2 = move_chooser(f, 3)
>>> g3 = all_moves

>>> h = tree_evaluator(f, g, 4, lambda arr: sum(arr) / len(arr)) # goes four levels deep
<I at (2,3), rot 2>

"""

import board
from pieces import *

import numpy
import functools
import random


class Evaluator(object):
    def __init__(self, *function_weight_pairs):
        """Evaluator((f, 3.21), (g, -10))"""
        self.funcs, self.weights = zip(*function_weight_pairs)
    def __call__(self, board):
        return sum([f(board) * w for f, w in zip(self.funcs, self.weights)])
    def __repr__(self):
        s = ''
        s += '<Evaluator: '
        s += ' + '.join([str(w) + '*' + f.__name__  for f, w in zip(self.funcs, self.weights)])
        s += '>'
        return s

class MoveChooser(object):
    def __init__(self, evaluator, n=1):
        self.evaluator = evaluator
        self.n = n
    def __call__(self, board, piece):
        moves = all_moves(board, piece)
        moves.sort(key=lambda (board, (piecename, row, column, rot)): self.evaluator(board))
        return moves[-self.n:]
    def __repr__(self):
        s = ''
        s += '<MoveChooser: '
        s += 'takes the best '
        if self.n == 1:
            s += 'move'
        else:
            s += str(self.n)
            s += 'moves'
        s += ' sorted by '
        s += str(self.evaluator)
        s += '>'
        return s

best = functools.partial(MoveChooser, n=1)

# move selection methods
def all_moves(board, piece):
    possible = []
    #TODO don't hardcode the -1, figure it out from piece rotations
    for col in range(-1, board.columns):
        piece.pos[1] = col
        for row in range(board.rows):
            piece.pos[0] = row
            for rot in range(len(piece.rotations)):
                piece.set_rotation(rot)
                try:
                    possible.append(((board + piece).cleared(), (piece.__class__.__name__, row, col, rot)))
                except ValueError:
                    pass
                #TODO check if piece could actually get there!
    return possible

# features

#TODO cache intermediate results for other metrics to use, and use lazy evaluation so order doesn't matter
def total_blocks(board):
    return board.array.sum()
def total_surface_area(board):
    return 0
def top_surface_area(board):
    board.array
    return 0
def caverns(board):
    return 0
def linear_height_penalty(board):
    penalty = numpy.hstack([[[x] for x in range(board.height, 0, -1)] for i in range(board.width)])
    return (penalty * board.array).sum()


def test_all_moves():
    e1 = Evaluator((total_blocks, -1), (linear_height_penalty, -1))
    cur_board = board.Board()
    while True:
        piece = random_tetronimo()(0,3)
        for b, m in all_moves(cur_board, piece):
            print b
            print e1(b), m
            raw_input()

def test_simple_ai():
    e1 = Evaluator((total_blocks, -1), (linear_height_penalty, -1))
    chooser1 = best(e1)
    piece = random_tetronimo()(0,3)
    cur_board = board.Board()
    while True:
        (b, m), = chooser1(cur_board, piece)
        cur_board = b
        print cur_board
        piece = random_tetronimo()(0,3)
        raw_input()

def simulate_simple_chooser():
    e1 = Evaluator((total_blocks, -1), (linear_height_penalty, -1))
    chooser1 = best(e1)
    print simulate(chooser1)

def simulate(chooser, n=1):
    piece = random_tetronimo()(0,3)
    cur_board = board.Board()
    results = []
    for _ in range(n):
        pieces = 0
        while True:
            pieces += 1
            (b, m), = chooser(cur_board, piece)
            cur_board = b
            piece = random_tetronimo()(0,3)
            try:
                cur_board.add_floating_piece(piece)
            except ValueError:
                results.append(pieces)
                break
    return results

def run_simple_evolution():
    choosers = [
        best(Evaluator((total_blocks, 0), (linear_height_penalty, 0))),
        best(Evaluator((total_blocks, 1), (linear_height_penalty, 1))),
        best(Evaluator((total_blocks, -1), (linear_height_penalty, 1))),
        #best(Evaluator((total_blocks, 1), (linear_height_penalty, -1))),
        #best(Evaluator((total_blocks, -1), (linear_height_penalty, -1))),
        ]
    evolve(choosers)

def mutate_simple_chooser(chooser):
    func_weight_pairs = []
    for i, (func, weight) in enumerate(zip(chooser.evaluator.funcs, chooser.evaluator.weights)):
        r = random.random()
        if r > .7:
            func_weight_pairs.append((func, weight+1))
        elif r < .3:
            func_weight_pairs.append((func, weight-1))
        else:
            func_weight_pairs.append((func, weight))
    new_chooser = best(Evaluator(*func_weight_pairs))
    return new_chooser



def evolve(choosers):
    num_choosers = len(choosers)
    for roundnum in xrange(1000):
        results = []
        for chooser in choosers:
            print 'starting simulation for ', chooser
            runs = []
            for i in range(1, 2):
                runs.append(simulate(chooser)[0])
                print 'finished simulation', i, 'for', chooser
                print runs[-1]
            total = sum(runs)
            print 'total score for', chooser
            print total
            results.append((total, chooser))
        print 'finished round', roundnum
        for score, chooser in results:
            print '----'
            print chooser
            print score
        results.sort()

        print '======='
        print '======='
        choosers = [results[-1][1]]
        for _ in range(1, num_choosers):
            choosers.append(mutate_simple_chooser(results[-1][1]))
        print 'new choosers:'
        for chooser in choosers:
            print chooser
        print

if __name__ == '__main__':
    #test_all_moves()
    #test_simple_ai()
    #simulate_simple_chooser()
    run_simple_evolution()

