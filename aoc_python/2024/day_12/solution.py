import os
import time
import adventofcode as aoc


class Field:
    def __init__(self, txt):

        self.grid = [[c for c in line] for line in txt.split("\n")]
        self.ni = len(self.grid)
        self.nj = len(self.grid[0])
        self.num_edges = [[0 for _ in g] for g in self.grid]
        self.num_corners = [[0 for _ in g] for g in self.grid]
        self.regions = []

    def __repr__(self):
        output = "\n".join(["".join([c for c in g]) for g in self.grid])

        output += "\n\n"
        output += "\n".join(["".join([str(n) for n in g]) for g in self.num_edges])
        return "\n" + output + "\n"
    
    def _get_edge(self, i, j):

        num = 0

        if i-1 < 0 or self.grid[i-1][j] != self.grid[i][j]:
            num += 1
        if i+1 >= self.ni or self.grid[i+1][j] != self.grid[i][j]:
            num += 1
        if j-1 < 0 or self.grid[i][j-1] != self.grid[i][j]:
            num += 1
        if j+1 >= self.nj or self.grid[i][j+1] != self.grid[i][j]:
            num += 1
        
        return num

    def get_edges(self):

        for i in range(self.ni):
            for j in range(self.nj):

                self.num_edges[i][j] = self._get_edge(i, j)
    
    def _get_region(self, i0, j0):

        todo = [(i0, j0)]
        region = [(i0, j0)]

        while len(todo) > 0:
            i, j = todo.pop()

            if i-1 >= 0 and self.grid[i-1][j] == self.grid[i][j]:
                if (i-1, j) not in region:
                    region.append((i-1, j))
                    todo.append((i-1, j))

            if i+1 < self.ni and self.grid[i+1][j] == self.grid[i][j]:
                if (i+1, j) not in region:
                    region.append((i+1, j))
                    todo.append((i+1, j))

            if j-1 >= 0 and self.grid[i][j-1] == self.grid[i][j]:
                if (i, j-1) not in region:
                    region.append((i, j-1))
                    todo.append((i, j-1))

            if j+1 < self.nj and self.grid[i][j+1] == self.grid[i][j]:
                if (i, j+1) not in region:
                    region.append((i, j+1))
                    todo.append((i, j+1))
    
        return region

    def get_regions(self):

        done = []

        for i in range(self.ni):
            for j in range(self.nj):

                if (i, j) not in done:
                    region = self._get_region(i, j)
                    self.regions.append(region)
                    done.extend(region)

    def get_region_scores(self, discount=False):

        tot = 0

        if discount:
            for region, side in zip(self.regions, self.sides):
                
                tot += side * len(region)

        else:
            for region in self.regions:
                
                tot += sum([self.num_edges[i][j] for i, j in region]) * len(region)

        return tot
    
    def count_corners(self, region, i, j):

        searches = [[(i, j), (i-1, j), (i, j-1), (i-1, j-1)],
                    [(i, j), (i-1, j), (i, j+1), (i-1, j+1)],
                    [(i, j), (i, j-1), (i+1, j), (i+1, j-1)],
                    [(i, j), (i+1, j), (i, j+1), (i+1, j+1)]
                    ]
        
        n = 0
        for search in searches:
            search_result = [1 if s in region else 0 for s in search]
            
            if (sum(search_result) == 1
                or (sum(search_result) == 2 and search_result[0] == 1 and search_result[-1] == 1)
                or (sum(search_result) == 3 and search_result[-1] == 0)):
                n += 1
        return n

    def get_region_sides(self, region):

        num = 0

        for i, j in region:

            num += self.count_corners(region, i, j)

        return num

    def get_sides(self):

        self.sides = []

        for region in self.regions:
            self.sides.append(self.get_region_sides(region))
    

def parse_input():

    with open(os.path.join(os.path.dirname(__file__), "input.txt"), "r") as file:
        txt = file.read().strip()

    return txt


def solve_level_1():
    """
    Solve level 1
    """

    # Read input file
    field = Field(parse_input())

    field.get_edges()

    field.get_regions()

    return field.get_region_scores()


def solve_level_2():
    """
    Solve level 2
    """
    # Read input file
    field = Field(parse_input())

    field.get_regions()

    field.get_sides()

    return field.get_region_scores(discount=True)


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
