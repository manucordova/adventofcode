import os
import time
import adventofcode as aoc
import itertools as it
from functools import cache


numeric_pos = {"7": (0, 0), "8": (0, 1), "9": (0, 2), "4": (1, 0), "5": (1, 1), "6": (1, 2),
               "1": (2, 0), "2": (2, 1), "3": (2, 2), None: (3, 0), "0": (3, 1), "A": (3, 2)}
directional_pos = {None: (0, 0), "^": (0, 1), "A": (0, 2), "<": (1, 0), "v": (1, 1), ">": (1, 2)}


def sanitize_paths(paths, p0, numeric=True):

    excluded_pos = numeric_pos[None] if numeric else directional_pos[None]

    i = 0
    while i < len(paths):
        p = list(p0)
        for d in paths[i]:

            if d == "^":
                p[0] -= 1
            if d == "v":
                p[0] += 1

            if d == "<":
                p[1] -= 1
            if d == ">":
                p[1] += 1
            
            if tuple(p) == excluded_pos:
                paths.pop(i)
                i -= 1
                break
        
        i += 1

    return paths


def get_shortest_paths(src_pos, trg_pos, numeric=True):
    cx = "^" if trg_pos[0] - src_pos[0] < 0 else "v"
    dx = abs(trg_pos[0] - src_pos[0])
    cy = "<" if trg_pos[1] - src_pos[1] < 0 else ">"
    dy = abs(trg_pos[1] - src_pos[1])

    return sanitize_paths(list(set([cx * dx + cy * dy, cy * dy + cx * dx])), src_pos, numeric=numeric)


def solve_numeric(num):
    pos = numeric_pos["A"]

    sequence = []

    for n in num:
        p = numeric_pos[n]
        paths = get_shortest_paths(pos, p, numeric=True)
        pos = p
        sequence.append(paths)
    
    sequence_parts = []
    for part in sequence:
        tmp = []
        for p in part:
            tmp.append("".join(p) + "A")
        
        sequence_parts.append(tmp)

    return sequence_parts


def solve_directional(seq):
    pos = directional_pos["A"]

    sequence = []

    for n in seq:
        p = directional_pos[n]
        paths = get_shortest_paths(pos, p, numeric=False)
        pos = p
        sequence.append(paths)
    
    sequence_parts = []
    for part in sequence:
        tmp = []
        for p in part:
            tmp.append("".join(p) + "A")
        
        sequence_parts.append(tmp)

    return sequence_parts


memory = {}

def min_cost(seq, depth):
    if depth == 0:
        return len(seq)
    
    if (seq, depth) in memory:
        return memory[(seq, depth)]
    
    sub_sequences = solve_directional(seq)

    cost = 0
    for part in sub_sequences:
        cost += min([min_cost(seq, depth-1) for seq in part])
    
    memory[(seq, depth)] = cost
    return cost


def parse_input():

    with open(os.path.join(os.path.dirname(__file__), "input.txt"), "r") as file:
        txt = file.read().strip()
    
    return txt.split("\n")


def solve_level_1():
    """
    Solve level 1
    """

    # Read input file
    nums = parse_input()

    depth = 2

    tot = 0
    for num in nums:
        sequence = solve_numeric(num)

        seq_tot = 0
        for part in sequence:
            seq_tot += min([min_cost(seq, depth) for seq in part])

        tot += int(num[:-1]) * seq_tot

    return tot


def solve_level_2():
    """
    Solve level 2
    """

    # Read input file
    nums = parse_input()

    depth = 25

    tot = 0
    for num in nums:
        sequence = solve_numeric(num)

        seq_tot = 0
        for part in sequence:
            seq_tot += min([min_cost(seq, depth) for seq in part])

        tot += int(num[:-1]) * seq_tot

    return tot


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
