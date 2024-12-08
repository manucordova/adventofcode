import os
import time
import adventofcode as aoc


def gcd(a, b):
    while b > 0:
        a, b = b, a%b
    return a


def parse_input():

    with open(os.path.join(os.path.dirname(__file__), "input.txt"), "r") as file:
        txt = file.read().strip()

    grid = [[c for c in line] for line in txt.split("\n")]

    return grid


def get_antennas_pos(grid):

    antennas = {}

    for i, line in enumerate(grid):
        for j, c in enumerate(line):
            if c != ".":

                if c not in antennas:
                    antennas[c] = []
                antennas[c].append((i, j))

    return antennas


def get_antinodes(antennas, ni, nj):

    antinodes = set()

    for a in antennas:
        
        for k, p1 in enumerate(antennas[a]):
            for p2 in antennas[a][k+1:]:

                diff = (p2[0] - p1[0], p2[1] - p1[1])
                an1 = (p2[0] + diff[0], p2[1] + diff[1])
                an2 = (p1[0] - diff[0], p1[1] - diff[1])

                if an1[0] >= 0 and an1[0] < ni and an1[1] >= 0 and an1[1] < nj:
                    antinodes.add(an1)

                if an2[0] >= 0 and an2[0] < ni and an2[1] >= 0 and an2[1] < nj:
                    antinodes.add(an2)

    return antinodes


def get_antinodes_dense(antennas, ni, nj):

    antinodes = set()

    for a in antennas:
        
        for k, p1 in enumerate(antennas[a]):
            for p2 in antennas[a][k+1:]:

                d1 = p2[0] - p1[0]
                d2 = p2[1] - p1[1]

                dd = gcd(abs(d1), abs(d2))

                diff = (d1 // dd, d2 // dd)

                p = p1
                n = 0
                while p[0] >= 0 and p[0] < ni and p[1] >= 0 and p[1] < nj:
                    antinodes.add(p)
                    n += 1
                    p = (p1[0] + n * diff[0], p1[1] + n * diff[1])
                
                p = p1
                n = 0
                while p[0] >= 0 and p[0] < ni and p[1] >= 0 and p[1] < nj:
                    antinodes.add(p)
                    n += 1
                    p = (p1[0] - n * diff[0], p1[1] - n * diff[1])

    return antinodes


def solve_level_1():
    """
    Solve level 1
    """

    # Read input file
    grid = parse_input()

    antennas = get_antennas_pos(grid)

    return len(get_antinodes(antennas, len(grid), len(grid[0])))


def solve_level_2():
    """
    Solve level 2
    """

    # Read input file
    grid = parse_input()

    antennas = get_antennas_pos(grid)

    return len(get_antinodes_dense(antennas, len(grid), len(grid[0])))


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
