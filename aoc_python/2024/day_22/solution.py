import os
import time
import adventofcode as aoc


class Sequence:

    def __init__(self, num):
        self._num = num
        self._old_num = None
        self._price = self._compute_price()
        self._old_price = None
        self._prices = {}
        self._diffs = []
    
    def _mix(self, val):
        self._num = self._num ^ val
    
    def _prune(self):
        self._num = self._num % 16777216
    
    def _compute_price(self):
        return self._num % 10

    def _update_diffs(self):

        self._diffs.append(self._price - self._old_price)

        if len(self._diffs) > 4:
            self._diffs.pop(0)
        
        if len(self._diffs) == 4 and tuple(self._diffs) not in self._prices:
                self._prices[tuple(self._diffs)] = self._price
    
    
    def step(self):

        self._old_num = self._num
        self._old_price = self._price

        self._mix(self._num * 64)
        self._prune()

        self._mix(self._num // 32)
        self._prune()

        self._mix(self._num * 2048)
        self._prune()

        self._price = self._compute_price()

        self._update_diffs()

    def get_num(self):
        return self._num

    def get_price(self):
        return self._price
    
    def get_prices(self):
        return self._prices


def parse_input():

    with open(os.path.join(os.path.dirname(__file__), "input.txt"), "r") as file:
        txt = file.read().strip()
    
    return list(map(int, txt.split("\n")))


def solve_level_1():
    """
    Solve level 1
    """

    # Read input file
    nums = parse_input()

    tot = 0

    for num in nums:
        seq = Sequence(num)
        for _ in range(2000):
            seq.step()
        tot += seq.get_num()

    return tot


def solve_level_2():
    """
    Solve level 2
    """

    # Read input file
    nums = parse_input()

    all_prices = {}

    for num in nums:
        seq = Sequence(num)
        for _ in range(2000):
            seq.step()
        for s, p in seq.get_prices().items():
            if s not in all_prices:
                all_prices[s] = 0
            all_prices[s] += p

    return max(all_prices.values())


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
