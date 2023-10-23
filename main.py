import pygame
import random

from pygame import Rect

from square import Square


class MineSweeperBoard():
    def __init__(self, board_size, first_x, first_y):
        self.HARD = 99
        self.MEDIUM = 50
        self.EASY = 25
        self.BEGINNER = 10
        self.board = []
        self.board_size = board_size
        self.difficulty = self.MEDIUM
        self.first_x = first_x
        self.first_y = first_y
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
                x_clear = False
                y_clear = False

                if x_coord <= self.first_x - 2 or x_coord >= self.first_x + 2:
                    x_clear = True
                if y_coord <= self.first_y - 2 or y_coord >= self.first_y + 2:
                    y_clear = True

                if x_clear and y_clear:
                    bomb_coord.add((x_coord, y_coord))
                    self.board[x_coord][y_coord].is_bomb = True

        self.count_bombs()

    def count_bombs(self):
        for row in self.board:
            for square in row:
                if square.is_bomb:
                    self.count_surrounding_bombs(square)

    def count_surrounding_bombs(self, bomb):
        top_row = 0
        bottom_row = self.board_size - 1
        left_most_col = 0
        right_most_col = self.board_size -1

        for row in range(bomb.row - 1, bomb.row + 2):
            # Top and Bottom guard
            if top_row <= row <= bottom_row:
                for col in range(bomb.col - 1, bomb.col + 2):
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
        self.GREY = (112,112,112)
        self.BLACK = (0,0,0)
        self.WHITE = (255,255,255)
        self.RED = (255,0,0)

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
                                        self.board = MineSweeperBoard(self.board_size, event.pos[0], event.pos[1])
                                        self.draw_board()

                                        first_click = False
                                    # TODO: Add in a discovered flag and algorithm to mark all the surrounding 0's
                                    # TODO: and adjacent non 0 squares as discovered. Don't show the bombs
                                    square.print_info()
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

                                # event.pos = (x,y)
                                # event.pos[0] = x
                                # event.pos[1] = y
                                # Checking if the click was within a square
                                if left_bound <= event.pos[0] <= right_bound and top_bound <= event.pos[1] <= bottom_bound:

                                    if not square.flagged:
                                        pygame.draw.rect(self.screen, self.RED, rect)
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


            if not drawn:
                drawn = self.draw_board()

    def draw_board(self):
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


if __name__ == "__main__":

    MineSweeperGUI()