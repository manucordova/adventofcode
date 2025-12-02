# Initialize an Advent of Code challenge

import adventofcode as aoc
import argparse


class ParserError(Exception):
    pass


python_canevas = """import os
import time
import adventofcode as aoc


def parse_input():

    with open(os.path.join(os.path.dirname(__file__), "input.txt"), "r") as file:
        txt = file.read().strip()

    return txt


def solve_level_1():
    \"\"\"
    Solve level 1
    \"\"\"

    # Read input file
    input_txt = parse_input()

    print(input_txt)

    return 0


def solve_level_2():
    \"\"\"
    Solve level 2
    \"\"\"

    # Read input file
    input_txt = parse_input()

    print(input_txt)

    return 0


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
"""


if __name__ == "__main__":

    # Setup parser
    usage_str = "python initialize_challenge.py -y [year] -d [day]"
    descr_str = "Initializes an Advent of Code challenge with requested day and year."
    epilog_str = ""

    parser = argparse.ArgumentParser(
        prog="initialize_challenge",
        usage=usage_str,
        description=descr_str,
        epilog=epilog_str,
    )

    parser.add_argument("-y", "--year", type=int, help="requested year")
    parser.add_argument("-d", "--day", type=int, help="requested day")
    parser.add_argument("-n", "--name", type=str, help="root directory for challenges")
    parser.add_argument(
        "-f", "--force", action="store_true", help="force overwriting the directory"
    )

    # Check arguments
    args = parser.parse_args()

    if args.year is None:
        raise ParserError("No year requested")

    if args.day is None:
        raise ParserError("No day requested")

    if args.name is None:
        raise ParserError("No root directory requested")

    con = aoc.AOCConnector(args.year, args.day)

    con.initialize(canevas=python_canevas, dir_name=args.name)
