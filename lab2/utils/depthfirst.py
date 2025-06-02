class DepthFirst(Search):
    def __init__(self, problem):
        super().__init__(problem)
        self.open = []
        self.reverse_successors = True

    def insert_node(self, node, node_list):
        node_list.insert(0, node)

    def extract_node(self, node_list):
        return node_list.pop(0)

    def is_empty(self, node_list):
        return len(node_list) == 0