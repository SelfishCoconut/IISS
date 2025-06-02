import json
from lab1.state import State
from lab1.action import Action

class Problem:
    def __init__(self, filename):
        
        with open(filename, mode='r', encoding='utf8') as file:
            self.data = json.load(file)

        self.initialIntersection = self.data['initial']
        self.finalIntersection = self.data['final']

        for inter in self.data['intersections']:
            if inter['identifier'] == self.initialIntersection:
                self.initialState = State(inter['identifier'], inter['longitude'], inter['latitude'])
            if inter['identifier'] == self.finalIntersection:
                self.finalState = State(inter['identifier'], inter['longitude'], inter['latitude'])

        self.actions = self.generate_action()
        self.intersections = {i["identifier"]: i for i in self.data["intersections"]}

    def generate_action(self):
        actions = {}
        for s in self.data['segments']:
            origin, dest, dist, spd = s['origin'], s['destination'], s['distance'], s['speed']
            if origin not in actions:
                actions[origin] = []
            actions[origin].append(Action(origin, dest, dist, spd))
        for origin in actions:
            actions[origin].sort(key=lambda a: a.cost)  # Ordenar por menor coste
        return actions

    def check_goal_state(self, state):
        return state == self.finalState

    def __str__(self):
        return f"Problem from {self.initialIntersection} to {self.finalIntersection}"