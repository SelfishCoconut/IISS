class BestFirst(Search):
    def __init__(self, problem, heuristic):
        super().__init__(problem)
        self.heuristic = heuristic
        self.open = PriorityQueue()
        self.current_nodes_stored = 0  # contador manual

    def insert_node(self, node, node_list):
        h = self.heuristic.get_hcost(node)
        node_list.put((h, node))
        self.current_nodes_stored += 1
        self.max_nodes_stored = max(self.max_nodes_stored, self.current_nodes_stored)

    def extract_node(self, node_list):
        self.current_nodes_stored -= 1
        return node_list.get()[1]

    def is_empty(self, node_list):
        return node_list.empty()