import pygame
import random

# Initialize Pygame
pygame.init()

# Tetris game constants
GRID_WIDTH = 10
GRID_HEIGHT = 20
CELL_SIZE = 20
SCREEN_WIDTH = GRID_WIDTH * CELL_SIZE
SCREEN_HEIGHT = GRID_HEIGHT * CELL_SIZE
FPS = 30
GRAVITY = 1

# Tetris shapes
SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 1], [1, 1, 0]],
    [[1, 0, 0], [1, 1, 1]],
    [[0, 0, 1], [1, 1, 1]],
    [[1, 1, 1], [0, 0, 1]],
]


class TetrisGame:
    def __init__(self):
        self.board = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]
        self.current_piece = self.generate_piece()
        self.next_piece = self.generate_piece()
        self.score = 0
        self.gravity_timer = FPS

    def generate_piece(self):
        shape = random.choice(SHAPES)
        piece = {"shape": shape, "row": 0, "col": GRID_WIDTH // 2 - len(shape[0]) // 2}
        return piece

    def rotate_piece(self):
            rotated_shape = list(map(list, zip(*reversed(self.current_piece["shape"]))))
            if self.is_valid_move(
                rotated_shape,
                self.current_piece["row"],
                self.current_piece["col"]
                ):
                self.current_piece["shape"] = rotated_shape

    def move_piece_left(self):
            if self.is_valid_move(
                self.current_piece["shape"],
                self.current_piece["row"],
                self.current_piece["col"] - 1
                ):
                self.current_piece["col"] -= 1


    def move_piece_right(self):
            if self.is_valid_move(
                self.current_piece["shape"], 
                self.current_piece["row"], 
                self.current_piece["col"] + 1
                ):
                self.current_piece["col"] += 1

    def move_piece_down(self):
        if self.is_valid_move(
            self.current_piece["shape"], 
            self.current_piece["row"] + 1, 
            self.current_piece["col"]
            ):
            self.current_piece["row"] += 1
        else:
            self.place_piece()
    
    def speed_move_piece_down(self):
            if self.is_valid_move(
                self.current_piece["shape"], 
                self.current_piece["row"] + 1, 
                self.current_piece["col"]
                ):
                self.current_piece["row"] += 1


    def place_piece(self):
        shape = self.current_piece["shape"]
        row = self.current_piece["row"]
        col = self.current_piece["col"]

        for i in range(len(shape)):
            for j in range(len(shape[0])):
                if shape[i][j] == 1:
                    self.board[row + i][col + j] = 1

        self.clear_lines()
        self.current_piece = self.next_piece
        self.next_piece = self.generate_piece()

        if not self.is_valid_move(
            self.current_piece["shape"],
            self.current_piece["row"],
            self.current_piece["col"],
        ):
            self.reset()

    def clear_lines(self):
        full_lines = []
        for i in range(GRID_HEIGHT):
            if all(self.board[i]):
                full_lines.append(i)

        for line in full_lines:
            self.board.pop(line)
            self.board.insert(0, [0] * GRID_WIDTH)

        self.score += len(full_lines)

    def is_valid_move(self, shape, row, col):
        for i in range(len(shape)):
            for j in range(len(shape[0])):
                if (shape[i][j] == 1) and (
                    (row + i >= GRID_HEIGHT)
                    or (col + j < 0 or col + j >= GRID_WIDTH)
                    or (self.board[row + i][col + j])
                ):
                    return False
        return True

    def reset(self):
        self.board = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]
        self.current_piece = self.generate_piece()
        self.next_piece = self.generate_piece()
        self.score = 0


# Initialize game display
display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris Game")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (33, 102, 196)
GREEN = (92, 184, 92)
RED = (217, 83, 79)

# Initialize Game
game = TetrisGame()

clock = pygame.time.Clock()
is_running = True

key_state = {
    pygame.K_LEFT: False,
    pygame.K_RIGHT: False,
    pygame.K_DOWN: False,
    pygame.K_UP: False
}

while is_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                key_state[pygame.K_LEFT] = True
            elif event.key == pygame.K_RIGHT:
                key_state[pygame.K_RIGHT] = True
            elif event.key == pygame.K_DOWN:
                key_state[pygame.K_DOWN] = True
            elif event.key == pygame.K_UP:
                key_state[pygame.K_UP] = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                key_state[pygame.K_LEFT] = False
            elif event.key == pygame.K_RIGHT:
                key_state[pygame.K_RIGHT] = False
            elif event.key == pygame.K_DOWN:
                key_state[pygame.K_DOWN] = False
            elif event.key == pygame.K_UP:
                key_state[pygame.K_UP] = False
    
    if key_state[pygame.K_LEFT]:
        game.move_piece_left()
    if key_state[pygame.K_RIGHT]:
        game.move_piece_right()
    if key_state[pygame.K_DOWN]:
        game.speed_move_piece_down()
    if key_state[pygame.K_UP]:
        game.rotate_piece()
    
    clock.tick(FPS)   
        
    # Update game logic
    
    game.gravity_timer -= 1
    if game.gravity_timer == 0:
        game.move_piece_down()
        game.gravity_timer = FPS // GRAVITY

    # Update display
    display.fill(BLACK)

    # Draw board
    for i in range(GRID_HEIGHT):
        for j in range(GRID_WIDTH):
            if game.board[i][j] == 1:
                pygame.draw.rect(
                    display, GREEN, (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                )
            pygame.draw.rect(
                display, WHITE, (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1
            )

    # Draw current piece
    shape = game.current_piece["shape"]
    row = game.current_piece["row"]
    col = game.current_piece["col"]
    for i in range(len(shape)):
        for j in range(len(shape[0])):
            if shape[i][j] == 1:
                pygame.draw.rect(
                    display,
                    BLUE,
                    (
                        (col + j) * CELL_SIZE,
                        (row + i) * CELL_SIZE,
                        CELL_SIZE,
                        CELL_SIZE,
                    ),
                )

    pygame.display.update()
    clock.tick(FPS)

# Quit the game
pygame.quit()