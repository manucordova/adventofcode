import os
import time
import adventofcode as aoc


class Node:
    def __init__(self, h):
        self._h = h
        self._score = 0
    
    @property
    def height(self):
        return self._h

    @height.setter
    def height(self, h):
        self._h = h
    
    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, s):
        self._score = s

    def __repr__(self):
        output = f"Node with height {self._h}. Current score: {self._score}"
        return output


class TrailMap:
    def __init__(self, grid):
        self._nodes = {}
        self._edges_desc = {}
        self._edges_asc = {}

        directions = [(-1, 0), (1, 0), (0, 1), (0, -1)]

        ni = len(grid)
        nj = len(grid[0])
        for i in range(ni):
            for j in range(nj):
                self._nodes[(i, j)] = Node(grid[i][j])

                self._edges_desc[(i, j)] = []
                self._edges_asc[(i, j)] = []
                for di, dj in directions:
                    if i + di >= 0 and i + di < ni and j + dj >= 0 and j + dj < nj:
                        if grid[i+di][j+dj] == grid[i][j] - 1:
                            self._edges_desc[(i, j)].append((i + di, j+dj))
                        elif grid[i+di][j+dj] == grid[i][j] + 1:
                            self._edges_asc[(i, j)].append((i + di, j+dj))
    
    def _init_scores(self, h):
        for n in self._nodes:
            self._nodes[n].score = 1 if self._nodes[n].height == h else 0

    def has_path(self, src, trg):
        if src == trg:
            return True

        elif self._nodes[src].height == self._nodes[trg].height:
            return False

        return any([self.has_path(n, trg) for n in self._edges_asc[src]])
    
    def get_trailhead_scores(self):

        src_list = [n for n in self._nodes if self._nodes[n].height == 0]
        trg_list = [n for n in self._nodes if self._nodes[n].height == 9]

        tot = 0
        for src in src_list:
            for trg in trg_list:
                if self.has_path(src, trg):
                    tot += 1
        
        return tot
    
    def propagate(self, src, trg):

        self._init_scores(src)

        h = src

        while h >= trg:

            nodes = [n for n in self._nodes if self._nodes[n].height == h]

            for n in nodes:
                for nei in self._edges_desc[n]:
                    self._nodes[nei].score += self._nodes[n].score
            
            h -= 1
    
        return sum([self._nodes[n].score for n in self._nodes if self._nodes[n].height == trg])

    def __repr__(self):
        output = ""
        for n in self._nodes:
            output += self._nodes[n].__repr__()

            output += f"\n    Node position: ({n[0]}, {n[1]})"

            output += "\n    Ascending neighbours: "
            output += ", ".join([f"({i}, {j})" for i, j in self._edges_asc[n]])
            output += "\n    Descending neighbours: "
            output += ", ".join([f"({i}, {j})" for i, j in self._edges_desc[n]])
            output += "\n"
        return output


def parse_input():

    with open(os.path.join(os.path.dirname(__file__), "input.txt"), "r") as file:
        txt = file.read().strip()

    grid = [[int(c) for c in line] for line in txt.split("\n")]

    trail_map = TrailMap(grid)

    return trail_map


def solve_level_1():
    """
    Solve level 1
    """

    # Read input file
    trail_map = parse_input()
    
    return trail_map.get_trailhead_scores()


def solve_level_2():
    """
    Solve level 2
    """

    # Read input file
    trail_map = parse_input()

    return trail_map.propagate(9, 0)


if __name__ == "__main__":

    debug = False

    year, day = aoc.get_year_day_from_path(__file__)
    con = aoc.AOCConnector(year, day)

    # Get current level
    level = con.get_level()
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
