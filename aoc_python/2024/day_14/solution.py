import os
import time
import adventofcode as aoc

from copy import deepcopy
from matplotlib import pyplot as plt


def parse_input():

    with open(os.path.join(os.path.dirname(__file__), "input.txt"), "r") as file:
        txt = file.read().strip()

    guards = []

    for line in txt.split("\n"):
        px = int(line.split("p=")[1].split(",")[0])
        py = int(line.split("p=")[1].split(",")[1].split()[0])
        vx = int(line.split("v=")[1].split(",")[0])
        vy = int(line.split("v=")[1].split(",")[1].split()[0])

        guards.append([[px, py], [vx, vy]])
    
    return guards


def normalize(p, n):

    while p < 0:
        p += n
    while p >= n:
        p -= n

    return p


def update(guards, nx, ny):

    for p, v in guards:
        p[0] = normalize(p[0] + v[0], nx)
        p[1] = normalize(p[1] + v[1], ny)

    return guards


def print_map(guards, nx, ny):
    grid = [[0 for _ in range(nx)] for _ in range(ny)]

    for p, _ in guards:
        grid[p[1]][p[0]] += 1

    print()
    print("\n".join(["".join([str(x) if x > 0 else "." for x in line]) for line in grid]))
    print()


def plot_map(guards, nx, ny, title=""):
    grid = [[0 for _ in range(nx)] for _ in range(ny)]

    for p, _ in guards:
        grid[p[1]][p[0]] += 1

    fig = plt.figure(figsize=(4, 3))
    ax = fig.add_subplot(1, 1, 1)

    ax.imshow(grid, vmin=0, vmax=1, cmap="Greys")
    ax.set_title(title)

    plt.show()
    plt.close()


def plot_map_interactive(guard_frames, nx, ny):

    grid_frames = []

    for guards in guard_frames:

        grid = [[0 for _ in range(nx)] for _ in range(ny)]

        for p, _ in guards:
            grid[p[1]][p[0]] += 1
        
        grid_frames.append(deepcopy(grid))

    fig = plt.figure(figsize=(4, 3))
    ax = fig.add_subplot(1, 1, 1)

    global i
    i = 0
    ax.imshow(grid_frames[i], vmin=0, vmax=1, cmap="Greys")
    ax.set_title(f"Frame {i}")

    plt.subplots_adjust(bottom = 0.15)

    #Update function
    def update_plot():

        global i
        ax.cla()
        ax.imshow(grid_frames[i], vmin=0, vmax=1, cmap="Greys")
        ax.set_title(f"Frame {i}")
        fig.canvas.draw_idle()

    def on_press(event):
        global i
        if event.key == 'right':
            i += 1
        if event.key == 'left':
            i -= 1
        
        if i < 0:
            i = 0
        if i >= len(grid_frames):
            i = len(grid_frames) - 1

        update_plot()

    fig.canvas.mpl_connect('key_press_event', on_press)
    
    plt.show()
    plt.close()


def count_quadrants(guards, nx, ny):

    n1 = len([1 for p, _ in guards if p[0] < nx // 2 and p[1] < ny // 2])
    n2 = len([1 for p, _ in guards if p[0] > nx // 2 and p[1] < ny // 2])
    n3 = len([1 for p, _ in guards if p[0] < nx // 2 and p[1] > ny // 2])
    n4 = len([1 for p, _ in guards if p[0] > nx // 2 and p[1] > ny // 2])

    return n1 * n2 * n3 * n4


def solve_level_1():
    """
    Solve level 1
    """

    # Read input file
    guards = parse_input()

    nx = 101
    ny = 103

    n_update = 100

    for _ in range(n_update):
        guards = update(guards, nx, ny)

    return count_quadrants(guards, nx, ny)


def solve_level_2():
    """
    Solve level 2
    """

    # Read input file
    guards = parse_input()

    nx = 101
    ny = 103

    n_update = 1000

    guard_frames = []
    guard_frames.append(deepcopy(guards))

    for _ in range(n_update):

        guards = update(guards, nx, ny)
        guard_frames.append(deepcopy(guards))

    plot_map_interactive(guard_frames, nx, ny)

    res = 1e12
    guards = deepcopy(guard_frames[0])
    i = 0
    while True:
        guards = update(guards, nx, ny)
        i += 1
        new_res = count_quadrants(guards, nx, ny)
        if new_res < res:
            plot_map(guards, nx, ny, f"Frame {i}")
            res = new_res
    
    return 0


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
