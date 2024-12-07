import pathlib as pl
import adventofcode as aoc
import copy
import tqdm

guard_chars = {(1, 0): "v", (-1, 0): "^", (0, 1): ">", (0, -1): "<"}


class GuardPath:

    def __init__(self, txt):

        self.grid = []
        self._init_grid = []
        for i, line in enumerate(txt.split("\n")):
            if "^" in line:
                self._init_guard_pos = (i, line.index("^"))
                self.guard_pos = (i, line.index("^"))
                self._init_guard_dir = (-1, 0)
                self.guard_dir = (-1, 0)

            self._init_grid.append([c for c in line.replace("^", ".")])
            self.grid.append([c for c in line.replace("^", ".")])
        

        self.boundaries = (len(self.grid), len(self.grid[0]))
        self.path = {}
    
    def move(self):

        trg_pos = list(self.guard_pos)
        while self.grid[trg_pos[0]][trg_pos[1]] != "#":

            self.grid[trg_pos[0]][trg_pos[1]] = "X"
            self.guard_pos = tuple(trg_pos)
        
            if self.guard_pos not in self.path:
                self.path[self.guard_pos] = []

            if self.guard_dir in self.path[self.guard_pos]:
                return True
            self.path[self.guard_pos].append(self.guard_dir)

            trg_pos[0] += self.guard_dir[0]
            trg_pos[1] += self.guard_dir[1]

            if any([p < 0 or p >= b for p, b in zip(trg_pos, self.boundaries)]):
                self.guard_pos = tuple(trg_pos)
                break
        
        return False
    
    def rotate(self):
        """
        -1,  0 -->  0,  1
         1,  0 -->  0, -1
         0,  1 -->  1,  0
         0, -1 --> -1,  0
         """
        guard_rotation = {(1, 0): (0, -1), (-1, 0): (0, 1), (0, 1): (1, 0), (0, -1): (-1, 0)}
        self.guard_dir = guard_rotation[self.guard_dir]

    def compute_path(self):
        while all([p >= 0 and p < b for p, b in zip(self.guard_pos, self.boundaries)]):
            loop = self.move()
            if loop:
                break
            self.rotate()

    def count_path(self):
        return sum([line.count("X") for line in self.grid])
    
    def get_path(self):
        return self.path
    
    def reset_grid(self):
        self.grid = copy.deepcopy(self._init_grid)
        self.guard_pos = self._init_guard_pos
        self.guard_dir = self._init_guard_dir
        self.path = {}
    
    def print_grid(self):

        print()
        for i, line in enumerate(self.grid):

            if self.guard_pos[0] == i:
                txt_line = "".join(line[:self.guard_pos[1]]) + guard_chars[self.guard_dir] + "".join(line[self.guard_pos[1]+1:])
            else:
                txt_line = "".join(line)
            print(txt_line)
        print()
    
    def add_obstacle(self, pos):
        self.grid[pos[0]][pos[1]] = "#"
    
    def check_loop(self):
        while all([p >= 0 and p < b for p, b in zip(self.guard_pos, self.boundaries)]):
            loop = self.move()
            if loop:
                return True
            self.rotate()
        return False


def solve_level_1():
    """
    Solve level 1
    """

    # Read input file
    with open(pl.Path(pl.Path(__file__).parent.resolve(), "input.txt"), "r") as file:
        input_txt = file.read().strip()

    guard = GuardPath(input_txt)

    guard.compute_path()

    return guard.count_path()


def solve_level_2():
    """
    Solve level 2
    """

    # Read input file
    with open(pl.Path(pl.Path(__file__).parent.resolve(), "input.txt"), "r") as file:
        input_txt = file.read().strip()

    guard = GuardPath(input_txt)

    guard.compute_path()

    path = guard.get_path()

    tot = 0
    for p in tqdm.tqdm(path):

        if not all([pi == gi for pi, gi in zip(p, guard._init_guard_pos)]):
            guard.reset_grid()
            guard.add_obstacle(p)

            loop = guard.check_loop()

            if loop:
                tot += 1

    return tot


if __name__ == "__main__":

    debug = False

    year, day = aoc.get_year_day_from_path(__file__)
    con = aoc.AOCConnector(year, day)

    # Get current level
    level = con.get_level()

    if debug:
        # Just print the solution
        if level == 1:
            print(solve_level_1())
        elif level == 2:
            print(solve_level_2())

    else:
        if level == 1:
            # Submit the solution
            verdict, success = con.submit_answer(1, solve_level_1())
            if success:
                con.reload_instructions(pl.Path(__file__).parent.resolve())
        elif level == 2:
            verdict, success = con.submit_answer(2, solve_level_2())

        print(verdict)
