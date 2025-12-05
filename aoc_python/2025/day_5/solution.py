import os
import time
import adventofcode as aoc


def parse_input():

    with open(os.path.join(os.path.dirname(__file__), "input.txt"), "r") as file:
        txt = file.read().strip()

    fresh_ranges = []
    available = []

    for line in txt.split("\n"):
        if "-" in line:
            fresh_ranges.append(tuple(map(int, line.split("-"))))
        elif line != "":
            available.append(int(line))

    return sorted(fresh_ranges, key=lambda x: x[0]), available


def solve_level_1():
    """
    Solve level 1
    """

    # Read input file
    fresh_ranges, available = parse_input()

    num_fresh = 0

    for item in available:
        for r0, r1 in fresh_ranges:
            if item >= r0 and item <= r1:
                num_fresh += 1
                break

    return num_fresh


def reduce_ranges(init_ranges):

    new_ranges = [init_ranges[0]]

    for r0, r1 in init_ranges:

        nr0, nr1 = new_ranges[-1]

        if r0 <= nr1:
            new_ranges[-1] = (min(r0, nr0), max(r1, nr1))
        else:
            new_ranges.append((r0, r1))

    return new_ranges


def solve_level_2():
    """
    Solve level 2
    """

    # Read input file
    fresh_ranges, _ = parse_input()

    fresh_ranges = reduce_ranges(fresh_ranges)

    return sum([r1 - r0 + 1 for r0, r1 in fresh_ranges])


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
