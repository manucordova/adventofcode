import os
import time
import itertools as it
import adventofcode as aoc


class Network:

    def __init__(self, links):
        self._nodes = {}
        self._neighbours = {}

        for link in links:
            c1, c2 = link.split("-")

            if c1 not in self._neighbours:
                self._neighbours[c1] = []
            if c2 not in self._neighbours:
                self._neighbours[c2] = []

            self._neighbours[c1].append(c2)
            self._neighbours[c2].append(c1)

            self._nodes[c1] = len(self._neighbours[c1])
            self._nodes[c2] = len(self._neighbours[c2])

    def find_fully_connected(self, c, min_size=3, exclude=None):

        groups = []
        done = [] if exclude is None else exclude

        for n in self._neighbours[c]:
            if n not in done:
                this_group = [c, n]
                i = 1
                while i < len(this_group):
                    for n2 in self._neighbours[this_group[i]]:
                        if all([k in self._neighbours[n2] for k in this_group]):
                            this_group.append(n2)

                    i += 1
                
                done.extend(this_group)
                if len(this_group) >= min_size:
                    groups.append(this_group)
        return groups
    
    @staticmethod
    def get_groups(group, size):

        if len(group) < size:
            raise ValueError("Group size is too small!")

        if len(group) == size:
            return [tuple(sorted(group))]
        
        return list(map(tuple, map(sorted, it.combinations(group, size))))

    
    def find_groups(self, size=3):

        groups = set()
        done = set()

        for n, w in self._nodes.items():

            if w >= size - 1:
                cur_groups = self.find_fully_connected(n, min_size=size)

                for group in cur_groups:
                    for g in self.get_groups(group, size):
                        groups.add(g)
                    for g in group:
                        done.add(g)

            done.add(n)

        return groups
    
    def find_longest_group(self, min_size=3):

        max_group = []
        done = set()

        for n, w in self._nodes.items():

            if w >= min_size - 1:
                cur_groups = self.find_fully_connected(n, min_size=min_size)

                for group in cur_groups:
                    if len(group) > len(max_group):
                        max_group = group.copy()

            done.add(n)

        return sorted(max_group)


def parse_input():

    with open(os.path.join(os.path.dirname(__file__), "input.txt"), "r") as file:
        links = file.read().strip().split("\n")
    
    return Network(links)


def solve_level_1():
    """
    Solve level 1
    """

    # Read input file
    net = parse_input()

    groups = net.find_groups()

    return len([1 for group in groups if any([g.startswith("t") for g in group]) ])


def solve_level_2():
    """
    Solve level 2
    """

    # Read input file
    net = parse_input()

    max_group = net.find_longest_group()

    return ",".join(max_group)


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
