'''
Kaiju Cats Roblox game state representation for Simulated Annealing solver.

@author: Anh Duc Nguyen
@date: 2026-03-02
'''

import copy
import io
import sys

from GameSimulation import simulation


# Command costs and budget
COMMANDS_COST = {"N": 10, "S": 10, "E": 10, "W": 10, "SP": 20, "PU": 30}
BUDGET = 200


### Helper functions for State class ###

def make_empty_instructions(board):
    instructions = []
    for i in range(5):
        row = []
        for j in range(5):
            if board[i][j] in ["HV", "LV"]:
                row.append([None, None])
            elif board[i][j] == "PP":
                row.append([None])
            else:
                row.append(None)
        instructions.append(row)
    return instructions


def budget_used(instructions):
    total = 0
    for row in instructions:
        for cell in row:
            if cell is not None:
                for cmd in cell:
                    if cmd is not None:
                        total += COMMANDS_COST[cmd]
    return total


def get_slots(board):
    """Return list of (row, col, slot_idx, valid_commands) for every placeable slot."""
    slots = []
    for i in range(5):
        for j in range(5):
            if board[i][j] in ["HV", "LV"]:
                slots.append((i, j, 0, ["N", "S", "E", "W", "SP", "PU"]))
                slots.append((i, j, 1, ["N", "S", "E", "W", "SP", "PU"]))
            elif board[i][j] == "PP":
                slots.append((i, j, 0, ["N", "S", "E", "W", "PU"]))
    return slots

    """State class representing a candidate solution (set of instructions) 
       and its energy (negative score).

    Returns:
    - step(): randomly modifies the instructions in-place; stores info for undo()
    - undo(): reverts the last step()
    - energy(): computes and returns negative total power (lower is better)
    - clone(): returns a deep copy of this state
    - __str__(): returns a string representation of the instructions and budget used
    """
class State:
    def __init__(self, board, slots, rng, instructions=None):
        self.board = board
        self.slots = slots
        self.rng = rng
        self.instructions = instructions if instructions is not None else make_empty_instructions(board)
        self._last_change = None  # stored for undo()
        self._cached_energy = None

    def step(self):
        """Apply one random in-place change; stores enough info for undo()."""
        used = budget_used(self.instructions)

        for _ in range(20):  # retry until a valid move is found
            op = self.rng.choices(["add", "remove", "change", "swap"], weights=[3, 1, 4, 2])[0]
            i, j, slot_idx, valid_cmds = self.rng.choice(self.slots)
            cur = self.instructions[i][j][slot_idx]

            if op == "add" and cur is None:
                affordable = [c for c in valid_cmds if used + COMMANDS_COST[c] <= BUDGET]
                if affordable:
                    new_cmd = self.rng.choice(affordable)
                    self.instructions[i][j][slot_idx] = new_cmd
                    self._last_change = ("single", i, j, slot_idx, None)
                    break

            elif op == "remove" and cur is not None:
                self.instructions[i][j][slot_idx] = None
                self._last_change = ("single", i, j, slot_idx, cur)
                break

            elif op == "change":
                if cur is None:
                    affordable = [c for c in valid_cmds if used + COMMANDS_COST[c] <= BUDGET]
                else:
                    affordable = [
                        c for c in valid_cmds
                        if used - COMMANDS_COST[cur] + COMMANDS_COST[c] <= BUDGET
                    ]
                if affordable:
                    new_cmd = self.rng.choice(affordable)
                    self.instructions[i][j][slot_idx] = new_cmd
                    self._last_change = ("single", i, j, slot_idx, cur)
                    break

            elif op == "swap":
                i2, j2, s2, valid2 = self.rng.choice(self.slots)
                if (i, j, slot_idx) != (i2, j2, s2):
                    cur2 = self.instructions[i2][j2][s2]
                    if (cur2 is None or cur2 in valid_cmds) and (cur is None or cur in valid2):
                        self.instructions[i][j][slot_idx] = cur2
                        self.instructions[i2][j2][s2] = cur
                        self._last_change = ("swap", i, j, slot_idx, cur, i2, j2, s2, cur2)
                        break

        self._cached_energy = None

    def undo(self):
        """Revert the last step()."""
        if self._last_change is None:
            return
        if self._last_change[0] == "single":
            _, i, j, slot_idx, old_val = self._last_change
            self.instructions[i][j][slot_idx] = old_val
        elif self._last_change[0] == "swap":
            _, i, j, slot_idx, old1, i2, j2, s2, old2 = self._last_change
            self.instructions[i][j][slot_idx] = old1
            self.instructions[i2][j2][s2] = old2
        self._last_change = None
        self._cached_energy = None

    def energy(self):
        """Return negative total power (SA minimizes energy; we maximize score)."""
        if self._cached_energy is None:
            b_copy = copy.deepcopy(self.board)
            i_copy = copy.deepcopy(self.instructions)
            old_stdout = sys.stdout
            sys.stdout = io.StringIO()
            try:
                b, r, g = simulation(b_copy, i_copy)
            finally:
                sys.stdout = old_stdout
            self._cached_energy = -(b + r + g)
        return self._cached_energy

    def clone(self):
        """Return a deep copy of this state."""
        s = State(
            board=self.board,
            slots=self.slots,
            rng=self.rng,
            instructions=copy.deepcopy(self.instructions),
        )
        s._cached_energy = self._cached_energy
        return s

    def __str__(self):
        lines = []
        for i in range(5):
            parts = []
            for j in range(5):
                cell = self.instructions[i][j]
                s = str(cell) if cell is not None else "None"
                parts.append(s.ljust(20))
            lines.append(" ".join(parts))
        lines.append(f"Budget used: {budget_used(self.instructions)}/{BUDGET}")
        return "\n".join(lines)
