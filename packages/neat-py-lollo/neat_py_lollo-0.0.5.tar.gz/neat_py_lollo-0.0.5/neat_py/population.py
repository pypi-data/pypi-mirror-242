from typing import List, Callable, Optional

from neat_py.agent import Agent
from neat_py.species import Species
from neat_py.neat_settings import Settings


class Population:
    def __init__(self, population_size: int, num_input: int, num_output: int) -> None:
        self.population_size: int = population_size
        self.num_input: int = num_input
        self.num_output: int = num_output

        self.agents: List[Agent] = []
        for i in range(self.population_size):
            self.agents.append(Agent(i, self.num_input, self.num_output))
            self.agents[i].brain.generate_network()
            self.agents[i].brain.mutate()

        self.species: List[Species] = []
        self.specialise()
        self.gen = 0
        self.best: Optional[Agent] = None
        self.best_fitness = 0

    def kill_not_improved(self) -> None:
        to_remove: List[Species] = []
        for s in self.species:
            if s.generation_without_improvement > Settings.PATIENCE:
                to_remove.append(s)

        for s in to_remove:
            self.species.remove(s)

    def avg_sum(self) -> float:
        avg_sum: float = 0
        for s in self.species:
            avg_sum += s.avg_fitness
        return avg_sum

    def calculate_fitness(self):
        current_max = 0
        for agent in self.agents:
            if agent.fitness > self.best_fitness:
                self.best_fitness = agent.fitness
                self.best = agent.clone()

            if agent.fitness > current_max:
                current_max = agent.fitness
        for agent in self.agents:
            agent.fitness /= current_max

    def natural_selection_classic(self) -> None:
        self.calculate_fitness()
        self.agents.sort(key=(lambda x: x.fitness), reverse=True)
        weights = [a.fitness for a in self.agents]
        new_pop = []
        for _ in range(self.population_size):
            parent_1 = Settings.rng.choices(self.agents, weights=weights)[0]
            parent_2 = Settings.rng.choices(self.agents, weights=weights)[0]
            child = parent_1.crossover(parent_2)
            new_pop.append(child)
        self.agents = new_pop

    def natural_selection(self) -> None:
        for s in self.species:
            s.update_fitness()
            s.update_old_fitness()
        self.species.sort(key=(lambda x: x.fitness), reverse=True)
        if self.best is None or self.species[0].champion.fitness > self.best.fitness:
            self.best = self.species[0].champion.clone()
        self.kill_not_improved()
        for s in self.species:
            s.cut()
            s.apply_fitness_sharing()
            s.update_avg()
        new_pop = []
        avg_sum: float = self.avg_sum()
        if self.best is not None:
            new_pop.append(self.best.clone())
        for s in self.species:
            child_num: int = int((s.avg_fitness / avg_sum) * (self.population_size-1)) - 1
            if child_num < 0:
                continue
            child = s.champion.clone()
            new_pop.append(child)
            for _ in range(child_num):
                if len(new_pop) > self.population_size:
                    break
                child = s.pull_child()
                new_pop.append(child)

            if len(new_pop) > self.population_size:
                break

        while len(new_pop) < self.population_size:
            if len(self.species) >= 1:
                child = self.species[0].pull_child()
            else:
                child = Agent(0, self.num_input, self.num_output)
            new_pop.append(child)

        self.agents = new_pop
        self.specialise()

    def remove_empty_species(self):
        to_remove: List[Species] = []
        for s in self.species:
            if s.is_empty():
                to_remove.append(s)

        for s in to_remove:
            self.species.remove(s)

    def specialise(self) -> None:
        for s in self.species:
            s.reset()

        for agent in self.agents:
            min_diff = Settings.DIFF_THRESHOLD
            min_diff_index = -1
            for i, s in enumerate(self.species):
                rep = s.rep
                diff = rep.similarity(agent, len(self.agents))
                if diff < min_diff:
                    min_diff_index = i
                    min_diff = diff
            if min_diff_index != -1:
                self.species[min_diff_index].agents.append(agent)
            else:
                self.species.append(Species(agent))
                self.species[len(self.species) - 1].agents.append(agent)

        self.remove_empty_species()

    def evolve(self, fitness_function: Callable[['Population'], None], num_generation: int = Settings.NUM_GENERATIONS):
        for g in range(num_generation):
            self.gen = g
            fitness_function(self)
            self.natural_selection()

            if len(self.agents) > self.population_size:
                raise Exception('Invalid pop size')

    def evolve_classic(self, fitness_function: Callable[['Population'], None],
                       num_generation: int = Settings.NUM_GENERATIONS):
        for g in range(num_generation):
            self.gen = g
            fitness_function(self)
            self.natural_selection_classic()

            if len(self.agents) > self.population_size:
                raise Exception('Invalid pop size')






