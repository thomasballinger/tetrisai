"""
Nintendo Tetris Rules - because that's the 20% I'm intersted in

Using Left-handed rotation rules (used Game Boy Tetris)


"""
import random
from board import Board

from pieces import *


class Game(object):
    def __init__(self, height, width):
        self.board=Board()
        self.current_piece = None
        self.bag = []
        self.lines=0
        self.start()
    dims = property(lambda self: self.board.array.shape)
    def __str__(self):
        temp = self.board.add_floating_piece(self.current_piece)
        return str(temp)
    def start(self):
        self.current_piece = self.get_next_piece()
    def piece_place_collides(self):
        return (self.current_piece.on_board(self.dims) & self.board.array).any()
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
        self.board = self.board.cleared()
    def fall(self):
        self.current_piece.pos[0] += 1
        if self.piece_place_collides() or self.piece_place_through_floor():
            self.current_piece.pos[0] -= 1
            self.board = self.board + self.current_piece

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

def play_test():
    g = Game(10, 8)
    while True:
        print g
        a = raw_input().lower()
        if a in ['d', 'r', 'right']:
            g.right()
        elif a in ['a', 'l', 'left']:
            g.left()
        elif a in ['e', 'rotate']:
            g.rotate_right()
        elif a in ['q']:
            g.rotate_left()
        else:
            g.fall()

if __name__ == '__main__':
    play_test()

