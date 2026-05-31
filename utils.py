import numpy as np

np_solved = np.zeros((5, 5), dtype=int)
vec_solved = -1 * np.ones((5, 5), dtype=int)
solved = np_solved.tolist()
colours = ['gray', 'blue']

top_left = np.ones((5, 5), dtype=int)
top_left[0, 0], top_left[0, 1], top_left[1, 0] = -1, -1, -1
top_right = np.ones((5, 5), dtype=int)
top_right[0, 4], top_right[0, 3], top_right[1, 4] = -1, -1, -1
bottom_left = np.ones((5, 5), dtype=int)
bottom_left[4, 0], bottom_left[4, 1], bottom_left[3, 0] = -1, -1, -1
bottom_right = np.ones((5, 5), dtype=int)
bottom_right[4, 4], bottom_right[4, 3], bottom_right[3, 4] = -1, -1, -1

top_mid = np.ones((5, 5), dtype=int)
top_mid[0, 1:4], top_mid[1, 2] = -1, -1
bottom_mid = np.ones((5, 5), dtype=int)
bottom_mid[4, 1:4], bottom_mid[3, 2] = -1, -1
mid_left = np.ones((5, 5), dtype=int)
mid_left[1:4, 0], mid_left[2, 1] = -1, -1
mid_right = np.ones((5, 5), dtype=int)
mid_right[1:4, 4], mid_right[2, 3] = -1, -1

true_mid = np.ones((5, 5), dtype=int)
true_mid[1, 2], true_mid[2, 1:4], true_mid[3, 2] = -1, -1, -1

vec_toggle = np.array([
    top_left,
    np.roll(top_mid, -1, axis=1),
    top_mid,
    np.roll(top_mid, 1, axis=1),
    top_right,
    np.roll(mid_left, -1, axis=0),
    np.roll(true_mid, (-1, -1), axis=(0, 1)),
    np.roll(true_mid, -1, axis=0),
    np.roll(true_mid, (-1, 1), axis=(0, 1)),
    np.roll(mid_right, -1, axis=0),
    mid_left,
    np.roll(true_mid, -1, axis=1),
    true_mid,
    np.roll(true_mid, 1, axis=1),
    mid_right,
    np.roll(mid_left, 1, axis=0),
    np.roll(true_mid, (1, -1), axis=(0, 1)),
    np.roll(true_mid, 1, axis=0),
    np.roll(true_mid, (1, 1), axis=(0, 1)),
    np.roll(mid_right, 1, axis=0),
    bottom_left,
    np.roll(bottom_mid, -1, axis=1),
    bottom_mid,
    np.roll(bottom_mid, 1, axis=1),
    bottom_right
])


def int_to_pos(num):
    return num // 5, num % 5


chase_the_lights_key = {
    '00111': [int_to_pos(3)],
    '01010': [int_to_pos(1), int_to_pos(4)],
    '01101': [int_to_pos(0)],
    '10001': [int_to_pos(3), int_to_pos(4)],
    '10110': [int_to_pos(4)],
    '11011': [int_to_pos(2)],
    '11100': [int_to_pos(1)],
}


def update_grid(grid, i, j, setup=False):
    # Update the grid based on the button press
    if setup:
        grid[i][j] = 1 - grid[i][j]
    else:
        for x, y in [(i, j), (i-1, j), (i+1, j), (i, j-1), (i, j+1)]:
            if 0 <= x < 5 and 0 <= y < 5:
                grid[x][y] = 1 - grid[x][y]


def vec_update_grid(vec_grid, moves):
    # Update the grid using vectorized operations
    moves = np.array(moves)
    toggles = vec_toggle[moves]
    vec_grid *= np.prod(toggles, axis=0)


def generate_random_grid():
    # Generate a random grid by applying random moves to the solved state
    np_grid = np.copy(np_solved)
    # Number of moves to apply, between 1 and 25
    N = np.random.randint(1, 26)
    # Randomly select N unique moves from the 25 possible positions
    moves = np.random.choice(25, N, replace=False)
    moves = [int_to_pos(move) for move in moves]
    for i, j in moves:
        update_grid(np_grid, i, j)
    # return the list of moves and the resulting grid as a list of lists
    return moves, np_grid.tolist()


def list_to_vec(grid):
    np_grid = np.array(grid, dtype=int)
    vec_grid = np.where(np_grid == 0, -1, 1)
    return vec_grid


def vec_to_list(vec_grid):
    grid = np.where(vec_grid == -1, 0, 1)
    return grid.tolist()

