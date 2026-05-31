import argparse
import tkinter as tk
from solver import vec_brute_force, chase_the_lights
from utils import generate_random_grid, update_grid, colours, solved


class Game:
    def __init__(self, solve_mode, solver_algorithm):
        # Initialise the game state
        self.solve_mode = solve_mode
        if self.solve_mode:
            self.solver_algorithm = solver_algorithm
            self.grid = [row[:] for row in solved]
            self.setup = True
        else:
            self.solution, self.grid = generate_random_grid()
            self.setup = False
        self.grid_copy = [row[:] for row in self.grid]

        # Initialise the GUI
        self.count = 0       
        self.streak = 0 
        self.root = tk.Tk()
        self.root.title('Lights Out')
        self.root.config(bg='black')
        self.buttons = self.make_buttons()
        self.count_label, self.streak_label = self.make_labels()

        # Start the GUI event loop
        self.root.mainloop()       

    def make_labels(self):
        # Create labels for move count and current streak
        count_label = tk.Label(
            self.root,
            text=f'Moves: 0',
            fg='white',
            bg='black'
        )
        count_label.grid(row=5, column=0, columnspan=5, pady=10)

        streak_label = tk.Label(
            self.root,
            text=f'Current Streak: 0',
            fg='white',
            bg='black'
        )
        streak_label.grid(row=6, column=0, columnspan=5, pady=10)

        return count_label, streak_label

    def make_buttons(self):
        # Create a 5x5 grid of buttons based on the current grid state
        buttons = []
        
        for i in range(5):
            row = []
            for j in range(5):
                button = tk.Button(
                    self.root,
                    bg=colours[self.grid[i][j]],
                    width=10,
                    height=5,
                    activebackground=colours[self.grid[i][j]],
                    command=lambda i=i, j=j: self.toggle_button(i, j)
                )
                button.grid(row=i, column=j, padx=5, pady=5)
                row.append(button)
            buttons.append(row)

        reset_button = tk.Button(
            self.root,
            text='Reset',
            bg='green',
            fg='white',
            command=self.reset_game
        )
        reset_button.grid(row=7, column=0, columnspan=5, pady=10)

        stuck_button = tk.Button(
            self.root,
            text='I`m stuck',
            bg='red',
            fg='white',
            command=self.show_solution
        )
        stuck_button.grid(row=8, column=0, columnspan=5, pady=10)

        return buttons
    
    def update_button_colours(self):
        # Update the button colours based on the new grid state
        for x in range(5):
            for y in range(5):
                self.buttons[x][y].config(
                    bg=colours[self.grid[x][y]],
                    activebackground=colours[self.grid[x][y]]
                )

    def clear_button_texts(self):
        # Clear the button labels
        for x in range(5):
            for y in range(5):
                self.buttons[x][y].config(text='')

    def toggle_button(self, i, j):
        # Toggle the button at (i, j) and update the grid and button states
        if not self.setup:
            self.count += 1
        update_grid(self.grid, i, j, self.setup)
        self.update_button_colours()
        self.count_label.config(text=f'Moves: {self.count}')
        if not self.setup and (self.grid == solved):
            self.root.after(200, self.go_green)
            self.root.after(1000, self.new_game)

    def reset_game(self):
        # Reset the game to the initial state
        self.grid = [row[:] for row in self.grid_copy]
        self.update_button_colours()
        self.count = 0
        self.count_label.config(text=f'Moves: {self.count}')

    def show_solution(self):
        # Get the solution from the solver and display it on the buttons
        self.setup = False
        if self.solve_mode:
            if self.grid == solved:
                print('The grid is already solved.')
                self.setup = True
                return
            
            self.grid_copy = [row[:] for row in self.grid]
            self.solution = self.solver_algorithm(self.grid)
            
            if self.solution == []:
                self.grid_copy = [row[:] for row in solved]
                self.setup = True

        for move in self.solution:
            self.buttons[move[0]][move[1]].config(text='Press')

    def new_game(self):
        if not self.solve_mode:
            self.solution, self.grid = generate_random_grid()
            self.setup = False
        else:
            self.grid = [row[:] for row in solved]
            self.setup = True
        self.grid_copy = [row[:] for row in self.grid]
        
        self.update_button_colours()
        self.clear_button_texts()
        self.count = 0
        self.count_label.config(text=f'Moves: {self.count}')
        self.streak += 1
        self.streak_label.config(text=f'Current Streak: {self.streak}')

    def go_green(self):
        # Make the buttons green when the game is solved
        for x in range(5):
            for y in range(5):
                self.buttons[x][y].config(bg='green', activebackground='green')


def main(args):
    solver_algorithm = None
    
    if args.solve:
        print('Starting the game in solve mode...')
        while True:
            choice = input(
"""\
----------------------------------------
Choose a solver algorithm
----------------------------------------
1. \033[1;95mBrute Force\033[0m
2. \033[1;95mChase the Lights\033[0m
Enter the number of your choice: \
"""
            )
            if choice == '1':
                solver_algorithm = vec_brute_force
                print('Loading Brute Force solver...')
                break
            elif choice == '2':
                solver_algorithm = chase_the_lights
                print('Loading Chase the Lights solver...')
                break
            else:
                print('Invalid choice. Please try again.')

    game = Game(solve_mode=args.solve, solver_algorithm=solver_algorithm)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Lights Out Game')
    parser.add_argument(
        '--solve',
        action='store_true',
        help='Solve the grid configuration',
    )
    args = parser.parse_args()
    main(args)

