import os
import time
import adventofcode as aoc


def parse_input():

    with open(os.path.join(os.path.dirname(__file__), "input.txt"), "r") as file:
        txt = file.read().strip()

    return txt


def num_digits(n):

    n_digits = 0

    while n > 0:
        n //= 10
        n_digits += 1

    return n_digits


def split_parts(n, part_factor):
    parts = []
    while n > 0:
        parts.append(n - n // part_factor * part_factor)
        n //= part_factor
    return parts[::-1]


def join_parts(parts, part_factor):
    num = 0
    for i, part in enumerate(parts[::-1]):
        num += part * part_factor ** i
    return num


def repeat_part(part, part_factor, num_parts):
    return join_parts([part] * num_parts, part_factor)


def keep_first_part(parts):

    for part in parts[1:]:
        if part > parts[0]:
            return False
        if part < parts[0]:
            return True

    return True


def next_invalid(n, split_in=2):

    nd = num_digits(n)
    part_factor = 10 ** (nd // split_in)

    # Only numbers with even numbers of digits can be invalid
    if nd % split_in == 0:

        parts = split_parts(n, part_factor)

        if not keep_first_part(parts):

            parts[0] += 1
            if num_digits(parts[0]) != num_digits(parts[1]):
                return next_invalid(10**(nd+1), split_in=split_in)

        return repeat_part(parts[0], part_factor, split_in)

    return next_invalid(10**nd, split_in=split_in)


def get_invalid_in_range(r1, r2, half_split_only=True):

    tot = 0

    if half_split_only:
        num = next_invalid(r1)

        while num <= r2:
            tot += num
            num = next_invalid(num+1)

    else:
        max_split = max(2, num_digits(r1))
        nums = [next_invalid(r1, n) for n in range(2, max_split+1)]
        num = min(nums)

        while num <= r2:
            tot += num
            max_split = max(2, num_digits(num+1))
            nums = [next_invalid(num+1, n) for n in range(2, max_split+1)]
            num = min(nums)

    return tot


def get_invalid_sum(ranges, half_split_only=True):
    return sum([get_invalid_in_range(r1, r2, half_split_only=half_split_only) for r1, r2 in ranges])


def solve_level_1():
    """
    Solve level 1
    """

    # Read input file
    input_txt = parse_input()

    ranges = [tuple(map(int, r.split("-"))) for r in input_txt.split(",")]

    return get_invalid_sum(ranges)


def solve_level_2():
    """
    Solve level 2
    """

    # Read input file
    input_txt = parse_input()

    ranges = [tuple(map(int, r.split("-"))) for r in input_txt.split(",")]

    return get_invalid_sum(ranges, half_split_only=False)


def is_invalid(n):
    s = str(n)

    for i in range(1, len(s)):
        if s == s[:i] * (len(s) // i):
            return True

    return False


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
