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


def parse_input(txt: str):

    mandatory_before = {}
    update_list = []

    for line in txt.split("\n"):

        if "|" in line:
            a, b = map(int, line.split("|"))
            if b not in mandatory_before:
                mandatory_before[b] = []
            mandatory_before[b].append(a)

        elif "," in line:
            update_list.append(list(map(int, line.split(","))))

    return mandatory_before, update_list


def check_order(update: list, mandatory_before: dict):

    for i, page in enumerate(update):
        if page in mandatory_before:
            for b in mandatory_before[page]:
                if b in update[i+1:]:
                    return False

    return True


def reorder(update: list, mandatory_before: dict):

    changed = True

    while changed:
        changed = False

        for i, page in enumerate(update):
            if page in mandatory_before:
                for b in mandatory_before[page]:
                    if b in update[i+1:]:
                        update.remove(b)
                        update.insert(i, b)

                        i += 1
                        changed = True


def solve_level_1():
    """
    Solve level 1
    """

    # Read input file
    with open(pl.Path(pl.Path(__file__).parent.resolve(), "input.txt"), "r") as file:
        input_txt = file.read().strip()

    mandatory_before, update_list = parse_input(input_txt)

    tot = 0
    for update in update_list:
        if check_order(update, mandatory_before):
            tot += update[len(update) // 2]

    return tot


def solve_level_2():
    """
    Solve level 2
    """

    # Read input file
    with open(pl.Path(pl.Path(__file__).parent.resolve(), "input.txt"), "r") as file:
        input_txt = file.read().strip()

    mandatory_before, update_list = parse_input(input_txt)

    tot = 0
    for update in update_list:
        if not check_order(update, mandatory_before):
            reorder(update, mandatory_before)
            tot += update[len(update) // 2]

    return tot


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
