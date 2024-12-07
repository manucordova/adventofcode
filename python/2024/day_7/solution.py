import os
import adventofcode as aoc


def evaluate_possible_operation(trg, cur_num, next_nums, concat=False):

    if len(next_nums) == 0:
        return trg == cur_num

    return (evaluate_possible_operation(trg, cur_num + next_nums[0], next_nums[1:], concat=concat) or
            evaluate_possible_operation(trg, cur_num * next_nums[0], next_nums[1:], concat=concat) or
            (concat and evaluate_possible_operation(trg, int(str(cur_num) + str(next_nums[0])), next_nums[1:], concat=concat)))


def parse_input():

    with open(os.path.join(os.path.dirname(__file__), "input.txt"), "r") as file:
        txt = file.read().strip()

    ops = []

    for line in txt.split("\n"):
        trg, nums = line.split(":")

        ops.append((int(trg), list(map(int, nums.split()))))

    return ops


def solve_level_1():
    """
    Solve level 1
    """

    # Read input file
    ops = parse_input()

    tot = 0
    for trg, nums in ops:
        if evaluate_possible_operation(trg, nums[0], nums[1:]):
            tot += trg

    return tot


def solve_level_2():
    """
    Solve level 2
    """

    # Read input file
    ops = parse_input()

    tot = 0
    for trg, nums in ops:
        if evaluate_possible_operation(trg, nums[0], nums[1:], concat=True):
            tot += trg

    return tot


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
                print(solve_level_1())
            elif level == 2:
                print(solve_level_2())

        else:
            if level == 1:
                # Submit the solution
                verdict, success = con.submit_answer(1, solve_level_1())
                if success:
                    con.reload_instructions(pl.Path(__file__).parent.resolve())
            elif level == 2:
                verdict, success = con.submit_answer(2, solve_level_2())

            print(verdict)
