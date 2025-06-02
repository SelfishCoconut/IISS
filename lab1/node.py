class Node:
    def __init__(self, state, depth=0, cost=0, parent=None, action=None):
        self.state = state
        self.depth = depth          #In case it's root, 0 by default
        self.cost = cost            #In case it's root, 0 by default
        self.parent = parent        #In case it's root, None by default
        self.action = action        #In case it's root, None by default (action to get to the child state)


    def __eq__(self,other):
       return isinstance(other, Node) and self.state == other.state

    #Method to resolve ties on comparisons of nodes (smaller id has priority in informed search algorithms)
    def __lt__(self, other):
        return self.cost < other.cost

    def getDepth(self):
        return self.depth

    def __str__(self):
        return ('The node is at state: '  + str(self.state) +
                ', with depth: ' + str(self.depth) +
                ', and cumulative cost: ' + str(self.cost))

    def __repr__(self):
        return f"Node({self.state}, cost={self.cost}, depth={self.depth})"