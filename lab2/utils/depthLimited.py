from lab1.search import Search

class DepthLimited(Search):
    def __init__(self, problem, limit):
        super().__init__(problem)
        self.limit = limit
        self.open = []

    def insert_node(self, node, node_list):
        node_list.insert(0, node)  # pila (LIFO)

    def extract_node(self, node_list):
        return node_list.pop(0)

    def is_empty(self, node_list):
        return len(node_list) == 0