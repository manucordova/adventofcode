import os
import time
import adventofcode as aoc


class Maze:
    def __init__(self, path, start_pos, end_pos, start_orientation="E"):
        self._nodes = []
        self._neighbours = {}
        self._start_node = (start_pos[0], start_pos[1], start_orientation)
        self._end_nodes = [(end_pos[0], end_pos[1], orientation) for orientation in self.get_orientations()]

        self._nx = len(path[0])
        self._ny = len(path)

        self._build_maze(path)

    @staticmethod
    def get_orientations():
        return "NESW"

    @staticmethod
    def rotate(orientation, clockwise=True):
        if clockwise:
            return "ESWN"["NESW".index(orientation)]
        return "WNES"["NESW".index(orientation)]

    def _add_node(self, i, j, path):

        for o in self.get_orientations():
            self._nodes.append((i, j, o))
            self._neighbours[(i, j, o)] = set()
            self._neighbours[(i, j, o)].add(((i, j, self.rotate(o)), 1000))
            self._neighbours[(i, j, o)].add(((i, j, self.rotate(o, clockwise=False)), 1000))

        if path[i-1][j]:
            self._neighbours[(i, j, "W")].add(((i-1, j, "W"), 1))

        if path[i+1][j]:
            self._neighbours[(i, j, "E")].add(((i+1, j, "E"), 1))

        if path[i][j-1]:
            self._neighbours[(i, j, "N")].add(((i, j-1, "N"), 1))

        if path[i][j+1]:
            self._neighbours[(i, j, "S")].add(((i, j+1, "S"), 1))

    def _build_maze(self, path):

        for i, line in enumerate(path):
            for j, valid in enumerate(line):
                if valid:
                    self._add_node(i, j, path)

    def __repr__(self):
        output = ""
        for j in range(self._ny):
            for i in range(self._nx):
                output += "." if (i, j, "E") in self._nodes else "#"

            output += "\n"
        return output

    def shortest_path(self):

        costs = {self._start_node: 0}

        todo = set()
        todo.add(self._start_node)
        visited = []

        while todo:
            node = min(todo, key=lambda x: costs[x])

            todo.remove(node)

            if node in self._end_nodes:
                return costs[node]

            for nei, move_cost in self._neighbours[node]:
                if nei not in visited:
                    if nei not in costs or costs[node] + move_cost < costs[nei]:
                        costs[nei] = costs[node] + move_cost
                        todo.add(nei)

        return -1

    def best_tiles(self):

        costs = {self._start_node: 0}

        todo = set()
        todo.add(self._start_node)
        visited = []

        parents = {self._start_node: None}
        end_cost = None

        while todo:
            node = min(todo, key=lambda x: costs[x])

            todo.remove(node)

            if end_cost is not None and costs[node] > end_cost:
                continue

            if node in self._end_nodes:
                end_cost = costs[node]

            for nei, move_cost in self._neighbours[node]:
                if nei not in visited:

                    # Neighbour already visited: a second path leads to that node
                    if nei in costs and costs[node] + move_cost == costs[nei]:
                        parents[nei].append(node)

                    if nei not in costs or costs[node] + move_cost < costs[nei]:
                        costs[nei] = costs[node] + move_cost
                        parents[nei] = [node]
                        todo.add(nei)

        best_tiles = set()

        todo = [n for n in self._end_nodes if n in parents]
        while len(todo) > 0:
            n = todo.pop(0)
            best_tiles.add((n[0], n[1]))
            node_parents = parents[n]
            if n != self._start_node:
                todo.extend([n2 for n2 in node_parents])

        return len(best_tiles)


def parse_input():

    with open(os.path.join(os.path.dirname(__file__), "input.txt"), "r") as file:
        lines = file.read().strip().split("\n")

    path = []
    for j, line in enumerate(lines):
        path.append([False if c == "#" else True for c in line])

        if "S" in line:
            start_pos = (line.index("S"), j)
        if "E" in line:
            end_pos = (line.index("E"), j)

    path = list(map(list, zip(*path)))

    maze = Maze(path, start_pos, end_pos)

    return maze


def solve_level_1():
    """
    Solve level 1
    """

    # Read input file
    maze = parse_input()

    return maze.shortest_path()


def solve_level_2():
    """
    Solve level 2
    """

    # Read input file
    maze = parse_input()

    return maze.best_tiles()


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
