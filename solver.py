import numpy as np
from tqdm import tqdm
from pprint import pprint
from itertools import combinations
from utils import (
    int_to_pos,
    update_grid,
    np_solved,
    vec_solved,
    vec_update_grid,
    list_to_vec,
    chase_the_lights_key,
    check_initial_moves,
    remaining_moves
)


def check_games_of_N_moves(grid, N):
    for moves in tqdm(combinations(range(25), N)):
        np_grid = np.array(grid, dtype=int)
        moves = [int_to_pos(move) for move in moves]
        for i, j in moves:
            update_grid(np_grid, i, j)
        
        if np.array_equal(np_grid, np_solved):
            print(f'\nFound a solution with {N} moves:')
            pprint(moves, width=40, compact=True)
            return moves
    
    print(f'No solution found with {N} moves.')
    return None


def brute_force(grid):
    for N in range(1, 26):
        print(f'\033[1;34mChecking for solutions with {N} moves...\033[0m')
        moves = check_games_of_N_moves(grid, N)
        if moves is not None:
            return moves
    
    print('No solution found for this configuration.')
    return []


def vec_check_games_of_N_moves(vec_grid, N):
    for moves in tqdm(combinations(range(25), N)):
        vec_grid_copy = np.copy(vec_grid)
        vec_update_grid(vec_grid_copy, moves)
        
        if np.array_equal(vec_grid_copy, vec_solved):
            moves = [int_to_pos(move) for move in moves]
            print(f'\nFound a solution with {N} moves:')
            pprint(moves, width=40, compact=True)
            return moves
    
    print(f'No solution found with {N} moves.')
    return None


def vec_brute_force(grid):
    vec_grid = list_to_vec(grid)
    for N in range(1, 26):
        print(f'\033[1;34mChecking for solutions with {N} moves...\033[0m')
        moves = vec_check_games_of_N_moves(vec_grid, N)
        if moves is not None:
            return moves
    
    print('No solution found for this configuration.')
    return []


def chase_the_lights(grid):
    np_grid = np.array(grid, dtype=int)
    moves = []
    for row in range(4):
        for col in range(5):
            if np_grid[row][col] == 1:
                update_grid(np_grid, row + 1, col)
                moves.append((row + 1, col))
    
    final_row = np_grid[4]
    if np.any(final_row):
        final_row = ''.join(str(x) for x in final_row)
        try:
            new_moves = chase_the_lights_key[final_row]
        except KeyError:
            print(f'No solution found for this configuration.')
            return []
        
        for move in new_moves:
            update_grid(np_grid, *move)
            moves.append(move)

        for row in range(4):
            for col in range(5):
                if np_grid[row][col] == 1:
                    update_grid(np_grid, row + 1, col)
                    if (row + 1, col) in moves:
                        moves.remove((row + 1, col))
                    else:
                        moves.append((row + 1, col))
    
    print(f'Found a solution with {len(moves)} moves:')
    pprint(moves, width=40, compact=True)
    return moves


def brute_force_v2(grid):
    # First, check if the solution will involve toggling any of the 5 "special"
    # positions (6, 8, 12, 16, 18)
    vec_grid = list_to_vec(grid)
    init_moves = check_initial_moves(vec_grid)
    N_init = len(init_moves)
    vec_update_grid(vec_grid, init_moves)

    # If the grid is already solved after the initial moves, return those moves
    if np.array_equal(vec_grid, vec_solved):
        print(f'Found a solution with {N_init} moves:')
        pprint(
            [int_to_pos(move) for move in init_moves],
            width=40,
            compact=True
        )
        return init_moves

    # Otherwise, we need to check combinations of the remaining moves
    for N in range(1, 21):
        print(
            '\033[1;34m'
            + f'Checking for solutions with {N_init + N} moves...'
            + '\033[0m'
        )
        for moves in tqdm(combinations(remaining_moves, N)):
            vec_grid_copy = np.copy(vec_grid)
            vec_update_grid(vec_grid_copy, moves)
            
            if np.array_equal(vec_grid_copy, vec_solved):
                moves = init_moves + list(moves)
                moves = [int_to_pos(move) for move in moves]
                print(f'\nFound a solution with {N_init + N} moves:')
                pprint(moves, width=40, compact=True)
                return moves
            
        print(f'No solution found with {N_init + N} moves.')
    
    print('No solution found for this configuration.')
    return []

