import os
import time
import adventofcode as aoc


def parse_input():

    with open(os.path.join(os.path.dirname(__file__), "input.txt"), "r") as file:
        txt = file.read().strip()

    banks = []
    for line in txt.split("\n"):
        banks.append([int(c) for c in line])

    return banks


def get_max_jolt(bank: list, i0=0, num=2):

    if num == 1:
        return max(bank[i0:])

    # Find the largest number that still leaves room for the next numbers
    for n in range(9, -1, -1):
        if n in bank[i0:]:
            idx = bank[i0:].index(n) + i0
            if len(bank) - idx >= num:
                return n * 10 ** (num - 1) + get_max_jolt(bank, i0=idx+1, num=num-1)

    return -1


def solve_level_1():
    """
    Solve level 1
    """

    # Read input file
    banks = parse_input()

    return sum([get_max_jolt(bank) for bank in banks])


def solve_level_2():
    """
    Solve level 2
    """

    # Read input file
    banks = parse_input()

    return sum([get_max_jolt(bank, num=12) for bank in banks])


if __name__ == "__main__":

    debug = True

    year, day = aoc.get_year_day_from_path(__file__)
    con = aoc.AOCConnector(year, day)

    # Get current level
    level = con.get_level()
    level = 2
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
