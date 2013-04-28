"""Tetronimos"""
import numpy
import board

__all__ = list("IJLSTZ") + ["TETRONIMOS"]

rotations = {
    'i1' :[[0,0,0,0],
           [0,0,0,0],
           [1,1,1,1],
           [0,0,0,0]],
    'i2' :[[0,1,0,0],
           [0,1,0,0],
           [0,1,0,0],
           [0,1,0,0]],
    'j' : [[0,0,0],
           [1,1,1],
           [0,0,1]],
    'l' : [[0,0,0],
           [1,1,1],
           [1,0,0]],
    's1' :[[0,0,0],
           [0,1,1],
           [1,1,0]],
    's2' :[[1,0,0],
           [1,1,0],
           [0,1,0]],
    't' : [[0,0,0],
           [1,1,1],
           [0,1,0]],
    'z1' :[[0,0,0],
           [1,1,0],
           [0,1,1]],
    'z2' :[[0,1,0],
           [1,1,0],
           [1,0,0]]}

for k, v in rotations.iteritems():
    rotations[k] = numpy.array(v, dtype=bool)

def generate_3x3_rotations(rotation):
    rotations = []
    for i in range(4):
        if i:
            rotation = numpy.rot90(rotation)
        rotations.append(rotation)
    return rotations

class Piece(object):
    def __init__(self, row, column):
        self._rotation_index = 0
        self.pos = [row, column]
    row = y = property(lambda self: self.pos[0])
    column = x = property(lambda self: self.pos[1])
    rotation = property(lambda self: self.rotations[self._rotation_index])
    def __repr__(self):
        return '<%s at %s, rot %s>' % (self.__class__.__name__, self.pos, self._rotation_index)
    def rotate(self, offset=1):
        self._rotation_index = (self._rotation_index + offset) % len(self.rotations)

    #TODO more efficient, clearner code for figuring out if position on board is legal?
    def on_board(self, dims=board.Board().array.shape):
        padded_board = self._on_padded_board(dims)
        empty_board_with_piece = padded_board[
                self.rotation.shape[0]:-self.rotation.shape[0],
                self.rotation.shape[1]:-self.rotation.shape[1]]
        return empty_board_with_piece
    def _on_padded_board(self, dims):
        padded_board = numpy.zeros((dims[0]+2*self.rotation.shape[0],
                                   dims[1]+2*self.rotation.shape[1]), dtype=bool)
        padded_board[self.rotation.shape[0]+self.pos[0]:self.pos[0]+2*self.rotation.shape[0],
                     self.rotation.shape[1]+self.pos[1]:self.pos[1]+2*self.rotation.shape[1]] = self.rotation
        return padded_board
    def in_bounds(self, dims):
        board = self.on_board(dims)
        return self.rotation.sum() == board.sum()
    def through_floor(self, dims):
        padded_board = self._on_padded_board(dims)
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
    piece = type(tetronimo_name, (Piece,),
            {'rotations':generate_3x3_rotations(rotations[tetronimo_name.lower()])})
    locals()[tetronimo_name] = piece
    TETRONIMOS[tetronimo_name] = piece
