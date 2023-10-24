import pygame
import random

from pygame import Rect

from square import Square


class MineSweeperBoard():
    def __init__(self, board_size, row, col):
        self.HARD = 99
        self.MEDIUM = 50
        self.EASY = 25
        self.BEGINNER = 10

        self.difficulty = self.MEDIUM

        self.board = []
        self.BOARD_SIZE = board_size

        self.TOP_ROW = 0
        self.BOTTOM_ROW = self.BOARD_SIZE - 1
        self.LEFT_MOST_COL = 0
        self.RIGHT_MOST_COL = self.BOARD_SIZE - 1

        self.first_x = col
        self.first_y = row

        self.set_up_board(board_size)

    def discover_squares(self, row, col):
        for row_index in range(row - 1, row + 2):
            if self.TOP_ROW <= row_index <= self.BOTTOM_ROW:
                for col_index in range(col - 1, col + 2):
                    if self.LEFT_MOST_COL <= col_index <= self.RIGHT_MOST_COL:
                        if self.board[row_index][col_index].is_bomb: continue

                        if self.board[row_index][col_index].surrounding_bombs == 0 and not self.board[row_index][col_index].discovered:
                            self.board[row_index][col_index].discovered = True
                            self.discover_squares(row_index, col_index)
                        else:
                            self.board[row_index][col_index].discovered = True

    def set_up_board(self, board_size):
        for row in range(board_size):
            row_details = []
            for col in range(board_size):
                row_details.append(Square(row, col))
            self.board.append(row_details)
        self.put_bombs()

    def put_bombs(self):
        bomb_coord = set()

        while len(bomb_coord) < self.difficulty:
            row_coord = random.randint(0, self.BOARD_SIZE - 1)
            col_coord = random.randint(0, self.BOARD_SIZE - 1)

            if (row_coord, col_coord) not in bomb_coord:
                row_clear = False
                col_clear = False

                if row_coord <= self.first_y - 2 or row_coord >= self.first_y + 2:
                    row_clear = True
                if col_coord <= self.first_x - 2 or col_coord >= self.first_x + 2:
                    col_clear = True

                if row_clear or col_clear:
                    bomb_coord.add((row_coord, col_coord))
                    self.board[row_coord][col_coord].is_bomb = True

        self.count_bombs()

    def count_bombs(self):
        for row in self.board:
            for square in row:
                if square.is_bomb:
                    self.count_surrounding_bombs(square)

    def count_surrounding_bombs(self, bomb):

        for row in range(bomb.row - 1, bomb.row + 2):
            # Top and Bottom guard
            if self.TOP_ROW <= row <= self.BOTTOM_ROW:
                for col in range(bomb.col - 1, bomb.col + 2):
                    # Left and Right Guard
                    if self.LEFT_MOST_COL <= col <= self.RIGHT_MOST_COL:
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
                    row_details.append("B")
                else:
                    row_details.append(str(col.surrounding_bombs))
            print("\t".join(row_details))


class MineSweeperGUI():
    def __init__(self):
        self.board_rect = []
        self.board_size = 15
        self.board = MineSweeperBoard(self.board_size, 7, 7)

        # Define the background colour
        # using RGB color coding.
        self.GREY = (112,112,112) # Unvisited
        self.BLACK = (0,0,0) # Background
        self.WHITE = (255,255,255) # Flagged
        self.SILVER = (192,192,192) # 0 Bombs
        self.BLUE = (0, 0, 255) # 1 bomb
        self.GREEN = (0,255,0) # 2 bombs
        self.RED = (255,0,0) # 3 bombs
        self.PURPLE = (128,0,128) # 4 Bombs
        self.ORANGE = (255, 165, 0) # 5 Bombs
        self.CYAN = (0,255,255) # 6 Bombs
        self.PINK = (255,192,203) # 7 Bombs
        self.MAROON = (128,0,0) # 8 Bombs


        self.background_colour = self.BLACK
        self.height = 600
        self.width = 600
        self.rect_size = 30

        # Define the dimensions of
        # screen object(width,height)
        self.screen = pygame.display.set_mode((self.height, self.width))

        # Set the caption of the screen
        pygame.display.set_caption('Mine Sweeper')

        # Fill the background colour to the screen
        self.screen.fill(self.background_colour)

        # Update the display using flip
        pygame.display.flip()

        self.RUNNING = True
        self.EXIT = False

        # Variable to keep our game loop running
        self.game_state = self.RUNNING

        self.game_loop()

    def game_loop(self):
        # game loop
        drawn = False
        first_click = True
        total_flags  = self.board.difficulty
        while self.game_state:

            # for loop through the event queue
            for event in pygame.event.get():

                # Check for QUIT event
                if event.type == pygame.QUIT:
                    self.game_state = self.EXIT
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # When a box is clicked
                    if event.button == pygame.BUTTON_LEFT:
                        # Initializing the variables
                        top_bound = 0
                        bottom_bound = 0
                        right_bound = 0
                        left_bound = 0
                        found = False

                        for row in self.board_rect:
                            for rect, square in row:
                                top_bound = rect.y
                                bottom_bound = rect.y + self.rect_size

                                left_bound = rect.x
                                right_bound = rect.x + self.rect_size

                                # event.pos = (x,y)
                                # event.pos[0] = x
                                # event.pos[1] = y
                                if left_bound <= event.pos[0] <= right_bound and \
                                    top_bound <= event.pos[1] <= bottom_bound:
                                    if first_click:
                                        # Make sure the first click isn't landed on a bomb
                                        self.board = MineSweeperBoard(self.board_size, square.row, square.col)

                                        first_click = False
                                    square.discovered = True
                                    # square.print_info()
                                    if square.is_bomb:
                                        self.game_state = self.EXIT
                                    if square.surrounding_bombs == 0:
                                        self.board.discover_squares(square.row, square.col)
                                    self.draw_board()
                                    self.show_discovered()
                                    # self.board.print_board()
                                    found = True
                                    break
                            if found:
                                break

                    elif event.button == pygame.BUTTON_RIGHT:
                        # Initializing the variables
                        top_bound = 0
                        bottom_bound = 0
                        right_bound = 0
                        left_bound = 0
                        found = False

                        for row in self.board_rect:
                            for rect, square in row:
                                top_bound = rect.y
                                bottom_bound = rect.y + self.rect_size

                                left_bound = rect.x
                                right_bound = rect.x + self.rect_size

                                # event.pos = (x_pos, y_pos)
                                # event.pos[0] = x_pos
                                # event.pos[1] = y_pos
                                # Checking if the click was within a square
                                if left_bound <= event.pos[0] <= right_bound and top_bound <= event.pos[1] <= bottom_bound:

                                    if not square.flagged:
                                        pygame.draw.rect(self.screen, self.WHITE, rect)
                                        square.flagged = True
                                        total_flags -= 1
                                    else:
                                        pygame.draw.rect(self.screen, self.GREY, rect)
                                        square.flagged = False
                                        total_flags += 1

                                    pygame.display.update()

                                    found = True
                                    break
                            if found:
                                break

            if total_flags == 0:
                self.game_state = self.EXIT

            if not drawn:
                drawn = self.draw_board()

    def draw_board(self):
        self.board_rect = []
        # Starting at in at the coord (50,50)
        y = 50
        x = 50
        for row in self.board.board:
            row_rect = []
            for square in row:
                rect = Rect(x, y, 30, 30)
                pygame.draw.rect(self.screen, self.GREY, rect)
                pygame.display.update()
                x += 35

                # Add tuple of rectangle with the square
                row_rect.append((rect, square))
            # Increase y step and reset x (column) coordinate
            y += 35
            x = 50

            # Associate the row with the rectangles
            self.board_rect.append(row_rect)
        return True

    def show_discovered(self):
        color = None

        discovered = [(rect,square) for row in self.board_rect for rect, square in row if square.discovered or square.flagged]
        # for row in self.board_rect:
        #     for rect, square in row:
        for rect, square in discovered:
            if square.surrounding_bombs == 1:
                color = self.BLUE
            elif square.surrounding_bombs == 2:
                color = self.GREEN
            elif square.surrounding_bombs == 3:
                color = self.RED
            elif square.surrounding_bombs == 4:
                color = self.PURPLE
            elif square.surrounding_bombs == 5:
                color = self.ORANGE
            elif square.surrounding_bombs == 6:
                color = self.CYAN
            elif square.surrounding_bombs == 7:
                color = self.PINK
            elif square.surrounding_bombs == 8:
                color = self.MAROON
            elif square.flagged:
                color = self.WHITE
            elif square.surrounding_bombs == 0:
                color = self.SILVER
            pygame.draw.rect(self.screen, color, rect)
            pygame.display.update()



if __name__ == "__main__":

    MineSweeperGUI()