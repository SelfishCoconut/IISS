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