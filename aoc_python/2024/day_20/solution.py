import os
import time
import adventofcode as aoc
from copy import deepcopy


class Race:

    def __init__(self, lines):
        
        grid = []

        for i, line in enumerate(lines):

            grid.append([False if c == "#" else True for c in line])

            if "S" in line:
                self._start_pos = (line.index("S"), i)
            
            if "E" in line:
                self._end_pos = (line.index("E"), i)
    
        self._init_grid = list(map(list, zip(*grid)))
        self._grid = deepcopy(self._init_grid)

        self._ni = len(self._grid)
        self._nj = len(self._grid[0])
    
    def __repr__(self):

        output = ""

        for j in range(self._nj):
            for i in range(self._ni):

                if self._start_pos == (i, j):
                    output += "S"
                elif self._end_pos == (i, j):
                    output += "E"
                else:
                    output += "." if self._grid[i][j] else "#"
            
            output += "\n"

        return output
    
    def reset(self):
        self._grid = deepcopy(self._init_grid)

    def _get_neighbours(self, i, j):
        nei = []

        dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for di, dj in dirs:
            i2 = i + di
            j2 = j + dj

            if i2 >= 0 and j2 >= 0 and i2 < self._ni and j2 < self._nj and self._grid[i2][j2]:
                nei.append((i2, j2))

        return nei
    
    def get_main_path(self):
        path = [self._start_pos]
        pos = self._start_pos
        while pos != self._end_pos:
            for nei in self._get_neighbours(*pos):
                if nei not in path:
                    path.append(nei)
                    pos = nei
                    break
        
        return path
    
    def get_cheat_positions(self):
        cheat_pos = []
        for i in range(self._ni):
            for j in range(self._nj):
                if not self._grid[i][j] and len(self._get_neighbours(i, j)) >= 2:
                    cheat_pos.append((i, j))
        return cheat_pos


def parse_input():

    with open(os.path.join(os.path.dirname(__file__), "input.txt"), "r") as file:
        lines = file.read().strip().split("\n")

    return Race(lines)


def solve_level_1():
    """
    Solve level 1
    """

    # Read input file
    race = parse_input()

    path = race.get_main_path()

    cheat_pos = race.get_cheat_positions()

    thresh = 100
    num = 0

    for pos in cheat_pos:
        cheat_nei = race._get_neighbours(*pos)
        ps = [path.index(p) for p in cheat_nei]
        time_saved = max(ps) - min(ps) - 2

        if time_saved >= thresh:
            num += 1

    return num


def solve_level_2():
    """
    Solve level 2
    """

    # Read input file
    race = parse_input()

    path = race.get_main_path()
    max_cheat_len = 20

    cheats = {}

    for t0, p1 in enumerate(path):
        for dt, p2 in enumerate(path[t0+1:]):

            dp = tuple(x2 - x1 for x1, x2 in zip(p1, p2))
            t = abs(dp[0]) + abs(dp[1])

            time_saved = dt - t + 1

            if t <= max_cheat_len and time_saved > 0:

                if time_saved not in cheats:
                    cheats[time_saved]  = 0
                
                cheats[time_saved] += 1

    return sum([cheats[k] for k in cheats if k >= 100])


if __name__ == "__main__":

    debug = True

    year, day = aoc.get_year_day_from_path(__file__)
    con = aoc.AOCConnector(year, day)

    # Get current level
    level = con.get_level()
    level = 2
    if level < 1:
        raise aoc.WrongLevelError()
    if level > 2:
        print("This challenge was already solved!")

    else:
        if debug:
            # Just print the solution
            if level == 1:
                start = time.time()
                print(solve_level_1())
                stop = time.time()
            elif level == 2:
                start = time.time()
                print(solve_level_2())
                stop = time.time()
            
            print(f"Level {level} run in {stop - start:.4e} s")

        else:
            if level == 1:
                # Submit the solution
                verdict, success = con.submit_answer(1, solve_level_1())
                if success:
                    con.reload_instructions(os.path.dirname(__file__))
            elif level == 2:
                verdict, success = con.submit_answer(2, solve_level_2())

            print(verdict)
