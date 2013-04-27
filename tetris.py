"""
Nintendo Tetris Rules - because that's the 20% I'm intersted in

Using Left-handed rotation rules (used Game Boy Tetris)


"""
import random
import numpy
from copy import deepcopy
from pprint import pprint

# Tetronimos
rotations = {
    'i1' : [[0,0,0,0],
           [0,0,0,0],
           [1,1,1,1],
           [0,0,0,0]],
    'i2' : [[0,1,0,0],
           [0,1,0,0],
           [0,1,0,0],
           [0,1,0,0]],
    'j' : [[0,0,0],
           [1,1,1],
           [0,0,1]],
    'l' : [[0,0,0],
           [1,1,1],
           [1,0,0]],
    's1' : [[0,0,0],
           [0,1,1],
           [1,1,0]],
    's2' : [[1,0,0],
           [1,1,0],
           [0,1,0]],
    't' : [[0,0,0],
           [1,1,1],
           [0,1,0]],
    'z1' : [[0,0,0],
           [1,1,0],
           [0,1,1]],
    'z2' : [[0,1,0],
           [1,1,0],
           [1,0,0]]}
for k, v in rotations.iteritems():
    rotations[k] = numpy.array(v)

def generate_3x3_rotations(rotation):
    rotations = []
    for i in range(4):
        if i: rotation = numpy.rot90(rotation)
        rotations.append(rotation)
    return rotations

#TODO rename "rotation"
class Piece(object):
    def __init__(self, row, column):
        self._rotation_index = 0
        self.pos = [row, column]
    def __getattr__(self, att):
        if att == 'rotation':
            return self.rotations[self._rotation_index]
        else:
            raise AttributeError()
    def __repr__(self):
        return str(self.rotations)
    def rotate(self, offset=1):
        self._rotation_index = (self._rotation_index + offset) % len(self.rotations)
    def on_board(self, dims):
        padded_board = self.on_padded_board(dims)
        empty_board_with_piece = padded_board[
                self.rotation.shape[0]:-self.rotation.shape[0],
                self.rotation.shape[1]:-self.rotation.shape[1]]
        return empty_board_with_piece
    def on_padded_board(self, dims):
        padded_board = numpy.zeros((dims[0]+2*self.rotation.shape[0],
                                   dims[1]+2*self.rotation.shape[1]))
        padded_board[self.rotation.shape[0]+self.pos[0]:self.pos[0]+2*self.rotation.shape[0],
                     self.rotation.shape[1]+self.pos[1]:self.pos[1]+2*self.rotation.shape[1]] = self.rotation
        return padded_board
    def in_bounds(self, dims):
        board = self.on_board(dims)
        return self.rotation.sum() == board.sum()
    def through_floor(self, dims):
        padded_board = self.on_padded_board(dims)
        is_through_floor = numpy.sum(padded_board[-self.rotation.shape[0]:, :])
        return is_through_floor

class I(Piece):
    rotations = [rotations['i1'].copy(), rotations['i2'].copy()]
class S(Piece):
    rotations = [rotations['s1'].copy(), rotations['s2'].copy()]
class Z(Piece):
    rotations = [rotations['z1'].copy(), rotations['z2'].copy()]
TETRONIMOS = {'I':I, 'S':S, 'Z':Z}
for tetronimo_name in 'JLT':
    TETRONIMOS[tetronimo_name] = type(tetronimo_name, (Piece,),
            {'rotations':generate_3x3_rotations(rotations[tetronimo_name.lower()])})
class NoPiece(Piece):
    rotations = [numpy.array([[0]])]

class Board(object):
    def __init__(self, height, width):
        self.board=numpy.zeros((height, width))
        self.current_piece = None
        self.bag = []
        self.lines=0
        self.start()
    width = property(lambda self:self.dims[1])
    height = property(lambda self:self.dims[0])
    dims = property(lambda self: self.board.shape)
    def __repr__(self):
        return str(self.board + self.current_piece.on_board(self.dims))
    def __str__(self):
        temp = self.board + self.current_piece.on_board(self.dims)
        s = ''
        for line in temp:
            for i in range(2):
                s += '\n'
                for x in line:
                    s += 'XXXXX' if x else '  .  '
        return s
    def start(self):
        self.current_piece = self.get_next_piece()
    def piece_place_collides(self):
        return numpy.max(self.current_piece.on_board(self.dims) + self.board) > 1
    def piece_place_through_floor(self):
        return self.current_piece.through_floor(self.dims)
    def piece_out_of_bounds(self):
        return not self.current_piece.in_bounds(self.dims)
    def piece_place_valid(self):
        return not (self.piece_place_collides() or
                    self.piece_out_of_bounds() or
                    self.piece_place_through_floor())
    def get_next_piece(self):
        if not self.bag:
            self.bag = list('IJLSTZ')
            random.shuffle(self.bag)
        return TETRONIMOS[self.bag.pop()](0, (self.dims[1] - 3)//2)
    def clear_lines(self):
        for row in range(self.dims[0]):
            if all(self.board[row]):
                self.board[1:row+1, :] = self.board[:row, :]
                self.board[0, :] = 0
                self.lines += 1
    def fall(self):
        self.current_piece.pos[0] += 1
        if self.piece_place_collides() or self.piece_place_through_floor():
            self.current_piece.pos[0] -= 1
            self.board = self.board + self.current_piece.on_board(self.dims)
            self.clear_lines()
            self.current_piece = self.get_next_piece()
            return False
        return True
    def right(self, delta=1):
        self.current_piece.pos[1] += delta
        if self.piece_place_collides() or self.piece_out_of_bounds():
            self.current_piece.pos[1] -= delta
            return False
        return True
    def left(self):
        return self.right(delta=-1)
    def rotate_right(self, offset=1):
        self.current_piece.rotate(offset)
        if self.piece_place_collides() or self.piece_out_of_bounds():
            self.current_piece.rotate(-offset)
            return False
        return True
    def rotate_left(self):
        self.rotate_right(offset=-1)

    def fall_without_new_piece(self):
        r = self.fall()
        self.current_piece = NoPiece(0,0)
        return r
    @property
    def total_blocks(self):
        return self.board.sum()
    @property
    def total_surface_area(self):
        return 0
    @property
    def top_surface_area(self):
        return 0
    @property
    def caverns(self):
        return 0
    @property
    def linear_height_penalty(self):
        penalty = numpy.hstack([[[x] for x in range(self.height, 0, -1)] for i in range(self.width)])
        return (penalty * self.board).sum()

def all_boards(board):
    possible = []
    for col in range(board.dims[1]):
        for row in range(board.dims[0]):
            for i in range(len(board.current_piece.rotations)):
                tempboard = deepcopy(board)
                tempboard.current_piece.rotate(i)
                tempboard.current_piece.pos = [row, col]
                if not tempboard.piece_place_valid():
                    continue
                if tempboard.fall_without_new_piece():
                    continue
                #TODO check if piece could actually get there!
                possible.append(tempboard)
    return possible

def evaluate(board):
    metrics = ['total_blocks', 'linear_height_penalty']
    data = {metric: getattr(board, metric) for metric in metrics}
    data['board'] = board
    return data

def play_test():
    b = Board(10, 8)
    while True:
        print b
        a = raw_input().lower()
        if a in ['d', 'r', 'right']:
            b.right()
        elif a in ['a', 'l', 'left']:
            b.left()
        elif a in ['e', 'rotate']:
            b.rotate_right()
        elif a in ['q']:
            b.rotate_left()
        else:
            b.fall()

if __name__ == '__main__':
    #play_test()
    real_board = Board(10, 8)
    while True:
        evaluations = [evaluate(b) for b in all_boards(real_board)]
        evaluations.sort(reverse=True, key=lambda x:x['total_blocks'] + x['linear_height_penalty'])
        for b in evaluations:
            pass #print b['board']
        print b['board']
        real_board.board = b['board'].board
        real_board.current_piece = real_board.get_next_piece()
        raw_input(str(real_board.lines))

