'''
Kaiju Cats Roblox game solver using SLS Simulated Annealing.

@author: Anh Duc Nguyen
@date: 2026-03-02
'''

import copy
import random

import BoardGeneration as bg
from GameSimulation import simulation
from SimulatedAnnealer import SimulatedAnnealer
from State import State, budget_used, get_slots, BUDGET


def solve(seed=42, restarts=5, iterations=2000, init_temp=500.0, decay_rate=0.997):
    board = bg.board_generation(seed)
    slots = get_slots(board)

    overall_best = None
    overall_best_energy = float("inf")

    for restart in range(restarts):
        run_seed = seed + restart * 1000
        print(f"Restart {restart + 1}/{restarts} (seed={run_seed}):")

        rng = random.Random(run_seed)
        init_state = State(board, slots, rng)
        annealer = SimulatedAnnealer(init_state, init_temp, decay_rate)
        best_state = annealer.search(iterations)

        score = -annealer.min_energy
        print(f"  -> score={score:.0f}  accept_rate={annealer.accept_rate:.1%}\n")

        if annealer.min_energy < overall_best_energy:
            overall_best_energy = annealer.min_energy
            overall_best = best_state

    assert overall_best is not None, "restarts must be > 0"
    return overall_best, -overall_best_energy


def main():
    seed = 42
    print("=" * 60)
    print("KaijuCats Instruction Solver (Simulated Annealing)")
    print("=" * 60 + "\n")

    best_state, best_score = solve(seed=seed, restarts=100, iterations=2000, 
                                   init_temp=500.0, decay_rate=0.997)

    used = budget_used(best_state.instructions)
    print(f"Best total power found: {best_score:.0f}")
    print(f"Budget used: {used}/{BUDGET}  (${BUDGET - used} remaining)")
    print("\nOptimized Instructions:")
    print(best_state)

    print("\n" + "=" * 60)
    print("Running final simulation with optimized instructions:")
    print("=" * 60)
    board = bg.board_generation(seed)
    simulation(copy.deepcopy(board), copy.deepcopy(best_state.instructions))


if __name__ == "__main__":
    main()
