"""
Lights Off Game (simple interactive version)
"""
import json
import argparse
import tkinter as tk

colours = ['gray', 'blue']


def load_grid():
    # Load the grid configuration from the JSON file
    try:
        with open('grid.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        # If the file doesn't exist, return a default grid
        return [[0 for _ in range(5)] for _ in range(5)]


def toggle(buttons, grid, i, j, setup=False):
    # Update the grid based on the button press
    if setup:
        grid[i][j] = 1 - grid[i][j]
    else:
        for x, y in [(i, j), (i-1, j), (i+1, j), (i, j-1), (i, j+1)]:
            if 0 <= x < 5 and 0 <= y < 5:
                grid[x][y] = 1 - grid[x][y]
    # Update the button colors based on the new grid state
    for x in range(5):
        for y in range(5):
            buttons[x][y].config(
                bg=colours[grid[x][y]],
                activebackground=colours[grid[x][y]]
            )


def main(args):
    # Load the grid configuration from the JSON file
    grid = load_grid()

    # Create the main application window
    root = tk.Tk()

    # Set window properties
    root.title('Lights Off')
    root.config(bg='black')

    # Create a 5x5 grid of buttons
    buttons = []
    for i in range(5):
        row = []
        for j in range(5):
            button = tk.Button(
                root,
                bg=colours[grid[i][j]],
                width=10,
                height=5,
                activebackground=colours[grid[i][j]],
                command=lambda i=i, j=j : toggle(
                    buttons,
                    grid,
                    i,
                    j,
                    args.setup
                )
            )
            button.grid(row=i, column=j, padx=5, pady=5)
            row.append(button)
        buttons.append(row)

    # Run window until it is closed by the user
    root.mainloop()

    if args.setup:
        # Save the updated grid configuration back to the JSON file
        with open('grid.json', 'w') as f:
            json.dump(grid, f)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Lights Off Game')
    parser.add_argument('--setup', action='store_true', help='Set up the grid configuration')
    args = parser.parse_args()
    main(args)

