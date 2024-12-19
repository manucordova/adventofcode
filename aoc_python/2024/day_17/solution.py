import os
import time
import adventofcode as aoc
import numpy as np


class Computer:
    def __init__(self, txt):
        self.pointer = 0
        self.output = []
        self._initialize(txt)

    def _initialize(self, txt):

        lines = txt.split("\n")

        self.A = int(lines[0].split()[-1])
        self.B = int(lines[1].split()[-1])
        self.C = int(lines[2].split()[-1])

        self.values = list(map(int, lines[4].split(": ")[1].split(",")))

    def reset(self, val):
        self.A = val
        self.B = 0
        self.C = 0
        self.pointer = 0
        self.output = []

    def __repr__(self):
        output = f"Register A: {self.A}\n"
        output += f"Register B: {self.B}\n"
        output += f"Register C: {self.C}\n"
        output += "\nProgram: " + ",".join(map(str, self.values)) + "\n"
        output += " " * (9 + 2 * self.pointer) + "^" + "\n"
        return output

    def get_output(self):
        return ",".join(map(str, self.output))

    def get_program(self):
        return ",".join(map(str, self.values))

    def combo(self, op):
        if op < 4:
            return op
        if op == 4:
            return self.A
        if op == 5:
            return self.B
        if op == 6:
            return self.C
        if op > 7:
            raise ValueError(f"Unexpected combo operand: {op}")

    def _adv(self):

        assert self.values[self.pointer] == 0
        self.pointer += 1

        self.A = self.A // (2 ** self.combo(self.values[self.pointer]))
        self.pointer += 1

    def _bxl(self):

        assert self.values[self.pointer] == 1
        self.pointer += 1

        self.B = self.B ^ self.values[self.pointer]
        self.pointer += 1

    def _bst(self):

        assert self.values[self.pointer] == 2
        self.pointer += 1

        self.B = self.combo(self.values[self.pointer]) % 8
        self.pointer += 1

    def _jnz(self):

        assert self.values[self.pointer] == 3
        self.pointer += 1

        if self.A == 0:
            self.pointer += 1
        else:
            self.pointer = self.values[self.pointer]

    def _bxc(self):

        assert self.values[self.pointer] == 4
        self.pointer += 1

        self.B = self.B ^ self.C
        self.pointer += 1

    def _out(self):

        assert self.values[self.pointer] == 5
        self.pointer += 1

        self.output.append(self.combo(self.values[self.pointer]) % 8)
        self.pointer += 1

    def _bdv(self):

        assert self.values[self.pointer] == 6
        self.pointer += 1

        self.B = self.A // (2 ** self.combo(self.values[self.pointer]))
        self.pointer += 1

    def _cdv(self):

        assert self.values[self.pointer] == 7
        self.pointer += 1

        self.C = self.A // (2 ** self.combo(self.values[self.pointer]))
        self.pointer += 1

    def _get_instruction(self, op):
        instr = {0: self._adv,
                 1: self._bxl,
                 2: self._bst,
                 3: self._jnz,
                 4: self._bxc,
                 5: self._out,
                 6: self._bdv,
                 7: self._cdv}
        return instr[op]

    def run(self, debug=False):
        while self.pointer >= 0 and self.pointer < len(self.values):
            self._get_instruction(self.values[self.pointer])()
            if debug:
                print(self)


def parse_input():

    with open(os.path.join(os.path.dirname(__file__), "input.txt"), "r") as file:
        txt = file.read().strip()

    return Computer(txt)


def solve_level_1():
    """
    Solve level 1
    """

    # Read input file
    computer = parse_input()

    computer.run()
    return computer.get_output()


class Optimizer:
    def __init__(self, n_bits, computer, trg, n_gen=1000, n_sel=10, n_mut=80, n_rng=100, n_crs=100):
        self.n_bits = n_bits
        self.computer = computer
        self.trg = trg

        self.n_gen = n_gen
        self.n_rng = n_rng
        self.n_mut = n_mut
        self.n_sel = n_sel
        self.n_crs = n_crs

        self.rng = np.random.default_rng(seed=123)

    @staticmethod
    def get_num(vals):
        return sum([v * 8**n for n, v in enumerate(vals)])

    def run_program(self, vals):

        self.computer.reset(self.get_num(vals))
        self.computer.run()
        return self.computer.get_output()

    def evaluate(self, vals):
        return self.loss(self.run_program(vals)) + np.log(self.get_num(vals))

    def loss(self, output):
        if len(output) != len(self.trg):
            return 1e12

        return sum([float(v != t) for v, t in zip(output, self.trg)]) / len(self.trg) * 1000.0

    def generate(self):
        return self.rng.integers(0, 8, size=self.n_bits)

    def mutate(self, vals):

        i = self.rng.integers(0, len(vals))
        vals[i] = self.rng.integers(0, 8)
        return vals

    def crossover(self, v1, v2):
        idx = np.arange(len(v1))
        self.rng.shuffle(idx)
        v = np.copy(v1)
        v[idx[:len(v1)//2]] = v2[idx[:len(v1)//2]]

        return v

    def get_next_pop(self, pop):

        next_pop = []

        for vals in pop:
            next_pop.append(np.copy(vals))
            for _ in range(self.n_mut):
                next_pop.append(self.mutate(np.copy(vals)))

        for _ in range(self.n_rng):
            next_pop.append(self.generate())

        for _ in range(self.n_crs):
            i, j = self.rng.integers(0, self.n_sel, size=2)
            next_pop.append(self.crossover(pop[i], pop[j]))

        return next_pop

    def run(self):

        # Initialize seed for first population
        pop = [self.generate() for _ in range(self.n_sel)]

        for i_gen in range(self.n_gen):

            # Generate next population
            next_pop = self.get_next_pop(pop)

            # Rank population
            losses = [self.evaluate(vals) for vals in next_pop]
            sel_idx = np.argsort(losses)

            # Select best unique samples as a seed for the next population
            pop = []
            sel_losses = []
            for i in sel_idx:
                if not any([np.all(next_pop[i] == p) for p in pop]):
                    pop.append(next_pop[i])
                    sel_losses.append(losses[i])

                    if len(pop) >= self.n_sel:
                        break

            print(f"Generation {i_gen+1}\n")

            print("    target: " + self.trg + "\n")

            print("    Best samples:")
            for i in range(self.n_sel):
                print("    " + ",".join(map(str, pop[i])) + f" = {self.get_num(pop[i])}")
                print("    result: " + self.run_program(pop[i]))
                print(f"    loss: {sel_losses[i]}")

        return self.get_num(pop[0])


def solve_level_2():
    """
    Solve level 2
    """

    # Read input file
    computer = parse_input()

    trg = computer.get_program()

    opt = Optimizer(16, computer, trg, n_gen=10, n_sel=10, n_mut=80, n_rng=100, n_crs=100)

    return opt.run()


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
