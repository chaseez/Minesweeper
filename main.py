import pygame
import random
from square import Square


class MineSweeperBoard():
    def __init__(self, board_size):
        self.HARD = 99
        self.MEDIUM = 50
        self.EASY = 25
        self.BEGINNER = 10
        self.board = []
        self.board_size = board_size
        self.difficulty = self.MEDIUM
        self.set_up_board(board_size)
    def set_up_board(self, board_size):
        for i in range(board_size):
            row = []
            for j in range(board_size):
                row.append(Square(i, j))
            self.board.append(row)
        self.put_bombs()

    def put_bombs(self):
        bomb_coord = set()

        while len(bomb_coord) < self.difficulty:
            x_coord = random.randint(0, self.board_size-1)
            y_coord = random.randint(0, self.board_size-1)

            if (x_coord, y_coord) not in bomb_coord:
                bomb_coord.add((x_coord, y_coord))
                self.board[x_coord][y_coord].is_bomb = True

        self.count_bombs()

    def count_bombs(self):
        for row in self.board:
            for square in row:
                if square.is_bomb:
                    self.count_surrounding_bombs(square)

        # for x, y in bomb_coord:
        #     if 0 < x < self.board_size - 1 and 0 < y < self.board_size - 1:
        #         self.count_bomb(x, y)
        #     elif x == 0 and 0 < y < self.board_size - 1:
        #         self.count_top_row_bomb(x, y)
        #     elif x == self.board_size - 1 and 0 < y < self.board_size - 1:
        #         self.count_bottom_row_bomb(x, y)
        #     elif y == 0 and 0 < x < self.board_size - 1:
        #         self.count_first_col_bomb(x, y)
        #     elif y == self.board_size - 1 and 0 < x < self.board_size - 1:
        #         self.count_last_col_bomb(x, y)

    def count_surrounding_bombs(self, square):
        top_row = 0
        bottom_row = self.board_size - 1
        left_most_col = 0
        right_most_col = self.board_size -1

        for row in range(square.row - 1, square.row + 2):
            # Top and Bottom guard
            if top_row <= row <= bottom_row:
                for col in range(square.col - 1, square.col + 2):
                    # Left and Right Guard
                    if left_most_col <= col <= right_most_col:
                        if not self.board[row][col].is_bomb:
                            self.board[row][col].surrounding_bombs += 1

    def print_board_details(self):
        for row in self.board:
            row_details = []
            for col in row:
                row_details.append(f'Bomb: {col.is_bomb}, Coordinate: ({col.row}, {col.col}), Surrounding Bombs: {col.surrounding_bombs}')
            print(row_details)

    def print_board(self):
        for row in self.board:
            row_details = []
            for col in row:
                if col.is_bomb:
                    row_details.append("Bomb")
                else:
                    row_details.append(str(col.surrounding_bombs) + '\t')
            print(", ".join(row_details))

if __name__ == "__main__":
    game = MineSweeperBoard(15)

    game.print_board()