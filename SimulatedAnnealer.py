import math
import random


class SimulatedAnnealer:
    def __init__(self, init_state, init_temp, decay_rate):
        self.state = init_state
        self.energy = init_state.energy()
        self.min_state = init_state.clone()
        self.min_energy = self.energy
        self.accept_rate = 0.0
        self.init_temp = init_temp
        self.decay_rate = decay_rate

    def search(self, iterations):
        temperature = self.init_temp
        accepts = 0

        for i in range(iterations):
            if i % 500 == 0:
                print(
                    f"    iter {i:>5}: best={-self.min_energy:.0f}"
                    f"  current={-self.energy:.0f}"
                    f"  T={temperature:.2f}"
                )

            self.state.step()
            next_energy = self.state.energy()

            if (next_energy <= self.energy
                    or random.random() < math.exp(
                        max((self.energy - next_energy) / temperature, -20)
                    )):
                self.energy = next_energy
                accepts += 1
                if next_energy < self.min_energy:
                    self.min_state = self.state.clone()
                    self.min_energy = next_energy
            else:
                self.state.undo()

            temperature *= self.decay_rate

        self.accept_rate = accepts / iterations
        return self.min_state
