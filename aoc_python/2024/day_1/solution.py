import pathlib as pl
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


def parse_input(txt):
    list1 = []
    list2 = []

    for line in txt.split("\n"):
        items = line.split()
        list1.append(int(items[0]))
        list2.append(int(items[1]))

    return list1, list2


def solve_level_1():
    """
    Solve level 1
    """

    # Read input file
    with open(pl.Path(pl.Path(__file__).parent.resolve(), "input.txt"), "r") as file:
        input_txt = file.read().strip()
    
    list1, list2 = parse_input(input_txt)

    total = 0
    for item1, item2 in zip(sorted(list1), sorted(list2)):
        total += abs(item2 - item1)

    return total


def solve_level_2():
    """
    Solve level 2
    """

    # Read input file
    with open(pl.Path(pl.Path(__file__).parent.resolve(), "input.txt"), "r") as file:
        input_txt = file.read().strip()
    
    list1, list2 = parse_input(input_txt)

    nums = {}

    total = 0
    for n in list1:
        if n not in nums:
            nums[n] = n * list2.count(n)
        total += nums[n]

    return total


if __name__ == "__main__":

    debug = False

    year, day = get_year_day_from_path()
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
