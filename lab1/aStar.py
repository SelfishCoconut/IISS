class AStar(Search):
    def __init__(self, problem, heuristic):
        super().__init__(problem)
        self.heuristic = heuristic
        self.counter = count()
        self.open = []
        self.open_states = {}  # Activamos el control de caminos dominados

    def insert_node(self, node, node_list):
        f = node.cost + self.heuristic.get_hcost(node)
        heapq.heappush(
            node_list,
            (f, node.cost, node.state.identifier, next(self.counter), node)
        )

    def extract_node(self, node_list):
        return heapq.heappop(node_list)[-1]

    def is_empty(self, node_list):
        return len(node_list) == 0
