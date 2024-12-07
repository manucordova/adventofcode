import pathlib as pl
import re
import adventofcode as aoc


def get_year_day_from_path():
    """
    Get the challenge year and day from the current path

    Returns
    -------
    int
        Challenge year
    int
        Challenge day
    """

    this_path = str(pl.Path(__file__).resolve())
    year = int(this_path.split("/")[-3])
    day = int(this_path.split("day_")[1].split("/")[0])

    return year, day


def solve(txt):
    result = re.findall(r"mul\(\d+,\d+\)", txt)
    return sum([int((num := re.split(r"\W", res))[1]) * int(num[2]) for res in result])


def solve_level_1():

    """
    Solve level 1
    """

    # Read input file
    with open(pl.Path(pl.Path(__file__).parent.resolve(), "input.txt"), "r") as file:
        input_txt = file.read().strip()

    return solve(input_txt)


def solve_level_2():

    """
    Solve level 2
    """

    # Read input file
    with open(pl.Path(pl.Path(__file__).parent.resolve(), "input.txt"), "r") as file:
        input_txt = file.read().strip()

    txt = re.sub(r"don't\(\)(.|\n)*?do\(\)", "", input_txt)
    return solve(txt)


if __name__ == "__main__":

    debug = True

    year, day = get_year_day_from_path()
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
