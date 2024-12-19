import os
import time
import adventofcode as aoc

POSSIBLE_MEM = {}
WAYS_MEM = {}


def parse_input():

    with open(os.path.join(os.path.dirname(__file__), "input.txt"), "r") as file:
        txt = file.read().strip()

    lines = txt.split("\n")
    
    elems = lines[0].split(", ")
    target_list = [line for line in lines[2:]]
    
    return elems, target_list


def is_possible(target, elems):

    if target in POSSIBLE_MEM:
        return POSSIBLE_MEM[target]

    if len(target) == 0:
        return True

    for elem in elems:
        if target.startswith(elem) and is_possible(target[len(elem):], elems):
            POSSIBLE_MEM[target] = True
            return True
    
    POSSIBLE_MEM[target] = False
    return False

def num_ways(target, elems):

    if target in WAYS_MEM:
        return WAYS_MEM[target]
    
    if len(target) == 0:
        return 1

    n = 0

    for elem in elems:
        if target.startswith(elem):
            n += num_ways(target[len(elem):], elems)

    WAYS_MEM[target] = n
    
    return n

def solve_level_1():
    """
    Solve level 1
    """

    # Read input file
    elems, target_list = parse_input()

    return len([0 for target in target_list if is_possible(target, elems)])


def solve_level_2():
    """
    Solve level 2
    """

    # Read input file
    elems, target_list = parse_input()

    return sum([num_ways(target, elems) for target in target_list])


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
