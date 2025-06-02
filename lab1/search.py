from abc import ABC, abstractmethod
from lab1.node import Node
from lab1.state import State
from datetime import timedelta
import time
class Search(ABC):
    def __init__(self, problem):
        self.problem = problem
        self.open = None
        self.closed_states = set()
        self.execution_time = 0
        self.total_cost = 0
        self.nodes_generated = 0
        self.nodes_expanded = 0
        self.max_nodes_stored = 0
        self.solution_depth = 0
        self.path_length = 0
        self.node_id_counter = 1
        self.solution_path = []
        self.solution_found = False
        self.reverse_successors = False
        self.open_states = None  # Activar solo en A* o Best-First si se desea

    @abstractmethod
    def insert_node(self, node, node_list): pass

    @abstractmethod
    def extract_node(self, node_list): pass

    @abstractmethod
    def is_empty(self, node_list): pass

    def generate_successors(self, node):
        successors = []
        for action in self.problem.actions.get(node.state.identifier, []):
            dest_id = action.destination
            dest_info = self.problem.intersections[dest_id]
            new_state = State(dest_id, dest_info["longitude"], dest_info["latitude"])
            new_node = Node(new_state, node.depth + 1, node.cost + action.cost, node, action)
            successors.append(new_node)
            self.nodes_generated += 1
            self.node_id_counter += 1
        return successors

    def recover_path(self, node):
        path = []
        while node.parent:
            path.append(node.action)
            node = node.parent
        return list(reversed(path))

    def display_solution(self, iterative=False):
        print(self.problem)
        print()
        if not self.solution_found:
            print("Generated nodes:", self.nodes_generated)
            print("Expanded nodes:", self.nodes_expanded)
            print("Execution time:", timedelta(seconds=self.execution_time))
            print("Solution length:", 0)
            print("Solution cost:", timedelta(seconds=0))
            print("Solution: []")
            return False
        else:
            print("Generated nodes:", self.nodes_generated)
            print("Expanded nodes:", self.nodes_expanded)
            print("Execution time:", timedelta(seconds=self.execution_time))
            print("Solution length:", self.solution_depth)
            print("Solution cost:", timedelta(seconds=self.total_cost))
            formatted = [f"{a.origin} → {a.destination} ({a.cost})" for a in self.solution_path]
            print("Solution:", "[" + ", ".join(formatted) + "]")
            return True

    def do_search(self, max_depth=None, iterative=False):
          start_time = time.perf_counter()
          self.insert_node(Node(self.problem.initialState), self.open)

          while not self.is_empty(self.open):
              if not isinstance(self.open, list) and not isinstance(self.open, PriorityQueue):
                  self.max_nodes_stored = max(self.max_nodes_stored, len(self.open))

              current = self.extract_node(self.open)

              # 💡 Evitar reexpandir estados ya visitados
              if current.state in self.closed_states:
                  continue

              # 💡 Ignorar nodos dominados por otros mejores en open_states
              if self.open_states is not None:
                  sid = current.state.identifier
                  if sid in self.open_states and current.cost > self.open_states[sid]:
                      continue

              # 🎯 Comprobación de objetivo
              if self.problem.check_goal_state(current.state):
                  self.solution_found = True
                  self.total_cost = current.cost
                  self.solution_depth = current.depth
                  self.solution_path = self.recover_path(current)
                  self.execution_time = time.perf_counter() - start_time
                  return self.display_solution(iterative)

              # 🔁 Generar sucesores solo si no hemos llegado a la profundidad máxima
              if max_depth is None or current.depth < max_depth:
                  successors = sorted(self.generate_successors(current), key=lambda s: s.state.identifier)
                  for s in successors:
                      sid = s.state.identifier
                      if self.open_states is not None:
                          if sid not in self.open_states or s.cost < self.open_states[sid]:
                              self.open_states[sid] = s.cost
                              self.insert_node(s, self.open)
                      else:
                          self.insert_node(s, self.open)

              # 🧠 Añadir estado a cerrados
              if not iterative:
                  self.closed_states.add(current.state)

              self.nodes_expanded += 1

          # 😕 Si se agota la búsqueda sin solución
          self.execution_time = time.perf_counter() - start_time
          return self.display_solution(iterative)
