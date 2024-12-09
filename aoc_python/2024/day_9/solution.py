import os
import time
import adventofcode as aoc


def parse_input(flag=False):

    with open(os.path.join(os.path.dirname(__file__), "input.txt"), "r") as file:
        txt = file.read().strip()

    # Array of (value, index_start, length)
    values = []

    value = 0
    index_start = 0

    i = 0
    while i < len(txt):

        index_start += int(txt[i-1]) if i > 0 else 0
        num_values = int(txt[i])

        if flag:
            values.append((value, index_start, num_values, True))
        else:
            values.append((value, index_start, num_values))

        index_start += num_values
        value += 1

        i += 2

    return values


def to_array(values: list[tuple], flag=False):
    output = []

    if flag:
        for v, i, n, _ in values:
            output.extend([0 for _ in range(i - len(output))])
            output.extend([v for _ in range(n)])

    else:
        for v, i, n in values:
            output.extend([0 for _ in range(i - len(output))])
            output.extend([v for _ in range(n)])

    return output


def print_values(values: list[tuple], flag=False):
    output = ""

    if flag:
        for v, i, n, _ in values:
            output += "." * (i - len(output))
            output += str(v) * n
    else:
        for v, i, n in values:
            output += "." * (i - len(output))
            output += str(v) * n
    print(output)


def compress_part1(values: list[tuple]):

    i = 0

    while True:
        v, _, n = values.pop()

        while i < len(values) - 1:
            _, i1, n1 = values[i]
            _, i2, _ = values[i+1]

            n_gap = i2 - (i1 + n1)

            if n_gap > 0:
                n_insert = min(n, n_gap)
                values.insert(i+1, (v, i1 + n1, n_insert))
                n -= n_insert
                i += 1

                if n <= 0:
                    break

            i += 1
        
        if n > 0:
            _, i1, n1 = values[-1]
            values.insert(len(values), (v, i1 + n1, n))
            return


def compress_part2(values: list[tuple]):

    j = len(values) - 1

    while j > 0:

        v, _, n, flag = values[j]
        
        # Value was not yet seen, check if it can be reordered
        if flag:

            # Check if it can be inserted 
            for i in range(j):
                _, i1, n1, _ = values[i]
                _, i2, _, _ = values[i+1]
                # The gap is large enough: insert the values there, update flag
                if n <= i2 - (i1 + n1):
                    values.pop(j)
                    values.insert(i+1, (v, i1 + n1, n, False))

                    j += 1

                    break

        j -= 1


def solve_level_1():
    """
    Solve level 1
    """

    # Read input file
    values = parse_input()

    compress_part1(values)

    return sum([i * v for i, v in enumerate(to_array(values))])


def solve_level_2():
    """
    Solve level 2
    """

    # Read input file
    values = parse_input(flag=True)

    compress_part2(values)

    return sum([i * v for i, v in enumerate(to_array(values, flag=True))])


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
