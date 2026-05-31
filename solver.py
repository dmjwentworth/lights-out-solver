import numpy as np
from tqdm import tqdm
from itertools import combinations
from utils import (
    int_to_pos,
    update_grid,
    np_solved,
    vec_solved,
    vec_update_grid,
    list_to_vec,
    )


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


def vec_check_games_of_N_moves(vec_grid, N):
    for moves in tqdm(combinations(range(25), N)):
        vec_grid_copy = np.copy(vec_grid)
        moves = [int_to_pos(move) for move in moves]
        for i, j in moves:
            vec_update_grid(vec_grid_copy, i, j)
        
        if np.array_equal(vec_grid_copy, vec_solved):
            print(f'\nFound a solution with {N} moves: {moves}')
            return moves
    
    print(f'No solution found with {N} moves.')
    return None


def vec_brute_force(grid):
    vec_grid = list_to_vec(grid)
    if np.array_equal(vec_grid, vec_solved):
        print('The grid is already solved.')
        return []
    
    for N in range(1, 26):
        print(f'\033[1;34mChecking for solutions with {N} moves...\033[0m')
        moves = vec_check_games_of_N_moves(vec_grid, N)
        if moves is not None:
            return moves
    
    print('No solution found.')
    return None


def solve(grid, fn=vec_brute_force):
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

