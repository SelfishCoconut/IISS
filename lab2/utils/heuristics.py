class Heuristic(ABC):
    @abstractmethod
    def get_hcost(self, node):
        pass


class OptimisticHeuristic(Heuristic):
    def __init__(self, problem):
        self.problem = problem
        self.goal = (self.problem.finalState.latitude, self.problem.finalState.longitude)

    def get_hcost(self, node):
        coordinates = (node.state.latitude, node.state.longitude)
        return geodesic(coordinates, self.goal).km