import numpy as np
from tqdm import tqdm
from pprint import pprint
from itertools import combinations
from patterns import (
    chase_the_lights_key,
    remaining_moves,
    couples,
    brothers,
    cousins,
)
from utils import (
    int_to_pos,
    update_grid,
    np_solved,
    vec_solved,
    vec_update_grid,
    list_to_vec,
    check_initial_moves,
    find_coupling_parity,
    find_n_seeds_to_choose,
    timed,
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
    print('\n===== Solving via brute force (v1) =====')
    vec_grid = list_to_vec(grid)
    for N in range(1, 26):
        print(f'\033[1;34mChecking for solutions with {N} moves...\033[0m')
        moves = vec_check_games_of_N_moves(vec_grid, N)
        if moves is not None:
            return moves
    
    print('No solution found for this configuration.')
    return []


def chase_the_lights(grid):
    print('\n==== Solving via chasing the lights ====')
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
    print('\n===== Solving via brute force (v2) =====')
    # First, check if the solution will involve toggling any of the 5 "special"
    # positions (6, 8, 12, 16, 18)
    vec_grid = list_to_vec(grid)
    init_moves = check_initial_moves(vec_grid)

    # Need to check combinations of the remaining moves
    for N in range(0, 21):
        print(
            '\033[1;34m'
            + f'Checking for solutions with {len(init_moves) + N} moves...'
            + '\033[0m'
        )
        for moves in tqdm(combinations(remaining_moves, N)):
            vec_grid_copy = np.copy(vec_grid)
            moves = init_moves + list(moves)
            vec_update_grid(vec_grid_copy, moves)
           
            if np.array_equal(vec_grid_copy, vec_solved):
                moves = [int_to_pos(move) for move in moves]
                print(f'\nFound a solution with {len(moves)} moves:')
                pprint(moves, width=40, compact=True)
                return moves
            
        print(f'No solution found with {len(init_moves) + N} moves.')

    print('No solution found for this configuration.')
    return []


@timed
def brute_force_v3(grid):
    solutions = {}

    print('\n===== Solving via brute force (v3) =====')
    # First, check if the solution will involve toggling any of the 5 "special"
    # positions (6, 8, 12, 16, 18)
    vec_grid = list_to_vec(grid)
    init_moves = check_initial_moves(vec_grid)

    # Find the nature of the 10 couples
    bosons, fermions = find_coupling_parity(vec_grid, "couples")
    husbands = [husband for husband in couples]

    # Check combinations of the remaining moves
    for N in range(0, 11):
        for pressed_husbdands in combinations(husbands, N):
            pressed_wives = [couples[husband] for husband in fermions if husband not in pressed_husbdands]
            pressed_wives += [couples[husband] for husband in pressed_husbdands if husband in bosons]
            moves = init_moves + list(pressed_husbdands) + pressed_wives
            
            vec_grid_copy = np.copy(vec_grid)
            vec_update_grid(vec_grid_copy, moves)
            
            if np.array_equal(vec_grid_copy, vec_solved):
                moves = [int_to_pos(move) for move in moves]
                solutions[len(moves)] = moves

                print('-' * 40)
                print(f'Found a solution with {len(moves)} moves:')
                print('-' * 40)
                pprint(moves, width=40, compact=True)
                print('-' * 40 + '\n')
            
    if len(solutions) > 0:
        min_moves = min(solutions.keys())
        moves = solutions[min_moves]
        print(f'\033[1;32mBest solution has {min_moves} moves.\033[0m')
        return moves

    print('No solution found for this configuration.')
    return []


@timed
def disentangle(grid):
    solutions = {}

    print('\n===== Solving by disentangling =====')
    # First, check if the solution will involve toggling any of the 5 "special"
    # positions (6, 8, 12, 16, 18)
    vec_grid = list_to_vec(grid)
    init_moves = check_initial_moves(vec_grid)

    # Find the nature of the 2 cousin-pairs
    bosonic_cousins, fermionic_cousins = find_coupling_parity(vec_grid, "cousins")
    type_a_cousins = [0, 1, 2]
    n_seeds_to_choose = find_n_seeds_to_choose(vec_grid)

    # Find the nature of the 5 brother-pairs
    bosonic_bros, fermionic_bros = find_coupling_parity(vec_grid, "brothers")

    # Find the nature of the 10 married-pairs
    bosonic_couples, fermionic_couples = find_coupling_parity(vec_grid, "couples")

    # Otherwise, we need to check combinations of the remaining moves
    for N in n_seeds_to_choose:
        for pressed_a_cousins in combinations(type_a_cousins, N):
            print(f"Trying seed {pressed_a_cousins}...")

            pressed_b_cousins = [cousins[type_a] for type_a in fermionic_cousins if type_a not in pressed_a_cousins]
            pressed_b_cousins += [cousins[type_a] for type_a in pressed_a_cousins if type_a in bosonic_cousins]
            pressed_a_bros = list(pressed_a_cousins) + pressed_b_cousins
            
            pressed_b_bros = [brothers[type_a] for type_a in fermionic_bros if type_a not in pressed_a_bros]
            pressed_b_bros += [brothers[type_a] for type_a in pressed_a_bros if type_a in bosonic_bros]
            pressed_husbdands = pressed_a_bros + pressed_b_bros

            pressed_wives = [couples[husband] for husband in fermionic_couples if husband not in pressed_husbdands]
            pressed_wives += [couples[husband] for husband in pressed_husbdands if husband in bosonic_couples]
            moves = init_moves + pressed_husbdands + pressed_wives
            
            vec_grid_copy = np.copy(vec_grid)
            vec_update_grid(vec_grid_copy, moves)
            
            if np.array_equal(vec_grid_copy, vec_solved):
                moves = [int_to_pos(move) for move in moves]
                solutions[len(moves)] = moves

                print('-' * 40)
                print(f'Found a solution with {len(moves)} moves:')
                print('-' * 40)
                pprint(moves, width=40, compact=True)
                print('-' * 40 + '\n')
            
    if len(solutions) > 0:
        min_moves = min(solutions.keys())
        moves = solutions[min_moves]
        print(f'\033[1;32mBest solution has {min_moves} moves.\033[0m')
        return moves

    print('No solution found for this configuration.')
    return []


@timed
def brute_force_v2_all_solutions(grid):
    solutions = {}

    print('\n===== Solving via brute force (v2) =====')
    # First, check if the solution will involve toggling any of the 5 "special"
    # positions (6, 8, 12, 16, 18)
    vec_grid = list_to_vec(grid)
    init_moves = check_initial_moves(vec_grid)

    # Check combinations of the remaining moves
    for N in range(0, 21):
        print(
            '\033[1;34m'
            + f'Checking for solutions with {len(init_moves) + N} moves...'
            + '\033[0m'
        )
        for moves in tqdm(combinations(remaining_moves, N)):
            vec_grid_copy = np.copy(vec_grid)
            moves = init_moves + list(moves)
            vec_update_grid(vec_grid_copy, moves)

            if np.array_equal(vec_grid_copy, vec_solved):
                moves = [int_to_pos(move) for move in moves]
                print(f'\nFound a solution with {len(moves)} moves:')
                pprint(moves, width=40, compact=True)
                solutions[len(moves)] = moves
            
        print(f'No solution found with {len(init_moves) + N} moves.')

    if len(solutions) > 0:
        min_moves = min(solutions.keys())
        moves = solutions[min_moves]
        print(f'\033[1;32mBest solution has {min_moves} moves.\033[0m')
        return moves

    print('No solution found for this configuration.')
    return []

