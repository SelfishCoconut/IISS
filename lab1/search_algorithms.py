from lab1.search import Search
from lab1.depthLimited import DepthLimited

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

class IterativeDeepening(DepthLimited):
    def __init__(self, problem):
        super().__init__(problem, limit=1)  # Iniciamos con límite 1
        self.open = []

    def do_search(self, max_depth=1):
        current_depth = max_depth
        found = False
        while not found and current_depth < 10:
            print('---------------------------------------------------- Iteration', current_depth, '----------------------------------------------------')
            # Ejecutamos búsqueda limitada con profundidad actual
            found = super().do_search(max_depth=current_depth, iterative=True)
            current_depth += 1
            # Limpiamos cerrados para la próxima iteración
            self.closed_states.clear()
        if not found and current_depth == 10:
            self.solution_found = False
            super().display_solution()

    def insert_node(self, node, node_list):
        node_list.insert(0, node)  # Inserta al principio (pila)

    def extract_node(self, node_list):
        return node_list.pop(0)    # Extrae del principio (pila)

    def is_empty(self, node_list):
        return len(node_list) == 0
    