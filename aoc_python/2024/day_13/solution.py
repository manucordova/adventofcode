import os
import time
import adventofcode as aoc


def invert_matrix(a):

    norm = 1.0 / ((a[0][0] * a[1][1]) - (a[0][1] * a[1][0]))

    a_inv = [[a[1][1] * norm, -a[0][1] * norm], [-a[1][0] * norm, a[0][0] * norm]]

    return a_inv


def mult(a, b):
    
    return [a[0][0] * b[0] + a[0][1] * b[1], a[1][0] * b[0] + a[1][1] * b[1]]


def nearest_int(x, max_diff=0.1):

    x0 = int(x)

    if x - x0 < max_diff:
        return x0
    if x - x0 > 1 - max_diff:
        return x0 + 1

    return -1


def parse_input(add=0):

    with open(os.path.join(os.path.dirname(__file__), "input.txt"), "r") as file:
        txt = file.read().strip()
    
    i = 0
    lines = txt.split("\n")

    machines = []

    while i+2 < len(lines):

        xa = int(lines[i].split("X+")[1].split(",")[0])
        ya = int(lines[i].split("Y+")[1])
        xb = int(lines[i+1].split("X+")[1].split(",")[0])
        yb = int(lines[i+1].split("Y+")[1])

        a = [[xa, xb], [ya, yb]]

        px = float(lines[i+2].split("X=")[1].split(",")[0])
        py = float(lines[i+2].split("Y=")[1])
        b = [px + add, py + add]

        machines.append((a, b))

        i += 4
    
    return machines


def solve_level_1():
    """
    Solve level 1
    """

    # Read input file
    machines = parse_input()

    tokens = 0

    for a, b in machines:

        a_inv = invert_matrix(a)

        n = mult(a_inv, b)

        na = nearest_int(n[0], max_diff=1e-3)
        nb = nearest_int(n[1], max_diff=1e-3)

        if na >= 0 and nb >= 0:
            tokens += 3 * na + nb

    return tokens


def solve_level_2():
    """
    Solve level 2
    """

    # Read input file
    machines = parse_input(add=10000000000000)

    tokens = 0

    for a, b in machines:

        a_inv = invert_matrix(a)

        n = mult(a_inv, b)

        na = nearest_int(n[0], max_diff=1e-3)
        nb = nearest_int(n[1], max_diff=1e-3)

        if na >= 0 and nb >= 0:
            tokens += 3 * na + nb

    return tokens


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
