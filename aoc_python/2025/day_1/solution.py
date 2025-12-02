import os
import time
import adventofcode as aoc


class Password:
    def __init__(self, max_num=100, cursor=50, count_passing=False, debug=False):

        self._max_num = max_num
        self._cursor = cursor
        self._count_passing = count_passing
        self._num_zeros = 0
        self._debug = debug

    def _update_cursor_ignore_passing(self, delta):
        self._cursor += delta
        self._cursor %= self._max_num
        if self._cursor == 0:
            self._num_zeros += 1

    def _update_cursor_count_passing(self, delta):

        if delta < 0:
            from_zero = self._cursor == 0
            self._cursor += delta

            self._num_zeros += abs((self._cursor - 1) // self._max_num) - int(from_zero)
            self._cursor %= self._max_num

        else:
            self._cursor += delta
            self._num_zeros += self._cursor // self._max_num
            self._cursor %= self._max_num

    def _update_cursor(self, delta):

        if self._count_passing:
            self._update_cursor_count_passing(delta)
        else:
            self._update_cursor_ignore_passing(delta)

    def apply_instructions(self, instructions):

        for instr in instructions.split("\n"):

            delta = int(instr[1:])
            debug_str = str(self._cursor)

            if instr.startswith("L"):
                self._update_cursor(-delta)
            elif instr.startswith("R"):
                self._update_cursor(delta)

            if self._debug:
                debug_str += f" --> {instr} --> {self._cursor} ({self._num_zeros} zeros)"
                print(debug_str)
        return self._num_zeros


def parse_input():

    with open(os.path.join(os.path.dirname(__file__), "input.txt"), "r") as file:
        txt = file.read().strip()

    return txt


def solve_level_1():
    """
    Solve level 1
    """

    # Read input file
    input_txt = parse_input()

    return Password().apply_instructions(input_txt)


def solve_level_2():
    """
    Solve level 2
    """

    # Read input file
    input_txt = parse_input()

    return Password(count_passing=True).apply_instructions(input_txt)


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
