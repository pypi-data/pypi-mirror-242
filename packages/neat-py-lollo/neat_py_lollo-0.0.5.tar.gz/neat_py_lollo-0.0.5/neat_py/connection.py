import neat_py.node as node
from neat_py.neat_settings import Settings


class Connection:
    def __init__(self, from_node: 'node.Node', to_node: 'node.Node', weight: float, enabled: bool = True) -> None:
        self.from_node: 'node.Node' = from_node
        self.to_node: 'node.Node' = to_node
        self.weight: float = weight
        self.enabled: bool = enabled

    def mutate_weight(self) -> None:
        if Settings.rng.random() < Settings.WEIGHT_RESET_PROBABILITY:
            self.weight = node.random_float(-1, 1)
        else:
            self.weight += Settings.rng.gauss(0, 1) / 50

    def clone(self) -> 'Connection':
        return Connection(self.from_node, self.to_node, self.weight, self.enabled)

    def get_innovation_number(self) -> int:
        innovation_number = (1 / 2) * (self.from_node.number + self.to_node.number) * (
                self.from_node.number + self.to_node.number + 1) + self.to_node.number
        return int(innovation_number)
