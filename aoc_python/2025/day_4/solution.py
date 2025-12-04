import os
import time
import adventofcode as aoc


def parse_input():

    with open(os.path.join(os.path.dirname(__file__), "input.txt"), "r") as file:
        txt = file.read().strip()

    grid = [[1 if c == "@" else 0 for c in row] for row in txt.split("\n")]

    return grid


def is_accessible(grid, i, j):

    num_adjacent = 0

    for di in [-1, 0, 1]:
        for dj in [-1, 0, 1]:
            if (i + di >= 0 and i + di < len(grid)
                and j + dj >= 0 and j + dj < len(grid[0])
                and not (di == 0 and dj == 0)):
                num_adjacent += grid[i+di][j+dj]

    return num_adjacent < 4


def count_accessible(grid, update_grid=False):

    accessible = 0

    for i in range(len(grid)):
        for j in range(len(grid[0])):

            if grid[i][j] == 1 and is_accessible(grid, i, j):
                accessible += 1
                if update_grid:
                    grid[i][j] = 0

    return accessible


def solve_level_1():
    """
    Solve level 1
    """

    # Read input file
    grid = parse_input()

    return count_accessible(grid)


def solve_level_2():
    """
    Solve level 2
    """

    # Read input file
    grid = parse_input()

    removed = 0

    accessible = count_accessible(grid, update_grid=True)
    while accessible > 0:
        removed += accessible
        accessible = count_accessible(grid, update_grid=True)

    return removed


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
