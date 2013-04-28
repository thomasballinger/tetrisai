
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
