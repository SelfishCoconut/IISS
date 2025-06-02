class BreadthFirst(Search):
    def __init__(self, problem):
        super().__init__(problem)
        self.open = []

    def insert_node(self, node, node_list):  # Insert at the end (FIFO)
        node_list.insert(len(node_list), node)

    def extract_node(self, node_list):       # Extract from the beginning
        return node_list.pop(0)

    def is_empty(self, node_list):
        return len(node_list) == 0