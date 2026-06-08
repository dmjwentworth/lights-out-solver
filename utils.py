import numpy as np

# -----------------------------------------------------------------------------
# For non-vectorised updating of the grid
# -----------------------------------------------------------------------------


def int_to_pos(num):
    return num // 5, num % 5


def update_grid(grid, i, j, setup=False):
    # Update the grid based on the button press
    if setup:
        grid[i][j] = 1 - grid[i][j]
    else:
        for x, y in [(i, j), (i-1, j), (i+1, j), (i, j-1), (i, j+1)]:
            if 0 <= x < 5 and 0 <= y < 5:
                grid[x][y] = 1 - grid[x][y]


def generate_random_grid():
    # Generate a random grid by applying random moves to the solved state
    np_grid = np.copy(np_solved)
    # Flip a coin 25 times, heads = 1, tails = 0
    x = np.random.choice(2, 25, replace=True)
    # If heads, press the button and update the grid accordingly
    moves = [i for i in range(25) if x[i] == 1]
    moves = [int_to_pos(move) for move in moves]
    for i, j in moves:
        update_grid(np_grid, i, j)
    # return the list of moves and the resulting grid as a list of lists
    return moves, np_grid.tolist()


# -----------------------------------------------------------------------------
# For vectorised operations
# -----------------------------------------------------------------------------

np_solved = np.zeros((5, 5), dtype=int)
vec_solved = np.ones((5, 5), dtype=int)
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


def vec_update_grid(vec_grid, moves):
    # Update the grid using vectorized operations
    moves = np.array(moves)
    toggles = vec_toggle[moves]
    vec_grid *= np.prod(toggles, axis=0)


def list_to_vec(grid):
    np_grid = np.array(grid, dtype=int)
    vec_grid = np.where(np_grid == 0, 1, -1)
    return vec_grid


def vec_to_list(vec_grid):
    grid = np.where(vec_grid == 1, 0, 1)
    return grid.tolist()


# -----------------------------------------------------------------------------
# For the chase the lights algorithm
# -----------------------------------------------------------------------------

chase_the_lights_key = {
    '00111': [int_to_pos(3)],
    '01010': [int_to_pos(1), int_to_pos(4)],
    '01101': [int_to_pos(0)],
    '10001': [int_to_pos(3), int_to_pos(4)],
    '10110': [int_to_pos(4)],
    '11011': [int_to_pos(2)],
    '11100': [int_to_pos(1)],
}

# -----------------------------------------------------------------------------
# For the brute-force-v2 algorithm
# -----------------------------------------------------------------------------

possible_init_moves = [6, 8, 12, 16, 18]
remaining_moves = [i for i in range(25) if i not in possible_init_moves]
one_light_key = {
    6: [1, 3, 5, 6, 8, 9, 13, 15, 16, 17, 21],
    8: [1, 3, 5, 6, 8, 9, 11, 17, 18, 19, 23],
    12: [0, 1, 7, 10, 12, 13, 15, 19, 21, 22, 24],
    16: [1, 5, 6, 7, 13, 15, 16, 18, 19, 21, 23],
    18: [3, 7, 8, 9, 11, 15, 16, 18, 19, 21, 23]
}

def check_initial_moves(vec_grid):
    init_moves = []
    flat_grid = vec_grid.flatten()
    for possible_init_move, lights in one_light_key.items():
        lights_of_interest = flat_grid[lights]
        if np.prod(lights_of_interest) == -1:
            init_moves.append(possible_init_move)
    return init_moves

