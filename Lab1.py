from lab1.problem import Problem
from lab1.search_algorithms import DepthFirst, BreadthFirst, IterativeDeepening
p = Problem('assets/lab1/problems/medium/calle_mariÌa_mariÌn_500_0.json')

print(p)
print("Initial State:", p.initialState,"\n")
print("Final State:", p.finalState ,"\n")

initial_id = p.initialState.identifier

if initial_id in p.actions:
    print(f"Number of actions available from initial state ({initial_id}): {len(p.actions[initial_id])}\n")
    print("First action from initial state:")

    print("\t" , p.actions[initial_id][0])
else:
    print("No actions available from the initial state.")

file = DepthFirst(Problem('assets/lab1/problems/medium/calle_mariÌa_mariÌn_500_0.json'))
file.do_search()

file = BreadthFirst(Problem('assets/lab1/problems/medium/calle_mariÌa_mariÌn_500_0.json'))
file.do_search()

file  = IterativeDeepening(Problem('assets/lab1/problems/medium/calle_mariÌa_mariÌn_500_0.json'))
file.do_search()