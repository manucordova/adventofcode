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


import pathlib as pl


def count_word_at_pos(word, grid, i, j):

    if grid[i][j] != word[0]:
        return 0

    num = 0

    # Search right
    if all([grid[i][j+k] == w for k, w in enumerate(word)]):
        num += 1

    # Search down
    if all([grid[i+k][j] == w for k, w in enumerate(word)]):
        num += 1

    # Search left
    if all([grid[i][j-k] == w for k, w in enumerate(word)]):
        num += 1

    # Search down
    if all([grid[i-k][j] == w for k, w in enumerate(word)]):
        num += 1

    # Search down right
    if all([grid[i+k][j+k] == w for k, w in enumerate(word)]):
        num += 1

    # Search down left
    if all([grid[i+k][j-k] == w for k, w in enumerate(word)]):
        num += 1

    # Search up right
    if all([grid[i-k][j+k] == w for k, w in enumerate(word)]):
        num += 1

    # Search up left
    if all([grid[i-k][j-k] == w for k, w in enumerate(word)]):
        num += 1

    return num


def count_word(word, grid):

    num = 0

    nrow = len(grid)
    ncol = len(grid[0])

    for i in range(nrow):
        for j in range(ncol):

            num += count_word_at_pos(word, grid, i, j)

    return num


def pad_grid(grid, pad):

    for line in grid:
        for _ in range(pad):
            line.insert(0, ".")
        line.extend(["." for _ in range(pad)])

    n = len(grid[0])
    for _ in range(pad):
        grid.insert(0, ["." for _ in range(n)])
        grid.insert(len(grid), ["." for _ in range(n)])


def count_x_word_at_pos(word, grid, i, j):

    n = len(word) // 2

    idx = list([-x - 1 for x in reversed(range(n))])
    idx.append(0)
    idx.extend([x + 1 for x in range(n)])

    assert len(idx) == len(word)

    if grid[i][j] != word[n]:
        return 0

    a = False
    b = False
    # Search down-right or up-left
    if all([grid[i+k][j+k] == w for k, w in zip(idx, word)]) or all([grid[i-k][j-k] == w for k, w in zip(idx, word)]):
        a = True

    # Search up-right or down-left
    if all([grid[i+k][j-k] == w for k, w in zip(idx, word)]) or all([grid[i-k][j+k] == w for k, w in zip(idx, word)]):
        b = True

    return int(a) * int(b)


def count_x_word(word, grid):

    num = 0

    nrow = len(grid)
    ncol = len(grid[0])

    for i in range(nrow):
        for j in range(ncol):

            num += count_x_word_at_pos(word, grid, i, j)

    return num


def solve_level_1():

    """
    Solve level 1
    """

    # Read input file
    with open(pl.Path(pl.Path(__file__).parent.resolve(), "input.txt"), "r") as file:
        input_txt = file.read().strip()

    word = "XMAS"

    grid = [[c for c in line] for line in input_txt.split("\n")]

    pad_grid(grid, len(word))

    return count_word(word, grid)


def solve_level_2():

    """
    Solve level 2
    """

    # Read input file
    with open(pl.Path(pl.Path(__file__).parent.resolve(), "input.txt"), "r") as file:
        input_txt = file.read().strip()

    word = "MAS"

    grid = [[c for c in line] for line in input_txt.split("\n")]

    pad_grid(grid, len(word) // 2)

    return count_x_word(word, grid)


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
