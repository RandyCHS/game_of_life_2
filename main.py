import pygame
import math
from random import randint

# ---
# View code - shouldn't need to touch!

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

WHITE = (255, 255, 255)
RED = (255, 0, 0)


def initialize_view():
    """
    Sets up the pygame environment for drawing
    """
    pygame.init()
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Game of Life")
    return screen


def draw_view_grid(screen):
    """
    Draw a single view of the grid
    """
    margin = 1
    rows, cols = len(grid), len(grid[0])
    block_size = math.floor((SCREEN_HEIGHT - (rows * margin)) / rows)
    for i in range(rows):
        for j in range(cols):
            rect = pygame.Rect(
                j * (block_size + margin),
                i * (block_size + margin),
                block_size,
                block_size
            )
            if grid[i][j] == 0:
                pygame.draw.rect(screen, WHITE, rect)
            else:
                pygame.draw.rect(screen, RED, rect)


def draw_view(screen, update_function, interval):
    """
    Constant updating of the grid calling the
    update_function at the specified interval
    """
    refresh_grid_event = pygame.USEREVENT + 1
    pygame.time.set_timer(refresh_grid_event, interval)

    done = False
    clock = pygame.time.Clock()
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == refresh_grid_event:
                draw_view_grid(screen)
                update_function()
        clock.tick(60)
        pygame.display.flip()


def close_view():
    """
    Shut down the view
    """
    pygame.quit()

# ---

# Code that we should let the students write
ROWS = 50
COLS = 50

grid = []
next_grid = []

def initialize_grids():
    for i in range(ROWS):
        grid.append([])
        next_grid.append([])
        for j in range(COLS):
            grid[i].append(0)
            next_grid[i].append(0)


def copy_and_reset_grid():
    for i in range(ROWS):
        for j in range(COLS):
            grid[i][j] = next_grid[i][j]
            next_grid[i][j] = 0


def print_grid():
    for i in range(ROWS):
        print(" ".join([str(grid[i][j]) for j in range(COLS)]))
    print()


def seed_test_grid():
    grid[1][1] = 1
    grid[2][1] = 1
    grid[3][1] = 1


def seed_random_grid(proportion):
    from random import randint
    num_cells = math.floor(ROWS * COLS * proportion)
    used = []
    i = 0
    while i < num_cells:
        rand_row = randint(0, ROWS - 1)
        rand_col = randint(0, COLS - 1)
        if (rand_row, rand_col) in used:
            continue
        used.append((rand_row, rand_col))
        grid[rand_row][rand_col] = 1
        i += 1


def seed_glider_grid(number):
    pattern = ((0, 0), (0, 1), (0, 2), (1, 0), (2, 1))
    for i in range(number):
        rand_row = randint(0, ROWS - 3)
        rand_col = randint(0, COLS - 3)
        for p in pattern:
            grid[rand_row + p[0]][rand_col + p[1]] = 1


def compute_next_gen():
  for i in range(ROWS):
    for j in range(COLS):
        apply_rules(i, j)
  # copy next_grid to grid, and reset next_grid
  copy_and_reset_grid()


def apply_rules(row, col):
    num_neighbors = count_neighbors(row, col)
    if grid[row][col] == 1:
        if num_neighbors < 2:
            next_grid[row][col] = 0
        elif num_neighbors == 2 or num_neighbors == 3:
            next_grid[row][col] = 1
        elif num_neighbors > 3:
            next_grid[row][col] = 0
    elif grid[row][col] == 0:
        if num_neighbors == 3:
            next_grid[row][col] = 1


def count_neighbors(row, col):
    count = 0
    if row-1 >= 0 and col-1 >= 0:
        if grid[row-1][col-1] == 1:
            count += 1
    if row-1 >= 0:
        if grid[row-1][col] == 1:
            count += 1
    if row-1 >= 0 and col+1 < COLS:
        if grid[row-1][col+1] == 1:
            count += 1
    if col-1 >= 0:
        if grid[row][col-1] == 1:
            count += 1
    if col+1 < COLS:
        if grid[row][col+1] == 1:
            count += 1
    if row+1 < ROWS and col-1 >= 0:
        if grid[row+1][col-1] == 1:
            count += 1
    if row+1 < ROWS:
        if grid[row+1][col] == 1:
            count += 1
    if row+1 < ROWS and col+1 < COLS:
        if grid[row+1][col+1] == 1:
            count += 1
    return count


def main():
    # Set up the pygame environment
    screen = initialize_view()

    # Set up the "models" that store the game play
    initialize_grids()

    # Use one of these to seed the initial grid and
    # comment out the other two
    # - seed_test_grid is just to make sure that
    #   the logic is working
    # - seed_random_grid sets the grid to the
    #   proportion specified as alive (red)
    # - seed_glider_grid sets up "gliders" that
    #   move across the landscape.  Use the parameter
    #   to specify how many gliders to randomly place
       
    # seed_test_grid()
    seed_random_grid(0.4)
    # seed_glider_grid(10)

    # Play the game.  The second parameter is the function
    # that implements the rules, which holds the model logic
    # that determines the next generation.  The third parameter
    # specifies the refresh rate in milliseconds (e.g. 1000 = 1 sec)
    draw_view(screen, compute_next_gen, 500)

    # Clean up the pygame en
    close_view()

if __name__ == '__main__':
    main()