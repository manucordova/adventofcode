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


def is_monotonous(report):

    sorted_report = list(sorted(report))
    sorted_report_inv = list(reversed(sorted(report)))

    return (all([r1 == r2 for r1, r2 in zip(report, sorted_report)]) or
            all([r1 == r2 for r1, r2 in zip(report, sorted_report_inv)]))


def is_safe(report, min_diff=1, max_diff=3):

    if not is_monotonous(report):
        return False

    for r1, r2 in zip(report[:-1], report[1:]):
        if abs(r2 - r1) < min_diff or abs(r2 - r1) > max_diff:
            return False

    return True


def is_safe_with_tol(report, min_diff=1, max_diff=3):

    if is_safe(report, min_diff=min_diff, max_diff=max_diff):
        return True

    for i in range(len(report)):
        tmp_report = report.copy()
        tmp_report.pop(i)
        if is_safe(tmp_report):
            return True

    return False


def solve_level_1():

    """
    Solve level 1
    """

    # Read input file
    with open(pl.Path(pl.Path(__file__).parent.resolve(), "input.txt"), "r") as file:
        input_txt = file.read().strip()

    report_list = [list(map(int, line.split()))for line in input_txt.split("\n")]

    total = 0
    for report in report_list:
        if is_safe(report):
            total += 1

    return total


def solve_level_2():

    """
    Solve level 2
    """

    # Read input file
    with open(pl.Path(pl.Path(__file__).parent.resolve(), "input.txt"), "r") as file:
        input_txt = file.read().strip()

    report_list = [list(map(int, line.split()))for line in input_txt.split("\n")]

    total = 0
    for report in report_list:
        if is_safe_with_tol(report):
            total += 1

    return total


if __name__ == "__main__":

    debug = True

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
