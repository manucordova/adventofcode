import os
import time
import adventofcode as aoc


def get_lock(lines, i):
    j = i+1
    while j < len(lines) and len(lines[j]) > 0:
        j += 1

    lock = []
    for x in range(len(lines[i])):
        for k in range(j - i):
            if lines[i+k][x] == ".":
                lock.append(k-1)
                break

    return tuple(lock), j - i


def get_key(lines, i):
    j = i+1
    while j < len(lines) and len(lines[j]) > 0:
        j += 1

    key = []
    for x in range(len(lines[i])):
        for k in range(j - i):
            if lines[j-k-1][x] == ".":
                key.append(k-1)
                break

    return tuple(key), j - i


def parse_input():

    locks = []
    keys = []

    with open(os.path.join(os.path.dirname(__file__), "input.txt"), "r") as file:
        lines = file.read().strip().split("\n")
    
    i = 0
    while i < len(lines):
        if len(lines[i]) > 0:
            if lines[i][0] == "#":
                lock, di = get_lock(lines, i)
                locks.append(lock)
                i += di
            elif lines[i][0] == ".":
                key, di = get_key(lines, i)
                keys.append(key)
                i += di
        else:
            i += 1

    
    return locks, keys


def solve_level_1():
    """
    Solve level 1
    """

    # Read input file
    locks, keys = parse_input()

    tot = 0
    for lock in locks:
        for key in keys:
            fit = [l + k for l, k in zip(lock, key)]
            if max(fit) <= 5:
                tot += 1

    return tot


def solve_level_2():
    """
    Solve level 2
    """

    # Read input file
    input_txt = parse_input()

    print(input_txt)

    return 0


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
