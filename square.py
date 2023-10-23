class Square():
    def __init__(self, row, col):
        self.is_bomb = False
        self.row = row
        self.col = col
        self.surrounding_bombs = 0
