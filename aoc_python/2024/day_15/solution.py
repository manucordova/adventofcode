import os
import time
import adventofcode as aoc


class Item:
    def __init__(self, pos_x, pos_y, w=1, h=1):
        self._pos = (pos_x, pos_y)
        self._size = (w, h)

    def get_pos(self):
        return self._pos

    def set_pos(self, pos_x, pos_y):
        self._pos = (pos_x, pos_y)

    @property
    def x(self):
        return self._pos[0]

    @property
    def y(self):
        return self._pos[1]

    @property
    def w(self):
        return self._size[0]

    @property
    def h(self):
        return self._size[1]

    @staticmethod
    def _get_vector(direction):
        if direction == "<":
            return (-1, 0)
        if direction == ">":
            return (1, 0)
        if direction == "^":
            return (0, -1)
        if direction == "v":
            return (0, 1)
        raise ValueError(f"Unknown direction: {direction}")

    def is_blocked(self, v, grid, items):

        for i in range(self.w):
            for j in range(self.h):

                next_x = self.x + i + v[0]
                next_y = self.y + j + v[1]

                # Check walls
                if grid[next_x][next_y] == 1:
                    return True

                # Check other items
                for item in items:
                    if (item.get_pos() != self.get_pos()
                        and item.collides(next_x, next_y)
                        and item.is_blocked(v, grid, items)):
                        return True

        return False

    def collides(self, x, y):
        for i in range(self.w):
            for j in range(self.h):
                if self.x + i == x and self.y + j == y:
                    return True
        return False

    def _apply_move(self, v, items):

        for i in range(self.w):
            for j in range(self.h):

                # Check other items
                for item in items:
                    if (item.get_pos() != self.get_pos()
                        and item.collides(self.x + i + v[0], self.y + j + v[1])):
                        item._apply_move(v, items)

        self.set_pos(self.x + v[0], self.y + v[1])

    def move(self, direction, grid, items):

        v = self._get_vector(direction)

        # 1. Check if wall clashes
        if self.is_blocked(v, grid, items):
            return False

        # 3. Apply move
        self._apply_move(v, items)


def print_grid(grid, boxes, robot, direction=None):

    output = ""

    j = 0
    while j < len(grid[0]):
        i = 0
        while i < len(grid):
            if grid[i][j] == 1:
                output += "#"
            else:
                item = False
                for box in boxes:
                    if box.x == i and box.y == j:
                        output += "[]"
                        i += 1
                        item = True
                        break
                if robot.x == i and robot.y == j:
                    output += "@" if direction is None else direction
                    item = True

                if not item:
                    output += "."

            i += 1

        output += "\n"
        j += 1
    print(output)


def parse_input(wide=False):

    with open(os.path.join(os.path.dirname(__file__), "input.txt"), "r") as file:
        lines = file.read().strip().split("\n")

    grid = []
    boxes = []
    i = 0
    while lines[i].startswith("#"):

        g = []
        for c in lines[i]:
            for _ in range(2 if wide else 1):
                g.append(1 if c == "#" else 0)
        grid.append(g.copy())

        boxes.extend([Item(2 * j if wide else j, i, w=2 if wide else 1) for j, c in enumerate(lines[i]) if c == "O"])
        if "@" in lines[i]:
            j = lines[i].index("@")
            robot = Item(2 * j if wide else j, i)
        i += 1

    grid = list(map(list, zip(*grid)))

    directions = ""
    while i < len(lines):
        directions += lines[i]
        i += 1

    return grid, boxes, robot, directions


def solve_level_1():
    """
    Solve level 1
    """

    # Read input file
    grid, boxes, robot, directions = parse_input()

    for direction in directions:

        robot.move(direction, grid, boxes)

    return sum([box.x + 100 * box.y for box in boxes])


def solve_level_2():
    """
    Solve level 2
    """

    # Read input file
    grid, boxes, robot, directions = parse_input(wide=True)

    for direction in directions:

        robot.move(direction, grid, boxes)

    return sum([box.x + 100 * box.y for box in boxes])


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
