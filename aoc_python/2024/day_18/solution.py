import os
import time
import adventofcode as aoc


class Grid:
    def __init__(self, byte_list, w, h):
        self._byte_list = byte_list
        self._w = w
        self._h = h
        self._last_byte = None
        self._path = None

        self._grid = [[0 for _ in range(self._h)] for _ in range(self._w)]

    def __repr__(self):
        output = ""
        for j in range(self._h):
            for i in range(self._w):
                output += "." if self._grid[i][j] == 0 else "#"

            output += "\n"
        return output

    def fall_bytes(self, num_bytes=-1):

        if num_bytes < 0:
            num_bytes = len(self._byte_list)

        while num_bytes > 0 and len(self._byte_list) > 0:
            i, j = self._byte_list.pop(0)
            self._last_byte = (i, j)
            self._grid[i][j] += 1
            num_bytes -= 1

    def get_neighbours(self, i, j):

        dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        neighbours = []
        for di, dj in dirs:
            i2 = i + di
            j2 = j + dj
            if i2 >= 0 and j2 >= 0 and i2 < self._w and j2 < self._h and self._grid[i2][j2] == 0:
                neighbours.append((i2, j2))
        return neighbours

    def shortest_path(self):

        start_node = (0, 0)
        end_node = (self._w - 1, self._h - 1)

        visited = set()
        lengths = {start_node: 0}
        todo = [start_node]
        parents = {start_node: None}

        while len(todo) > 0:
            coords = todo.pop(0)
            visited.add(coords)
            for nei in self.get_neighbours(*coords):
                length = lengths[coords] + 1
                if nei not in visited or length < lengths[nei]:
                    lengths[nei] = length
                    parents[nei] = coords
                    if nei not in todo:
                        todo.append(nei)

                if nei == end_node:
                    n = nei
                    self._path = [n]
                    while parents[n] is not None:
                        n = parents[n]
                        self._path.append(n)
                    return lengths[nei]

        return -1

    def get_last_byte(self):
        return self._last_byte

    def get_path(self):
        return self._path


def parse_input():

    with open(os.path.join(os.path.dirname(__file__), "input.txt"), "r") as file:
        txt = file.read().strip()

    byte_list = [list(map(int, line.split(","))) for line in txt.split("\n")]

    return byte_list


def solve_level_1():
    """
    Solve level 1
    """

    # Read input file
    byte_list = parse_input()

    size = 71
    n_fall = 1024
    grid = Grid(byte_list, size, size)

    grid.fall_bytes(n_fall)

    return grid.shortest_path()


def solve_level_2():
    """
    Solve level 2
    """

    # Read input file
    byte_list = parse_input()

    size = 71
    n_fall = 1024
    grid = Grid(byte_list, size, size)

    grid.fall_bytes(n_fall)

    while grid.shortest_path() >= 0:

        while grid.get_last_byte() not in grid.get_path():
            grid.fall_bytes(1)

    return grid.get_last_byte()


if __name__ == "__main__":

    debug = True

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
