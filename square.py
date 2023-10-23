class Square():
    def __init__(self, row, col):
        self.is_bomb = False
        self.row = row
        self.col = col
        self.surrounding_bombs = 0
        self.flagged = False
        self.discovered = False

    def print_info(self):
        print(f'Bomb: {self.is_bomb}, Coordinate: ({self.row}, {self.col}), Surrounding Bombs: {self.surrounding_bombs}')
