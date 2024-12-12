import os
import time
import adventofcode as aoc


def parse_input():

    with open(os.path.join(os.path.dirname(__file__), "input.txt"), "r") as file:
        txt = file.read().strip()

    stones = {}

    for item in map(int, txt.split()):
        if item not in stones:
            stones[item] = 0
        stones[item] += 1

    return stones


def blink(stones):

    next_stones = {}

    for s in stones:

        s_str = str(s)
        len_s = len(s_str)

        if s == 0:
            next_s = [1]
        elif len_s % 2 == 0:
            next_s = [int(s_str[:len_s//2]), int(s_str[len_s//2:])]
        else:
            next_s = [s * 2024]

        for s2 in next_s:
            if s2 not in next_stones:
                next_stones[s2] = 0
            next_stones[s2] += stones[s]

    return next_stones


def solve_level_1():
    """
    Solve level 1
    """

    # Read input file
    stones = parse_input()

    for _ in range(25):
        stones = blink(stones)

    return sum([x for x in stones.values()])


def solve_level_2():
    """
    Solve level 2
    """

    # Read input file
    stones = parse_input()

    for _ in range(75):
        stones = blink(stones)

    return sum([x for x in stones.values()])


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
