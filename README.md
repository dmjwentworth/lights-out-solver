## lights-out-solver

___
### Setup
___
```
git clone https://github.com/dmjwentworth/lights-out-solver
cd lights-out-solver
python -m venv .venv
source .venv/bin/activate       # Windows: .venv/Scripts/activate
pip install -r requirements.txt
```

___
### Solve mode
___
1) Run `python play.py --solve`
2) Type 3 (and press `Enter`) to use a Brute Force algorithm which is guaranteed to find the solution with the shortest number of moves (if it exists) but may take about a second, or type 4 (and press `Enter`) to use an algorithm based on the "chase the lights" strategy which will always find a solution instantly (if one exists), but on some occasions it will not be the optimal one.
3) An empty board will show up, use this to construct the board you wish to solve.
4) Press "I`m stuck" to run the solving algorithm.

___
### Default mode
___
1) Run `python play.py`
2) A randomly generated board will pop up – try to solve it!
3) The "I`m stuck" button in this mode gives instructions relative to the state of the board when the button was pressed. The "Reset" button returns the board to this state.

