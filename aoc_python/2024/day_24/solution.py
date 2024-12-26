import os
import time
import adventofcode as aoc


class Monitor:

    def __init__(self, lines, swap={}):
        self._bits = {}
        self._init_vals = [line for line in lines if ": " in line]
        self._init_instr = [swap[line] if line in swap else line for line in lines if " -> " in line]
        self._instr = self._init_instr.copy()

        for line in self._init_vals:
            self._init_bit(line)

    def _init_bit(self, line):
        bit, val = line.split(": ")
        self._bits[bit] = int(val) == 1

    def _apply_gate(self, line):

        inputs, output = line.split(" -> ")

        x, instr, y = inputs.split()

        if x not in self._bits or y not in self._bits:
            return False

        if instr == "AND":
            self._bits[output] = self._bits[x] and self._bits[y]
        elif instr == "XOR":
            self._bits[output] = self._bits[x] != self._bits[y]
        elif instr == "OR":
            self._bits[output] = self._bits[x] or self._bits[y]
        
        return True
    
    def run(self):

        while self._instr:
            line = self._instr.pop(0)

            success = self._apply_gate(line)
            if not success:
                self._instr.append(line)

    def get_output(self, start="z", keep_bits=False):

        output = ""
        for k in reversed(sorted(self._bits.keys())):
            if k.startswith(start):
                output += str(int(self._bits[k]))

        if keep_bits:
            return output
        else:
            return int(output, 2)
    
    def reset(self, x_val, y_val, i_bit=0, n_bits=45):
        self._bits = {}
        for i in range(n_bits):
            if i == i_bit:
                self._bits[f"x{i:02.0f}"] = x_val
                self._bits[f"y{i:02.0f}"] = y_val
            else:
                self._bits[f"x{i:02.0f}"] = 0
                self._bits[f"y{i:02.0f}"] = 0
        
        self._instr = self._init_instr.copy()

    def _get_gate_output(self, x_in, y_in, gate):
        for instr in self._init_instr:
            inp, out = instr.split(" -> ")
            if x_in in inp and y_in in inp and gate in inp:
                return out.strip()
        raise ValueError(f"No gate output for {x_in} {gate} {y_in}")

    def _get_gate_partner_input(self, x_in, gate):
        for instr in self._init_instr:
            inp, _ = instr.split(" -> ")
            if x_in in inp and gate in inp:
                for x in inp.split(f" {gate} "):
                    if x != x_in:
                        return x
    
    def _get_gate_input(self, x_out, gate):
        for instr in self._init_instr:
            inp, out = instr.split(" -> ")
            if x_out == out and gate in inp:
                return inp.split(f" {gate} ")

    def verify(self, n=45):

        # Verify initial half adder
        s = self._get_gate_output("x00", "y00", "XOR")
        cin = self._get_gate_output("x00", "y00", "AND")

        if s != "z00":
            raise ValueError(f"Wrong output: {s} -> z00")

        for i in range(1, n):

            xy_xor = self._get_gate_output(f"x{i:02d}", f"y{i:02d}", "XOR")
            xy_and = self._get_gate_output(f"x{i:02d}", f"y{i:02d}", "AND")

            print(f"x{i:02d} XOR y{i:02d} -> {xy_xor}")
            print(f"x{i:02d} AND y{i:02d} -> {xy_and}")

            s = self._get_gate_output(xy_xor, cin, "XOR")

            print(f"{xy_xor} XOR {cin} -> {s}")

            if s != f"z{i:02d}":
                raise ValueError(f"Wrong output: {s} -> z{i:02d}")
            
            cin_and = self._get_gate_output(xy_xor, cin, "AND")

            cin = self._get_gate_output(xy_and, cin_and, "OR")
            print("")
 
    def __repr__(self):
        output = "Bits:\n"
        for bit, val in self._bits.items():
            output += f"  {bit} = {int(val)}\n"
        output += "\nRemaining instructions:\n"
        output += "\n".join(["  " + l for l in self._instr])
        return output


def parse_input(swap=None):

    with open(os.path.join(os.path.dirname(__file__), "input.txt"), "r") as file:
        lines = file.read().strip().split("\n")
    
    monitor = Monitor(lines, swap=swap)
    
    return monitor


def solve_level_1():
    """
    Solve level 1
    """

    # Read input file
    monitor = parse_input()

    monitor.run()

    return monitor.get_output()


def solve_level_2():
    """
    Solve level 2
    """

    swap = {
        "mbv XOR hks -> ggn": "mbv XOR hks -> z10",
        "gvm OR smt -> z10": "gvm OR smt -> ggn",
        "x17 XOR y17 -> jcb": "x17 XOR y17 -> ndw",
        "x17 AND y17 -> ndw": "x17 AND y17 -> jcb",
        "rmn XOR whq -> grm": "rmn XOR whq -> z32",
        "rmn AND whq -> z32": "rmn AND whq -> grm",
        "pqv XOR bnv -> twr": "pqv XOR bnv -> z39",
        "x39 AND y39 -> z39": "x39 AND y39 -> twr",
    }

    # Read input file
    monitor = parse_input(swap=swap)

    monitor.run()

    monitor.verify()

    wires = []
    for s in swap:
        wires.append(s.split()[-1])
    return ",".join(sorted(wires))


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
