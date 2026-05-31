import numpy as np
from tqdm import tqdm
from itertools import combinations
from utils import int_to_pos, update_grid, np_solved


def check_games_of_N_moves(grid, N):
    for moves in tqdm(combinations(range(25), N)):
        np_grid = np.array(grid, dtype=int)
        moves = [int_to_pos(move) for move in moves]
        for i, j in moves:
            update_grid(np_grid, i, j)
        
        if np.array_equal(np_grid, np_solved):
            print(f'\nFound a solution with {N} moves: {moves}')
            return moves
    
    print(f'No solution found with {N} moves.')
    return None


def brute_force(grid):
    if np.array_equal(np.array(grid, dtype=int), np_solved):
        print('The grid is already solved.')
        return []

    for N in range(1, 26):
        print(f'\033[1;34mChecking for solutions with {N} moves...\033[0m')
        moves = check_games_of_N_moves(grid, N)
        if moves is not None:
            return moves
    
    print('No solution found.')
    return None


def solve(grid, fn=brute_force):
    return fn(grid)


def main():
    grid = [
        [0, 1, 0, 0, 0],
        [1, 1, 1, 0, 0],
        [0, 1, 0, 1, 0],
        [0, 0, 1, 1, 1],
        [0, 0, 0, 1, 0]
    ]
    
    moves = solve(grid)
    if moves is not None:
        print(f'Solution found:\n{moves}')
    else:
        print('No solution found.')


if __name__ == '__main__':
    main()

