"""
Tetris, gameboy rules

Viewing tetris as basically a turn-based game, so long as we make our decision
withing .1s or so - so assuming expert moving-pieces abilities

Represent boards as numpy arrays

let's be rather functional about this!


>>> import piece
>>> b = Board()
>>> b2 = b + piece.I(0,0) # only works if this would be a resting place
ValueError: Not a stable position on board
>>> b2.get_positions(piece.I(0, 0)) # were there an I piece at 0 0, where could it be put
(<I at (2, 3), rot 2>, <I at (3,4), rot 4>)
>>> b2 + _[0]
<Board object at 0x012345678>

>>> f = evaluator((blocks, 3.2), (caverns, -2))
>>> f(b)
123.456
>>> g = move_thresholder(f, 150)
>>> g2 = move_chooser(f, 3)
>>> g3 = all_moves

>>> h = tree_evaluator(f, g, 4)
<I at (2,3), rot 2>
"""
import numpy

ROWS = 18
COLUMNS = 10

class Board(object):
    def __init__(self, copy_of=None, width=COLUMNS, height=ROWS):
        """If copy_of is provided, width and height are ignored"""
        if copy_of is None:
            self._array = numpy.array(
                    [[False for _ in range(COLUMNS)] for _ in range(ROWS)],
                    dtype=bool)
        else:
            self._array = numpy.array(copy_of, copy=True)
        self._array.flags.writeable = False
    array = property(lambda self: self._array)
    @property
    def array(self):
        return self._array
    width = property(lambda self: self._array.shape[1])
    columns = property(lambda self: self._array.shape[1])
    height = property(lambda self: self._array.shape[0])
    rows = property(lambda self: self._array.shape[0])
    def __add__(self, piece):
        #TODO make pieces immutable or otherwise clean up this code
        # Only pieces can be added to a board
        on_board = piece.on_board()
        if not piece.in_bounds(self.array.shape):
            raise ValueError("Piece {} is out of bounds".format(piece))
        if (on_board & self.array).any():
            raise ValueError("Piece {} collides with debris".format(piece))
        piece.pos[0] += 1
        if ((not piece.through_floor(self.array.shape)) and
                (not (piece.on_board() & self.array).any())):
            piece.pos[0] -= 1
            raise ValueError("Piece {} doesn't rest on other debris".format(piece))
        piece.pos[0] -= 1
        new = Board(copy_of=self.array)
        new._array.flags.writeable = True
        new._array += on_board
        new._array.flags.writeable = False
        return new
    def add_floating_piece(self, piece):
        new = Board(copy_of=self.array)
        new._array.flags.writeable = True
        on_board = piece.on_board()
        new._array += on_board
        new._array.flags.writeable = False
        return new
    def __eq__(self, other):
        if isinstance(Board, other):
            return self.array == other.array
        else:
            return False
    def __str__(self):
        s = ''
        for line in self.array:
            for i in range(2):
                s += '\n'
                for x in line:
                    s += 'XXXXX' if x else '  .  '
        return s
    def cleared(self):
        new = Board(copy_of=self.array)
        new._array.flags.writeable = True
        for row in range(new.rows):
            if new._array[row].all():
                new._array[1:row+1, :] = new._array[:row, :]
                new._array[0, :] = 0
        new._array.flags.writeable = False
        return new

# move selection methods

def all_boards(board, piece):
    possible = []
    for col in range(board.columns):
        for row in range(board.rows):
            for i in range(len(piece.rotations)):
                piece.rotate(i)
                try:
                    possible.append(board + piece)
                except ValueError:
                    pass
                #TODO check if piece could actually get there!
    return possible

def evaluate(board):
    metrics = ['total_blocks', 'linear_height_penalty']
    data = {metric: getattr(board, metric) for metric in metrics}
    data['board'] = board
    return data
